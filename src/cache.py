from src.database import Database
from src.structs import Object, Association
from src.LRU_cache import LRUCache

class Node:
    def __init__(self, objects_cache_size, associations_lists_cache_size, associations_counts_cache_size, db):
        self.obj_size = objects_cache_size
        self.assoc_lists_size = associations_lists_cache_size
        self.assoc_counts_size = associations_counts_cache_size
        self.objects = LRUCache(objects_cache_size)
        self.assoc_lists = LRUCache(associations_lists_cache_size)
        self.assoc_counts = LRUCache(associations_counts_cache_size)
        self.database = db

    def obj_get(self, obj_id):
        obj = self.objects.get(obj_id)
        if obj != -1:
            return obj
        obj = self.database.retrieve_object(obj_id)
        if obj is None:
            print("{MSG} OBJECT [ID]: " + obj_id + " is neither in cache nor the storage")
            return None
        return obj

    def assoc_get(self, id1, atype, id2set, low=None, high=None):
        assocs = []
        assocs_not_in_cache = []
        # THE BELOW NEEDS REVISION
        for id2 in id2set:
            key = (id1, atype, id2)
            assoc = self.assoc_lists.get(key)
            if low is not None and high is not None:
                if assoc != -1 and low <= assoc.creation_time <= high:
                    assocs.append(assoc)
                else:
                    assocs_not_in_cache.append(id2)
            else:
                if assoc != -1:
                    assocs.append(assoc)
                else:
                    assocs_not_in_cache.append(id2)
        storage_assocs = self.database.get_associations(id1, atype, assocs_not_in_cache, low, high)
        assocs.extend(storage_assocs)
        return assocs

    def assoc_count(self, id1, atype):
        key = (id1, atype)
        count = self.assoc_counts.get(key)
        if count != -1:
            return count
        return self.database.count_associations(id1, atype)
