from src.structs import Object, Association, key_found_in_cache, key_found_in_storage, assocs_to_str
from src.LRU_cache import LRUCache
from src.flags import DEBUG_FLAG


class TAONode:
    def __init__(self, objects_cache_size, associations_lists_cache_size, associations_counts_cache_size, db):
        self.obj_size = objects_cache_size
        self.assoc_lists_size = associations_lists_cache_size
        self.assoc_counts_size = associations_counts_cache_size
        self.objects_cache = LRUCache(objects_cache_size)
        self.assoc_lists_cache = LRUCache(associations_lists_cache_size)
        self.assoc_counts_cache = LRUCache(associations_counts_cache_size)
        self.database = db

    def obj_get(self, obj_id):
        obj = self.objects_cache.get_element(obj_id)
        if obj != -1:
            print(key_found_in_cache(obj_id))
            return obj
        obj = self.database.retrieve_object(obj_id)
        if obj is None:
            if DEBUG_FLAG:
                print("{MSG} OBJECT [ID]: " + str(obj_id) + " is neither in TAO cache nor the storage")
                return obj
        else:
            self.objects_cache.set(obj_id, obj)
            print(key_found_in_storage(obj_id))
            return obj

    def obj_add(self, object_id, object_type, keys_values):
        try:
            obj = Object(object_id, object_type, keys_values)
            self.database.create_object(obj)
            self.objects_cache.set(object_id, obj)
        except:
            if DEBUG_FLAG:
                print("{MSG} OBJECT [ID]: " + str(object_id) + " [TYPE]: " + object_type +
                      " creation failed. Probably this id exists already, consider using obj_update")

    def obj_update(self, object_id, object_type, keys_values):
        try:
            obj = Object(object_id, object_type, keys_values)
            self.database.update_object(obj)
            self.objects_cache.set(object_id, obj)
        except:
            if DEBUG_FLAG:
                print("{MSG} OBJECT [ID]: " + str(object_id) + " [TYPE]: " + object_type +
                      " update failed. This shouldn't have failed, you did sth miserably wrong")

    # This assumes that since TAO sacrifices consistency over performance
    # we prefer to leave the cached object in the cached until it is eventually
    # kicked out than to look it up and delete it, so we just delete from the
    # storage
    # TODO: Should this cascade to associations? Privacy concern; Is the data of a deleted user kept?
    def obj_delete(self, object_id):
        self.database.delete_object(object_id)

    def assoc_add(self, object_id1, association_type, object_id2, creation_time, keys_values):
        try:
            new_assoc = Association(object_id1, association_type, object_id2, creation_time, keys_values)
            self.database.add_association(new_assoc)
            key = (object_id1, association_type)
            cached_assocs_list = self.assoc_lists_cache.get_element(key)

            if cached_assocs_list == -1:
                self.assoc_lists_cache.set(key, [new_assoc])
                assoc_counter = 1
            else:
                cached_assocs_list.append(new_assoc)
                cached_assocs_list.sort(key=lambda x: x.creation_time, reverse=True)
                self.assoc_lists_cache.set(key, cached_assocs_list)
                assoc_counter = len(cached_assocs_list)
            # Following TAO's details the counts caches understand the semantics of their contents
            # and for that reason they should be be in coordination with the actual assoc list
            self.assoc_counts_cache.set(key, assoc_counter)
        except:
            if DEBUG_FLAG:
                print("{MSG} ASSOCIATION [ID1]: " + str(object_id1) + " [TYPE]: " + str(association_type) +
                      " [ID2]: " + str(object_id2) + " creation failed. Probably this key exists already, "
                                                     "consider using assoc_delete first")

    def assoc_get(self, id1, atype, id2set, low=None, high=None):
        ret_assocs = []
        key = (id1, atype)
        cached_assocs = self.assoc_lists_cache.get_element(key)
        cached_id2s = []
        not_cached_id2s = []

        # Retrieve the ones that exist already in cache (if any)
        # Iterate through the ones in cache
        if cached_assocs != -1:
            print(key_found_in_cache(key))
            for assoc in cached_assocs:
                # If any of them is in the requested set of id2s
                if assoc.object_id2 in id2set:
                    # If the low and high filter is set
                    if low is not None and high is not None:
                        # And they actually pass that filter
                        if low <= assoc.creation_time <= high:
                            # Then append them to the list of cached id2s of interest and the list of
                            # associations we will return
                            cached_id2s.append(assoc.object_id2)
                            ret_assocs.append(assoc)
                    else:
                        # Else if there is no filtering simply add them
                        cached_id2s.append(assoc.object_id2)
                        ret_assocs.append(assoc)

        # Create a list with those that we need to search for in storage
        for id2 in id2set:
            if id2 not in cached_id2s:
                not_cached_id2s.append(id2)
        # Retrieve them from storage
        storaged_assocs = self.database.get_associations(id1, atype, not_cached_id2s, low, high)
        # Create the final sorted list by descending creation time
        ret_assocs.extend(storaged_assocs)
        ret_assocs.sort(key=lambda x: x.creation_time, reverse=True)
        # Add it to cache
        self.assoc_lists_cache.set(key, ret_assocs)
        # Following TAO's details the counts caches understand the semantics of their contents
        # and for that reason they should be be in coordination with the actual assoc list
        if ret_assocs:
            assoc_counter = len(ret_assocs)
            self.assoc_counts_cache.set(key, assoc_counter)
        if DEBUG_FLAG and not ret_assocs:
            print("{MSG} QUERY assoc_get WITH ARGS: " + str(id1) + " " + atype + " " + id2set + " " + str(low) + " "
                  + str(high) + " RETURNED EMPTY")
        return ret_assocs

    def assoc_count(self, id1, atype):
        key = (id1, atype)
        count = self.assoc_counts_cache.get_element(key)
        if count == -1:
            count = self.database.count_associations(id1, atype)
            self.assoc_counts_cache.set(key, count)
        return count

    def assoc_range(self, id1, atype, pos, limit):
        key = (id1, atype)
        # The following is not part of the paper and it is an optimization
        # In order to quickly find whether we can answer the query on the [pos, pos+limit) domain
        # we firstly try to see whether we have enough associations stored in memory so we can avoid
        # visiting the storage
        assoc_counter = self.assoc_counts_cache.get_element(key)
        if assoc_counter != -1 and assoc_counter >= pos + limit:
            ret_assocs = self.assoc_lists_cache.get_element(key)
            return ret_assocs[pos, pos + limit]
        return self.database.get_associations_range(id1, atype, pos, limit)

    def assoc_time_range(self, id1, atype, low, high, limit):
        return self.database.get_associations_time_range(id1, atype, low, high, limit)

    def assoc_del(self, id1, atype, id2):
        self.database.delete_association(id1, atype, id2)
