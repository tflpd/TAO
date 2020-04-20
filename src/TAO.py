from src.TAO_cache import TAONode
from src.database import Database
from src.structs import Object, Association
from src.LRU_cache import LRUCache
from src.structs import AssociationType, ObjectType, InverseAssociationType

OBJECTS_TYPES = {"user", "post", "comment", "location", "checkin", "page"}

ASSOCIATION_TYPES = {"liked", "tagged_at", "authored", "friend", "checked_in", "poked", "has_comment"}
INV_ASSOCIATION_TYPES = {"liked_by", "tagged", "authored_by", "friend", "locationed", "poked_by"}


##
# How to read the above:
# user liked post
# post liked_by user
#
# user tagged_at checkin
# checkin tagged user
#
# checkin locationed location
# location checked_in checkin
#
# checkin has_comment comment
#
# etc
#
# start = time.time()
# print(f’Duration: {time.time() — start}s’)
##

def main():
    db = Database()

    # obj1 = Object(object_id=1, object_type="user", keys_values={'name': 'thanos'})
    # obj2 = Object(object_id=2, object_type="user", keys_values={'name': 'anna'})
    # asoc1 = Association(obj1=obj1.get_id(), association_type="friend", obj2=obj2.get_id(), creation_time=10, keys_values={"status": "haha"})
    # asoc2 = Association(obj1=obj1.get_id(), association_type="friend", obj2=3, creation_time=13, keys_values={"status": "hihi"})
    # print(asoc1.creation_time)

    # db.create_object(obj1)
    # db.delete_object(obj2.object_id)
    # print(db.retrieve_object(obj1.object_id))
    # obj11 = Object(4, "user", {'name': 'thanossss'})
    # db.update_object(obj11)
    # print(db.retrieve_object(obj11.object_id))
    # db.create_object(obj2)
    # db.add_association(asoc1)
    # db.add_association(asoc2)
    # asocs = db.get_associations(obj1.get_id(), "friend", [obj2.get_id(), 3])
    # asocs = db.count_associations(obj1.get_id(), "friend")
    # asocs = db.get_associations_time_range(obj1.get_id(), "friend", 0, 13, 2)
    # for asoc in asocs:
    #     print(asoc)
    # asocs = db.get_associations(obj2.get_id(), "friend", [obj1.get_id(), 3], 0, 11)
    # for asoc in asocs:
    #     print(asoc)
    # asocs = db.get_all_associations()
    # for asoc in asocs:
    #     print(asoc)

    # LRU TESTING
    # key1 = (1, 1)
    # key2 = (2, 2)
    # key3 = (3, 3)
    #
    # cache = LRUCache(3)
    #
    # cache.set(key1, obj1)
    # cache.print_elements()
    #
    # cache.set(key2, obj1)
    # cache.print_elements()
    #
    # cache.get_element(key1)
    # cache.print_elements()
    #
    # cache.set(key3, obj1)
    # cache.print_elements()
    #
    # cache.get_element(key3)
    # cache.print_elements()

    # TAO node testing
    tao = TAONode(objects_cache_size=1, associations_lists_cache_size=1, associations_counts_cache_size=1, db=db)
    # Create the objects and the associations and add them in the DB/Cache
    obj1 = Object(object_id=105, object_type=ObjectType.user, keys_values={'name': 'Alice'})
    tao.obj_add(object_id=105, object_type=ObjectType.user, keys_values={'name': 'Alice'})

    obj2 = Object(object_id=244, object_type=ObjectType.user, keys_values={'name': 'Bob'})
    tao.obj_add(object_id=244, object_type=ObjectType.user, keys_values={'name': 'Bob'})

    obj3 = Object(object_id=379, object_type=ObjectType.user, keys_values={'name': 'Cathy'})
    tao.obj_add(object_id=379, object_type=ObjectType.user, keys_values={'name': 'Cathy'})

    obj4 = Object(object_id=471, object_type=ObjectType.user, keys_values={'name': 'David'})
    tao.obj_add(object_id=471, object_type=ObjectType.user, keys_values={'name': 'David'})

    obj5 = Object(object_id=534, object_type=ObjectType.location,
                  keys_values={'name': 'Golden Gate Bridge', 'loc': '38.019820N, 23.846082W'})
    tao.obj_add(object_id=534, object_type=ObjectType.location,
                keys_values={'name': 'Golden Gate Bridge', 'loc': '38.019820N, 23.846082W'})

    obj6 = Object(object_id=632, object_type=ObjectType.checkin, keys_values={})
    tao.obj_add(object_id=632, object_type=ObjectType.checkin, keys_values={})

    obj7 = Object(object_id=771, object_type=ObjectType.comment, keys_values={'text': 'Wish we were there!'})
    tao.obj_add(object_id=771, object_type=ObjectType.comment, keys_values={'text': 'Wish we were there!'})

    # Alice and Bob are friends
    assoc1 = Association(obj1=obj1.get_id(), association_type=AssociationType.friend, obj2=obj2.get_id(),
                         creation_time=1,
                         keys_values={"friendship_level": "buddies"})
    tao.assoc_add(object_id1=obj1.get_id(), association_type=AssociationType.friend, object_id2=obj2.get_id(),
                  creation_time=1,
                  keys_values={"friendship_level": "buddies"})
    # Alice and Cathy are friends
    assoc2 = Association(obj1=obj1.get_id(), association_type=AssociationType.friend, obj2=obj3.get_id(),
                         creation_time=2,
                         keys_values={"friendship_level": "good buddies"})
    tao.assoc_add(object_id1=obj1.get_id(), association_type=AssociationType.friend, object_id2=obj3.get_id(),
                  creation_time=2,
                  keys_values={"friendship_level": "good buddies"})
    # Bob and Cathy are friends
    assoc3 = Association(obj1=obj2.get_id(), association_type=AssociationType.friend, obj2=obj3.get_id(),
                         creation_time=3,
                         keys_values={"friendship_level": "best buddies"})
    tao.assoc_add(object_id1=obj2.get_id(), association_type=AssociationType.friend, object_id2=obj3.get_id(),
                  creation_time=3,
                  keys_values={"friendship_level": "best buddies"})
    # Bob and David are friends
    assoc4 = Association(obj1=obj2.get_id(), association_type=AssociationType.friend, obj2=obj4.get_id(),
                         creation_time=4,
                         keys_values={"friendship_level": "super buddies"})
    tao.assoc_add(object_id1=obj2.get_id(), association_type=AssociationType.friend, object_id2=obj4.get_id(),
                  creation_time=4,
                  keys_values={"friendship_level": "super buddies"})
    # Cathy and David are friends
    assoc5 = Association(obj1=obj3.get_id(), association_type=AssociationType.friend, obj2=obj4.get_id(),
                         creation_time=5,
                         keys_values={"friendship_level": "super duper buddies"})
    tao.assoc_add(object_id1=obj3.get_id(), association_type=AssociationType.friend, object_id2=obj4.get_id(),
                  creation_time=5,
                  keys_values={"friendship_level": "super duper buddies"})

    # Alice has authored a checkin
    assoc6 = Association(obj1=obj1.get_id(), association_type=AssociationType.authored, obj2=obj6.get_id(),
                         creation_time=6,
                         keys_values={"has_checked_in_before_there": "true"})
    tao.assoc_add(object_id1=obj1.get_id(), association_type=AssociationType.authored, object_id2=obj6.get_id(),
                  creation_time=6,
                  keys_values={"has_checked_in_before_there": "true"})
    # Cathy has authored a comment
    assoc8 = Association(obj1=obj3.get_id(), association_type=AssociationType.authored, obj2=obj7.get_id(),
                         creation_time=8,
                         keys_values={"see_more_indication": "true"})
    tao.assoc_add(object_id1=obj3.get_id(), association_type=AssociationType.authored, object_id2=obj7.get_id(),
                  creation_time=8,
                  keys_values={"see_more_indication": "true"})

    # Bob has tagged in a checkin
    assoc7 = Association(obj1=obj2.get_id(), association_type=AssociationType.tagged_at, obj2=obj6.get_id(),
                         creation_time=7,
                         keys_values={"has_checked_in_before_there": "true"})
    tao.assoc_add(object_id1=obj2.get_id(), association_type=AssociationType.tagged_at, object_id2=obj6.get_id(),
                  creation_time=7,
                  keys_values={"has_checked_in_before_there": "true"})

    # David has liked a comment
    assoc9 = Association(obj1=obj4.get_id(), association_type=AssociationType.liked, obj2=obj7.get_id(),
                         creation_time=9,
                         keys_values={})
    tao.assoc_add(object_id1=obj4.get_id(), association_type=AssociationType.liked, object_id2=obj7.get_id(),
                  creation_time=9,
                  keys_values={})

    # A checkin was made to Golden Gate Bridge location
    assoc10 = Association(obj1=obj6.get_id(), association_type=AssociationType.checked_in, obj2=obj5.get_id(),
                          creation_time=10,
                          keys_values={})
    tao.assoc_add(object_id1=obj6.get_id(), association_type=AssociationType.checked_in, object_id2=obj5.get_id(),
                  creation_time=10,
                  keys_values={})

    # A checkin has a comment in it
    assoc11 = Association(obj1=obj6.get_id(), association_type=AssociationType.has_comment, obj2=obj7.get_id(),
                          creation_time=11,
                          keys_values={"time": "1334511670"})
    tao.assoc_add(object_id1=obj6.get_id(), association_type=AssociationType.has_comment, object_id2=obj7.get_id(),
                  creation_time=11,
                  keys_values={"time": "1334511670"})

    # Test whether the above functions work as expected
    # obj = tao.obj_get(632)
    # if obj is not None:
    #     print(obj)
    # obj = tao.obj_get(632)
    # if obj is not None:
    #     print(obj)
    # obj = tao.obj_get(632)
    # if obj is not None:
    #     print(obj)
    #tao.assoc_lists_cache.print_assocs()
    #assocs = tao.assoc_get(obj1.get_id(), AssociationType.friend, [obj2.get_id()])
    #assocs = tao.assoc_range(obj1.get_id(), AssociationType.friend, 0, 10)
    # assocs = tao.assoc_time_range(obj1.get_id(), AssociationType.friend, 0, 2, 10)
    # if assocs is not None:
    #     for assoc in assocs:
    #         print(assoc)
    #assocs_count = tao.assoc_count(obj1.get_id(), AssociationType.friend)
    assocs_count = db.count_associations(obj6.get_id(), InverseAssociationType.authored_by)
    print(assocs_count)

    db.close()


if __name__ == "__main__":
    main()