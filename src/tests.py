from src.LRU_cache import LRUCache
from src.TAO_cache import TAONode
from src.database import Database
from src.flags import NUM_OPS, DEBUG_FLAG
from src.structs import Object, Association, ObjectType, AssociationType, InverseAssociationType, get_random_assoc_type, \
    get_random_object_type
import random


class UnitTests:
    def __init__(self):
        print("Started executing unit test...")
        db = Database()
        obj1 = Object(object_id=1, object_type="user", keys_values={'name': 'thanos'})
        obj2 = Object(object_id=2, object_type="user", keys_values={'name': 'anna'})
        asoc1 = Association(obj1=obj1.get_id(), association_type="friend", obj2=obj2.get_id(), creation_time=10,
                            keys_values={"status": "haha"})
        asoc2 = Association(obj1=obj1.get_id(), association_type="friend", obj2=3, creation_time=13,
                            keys_values={"status": "hehe"})

        db.create_object(obj1)
        db.delete_object(obj2.object_id)
        print(db.retrieve_object(obj1.object_id))
        obj11 = Object(4, "user", {'name': 'thanossss'})
        db.update_object(obj11)
        print(db.retrieve_object(obj11.object_id))
        db.create_object(obj2)
        db.add_association(asoc1)
        db.add_association(asoc2)
        asocs = db.get_associations(obj1.get_id(), "friend", [obj2.get_id(), 3])
        asocs = db.count_associations(obj1.get_id(), "friend")
        asocs = db.get_associations_time_range(obj1.get_id(), "friend", 0, 13, 2)
        for asoc in asocs:
            print(asoc)
        asocs = db.get_associations(obj2.get_id(), "friend", [obj1.get_id(), 3], 0, 11)
        for asoc in asocs:
            print(asoc)
        asocs = db.get_all_associations()
        for asoc in asocs:
            print(asoc)

        # LRU TESTING
        key1 = (1, 1)
        key2 = (2, 2)
        key3 = (3, 3)

        cache = LRUCache(3)

        cache.set(key1, obj1)
        cache.print_objects()

        cache.set(key2, obj1)
        cache.print_objects()

        cache.get_element(key1)
        cache.print_objects()

        cache.set(key3, obj1)
        cache.print_objects()

        cache.get_element(key3)
        cache.print_objects()

        db.close()


class PaperExample:
    def __init__(self):
        print("Started executing paper's example...")
        db = Database()

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

        # Reference client implementation
        # The first row has the natural language query
        # The second row has the TAO API translated query

        obj = tao.obj_get(632)
        if obj is not None:
            print(obj)
        obj = tao.obj_get(632)
        if obj is not None:
            print(obj)
        obj = tao.obj_get(632)
        if obj is not None:
            print(obj)
        tao.assoc_lists_cache.print_assocs()
        assocs = tao.assoc_get(obj1.get_id(), AssociationType.friend, [obj2.get_id()])
        assocs = tao.assoc_get(obj1.get_id(), AssociationType.friend, [obj2.get_id()])
        assocs = tao.assoc_range(obj1.get_id(), AssociationType.friend, 0, 10)
        assocs = tao.assoc_time_range(obj1.get_id(), AssociationType.friend, 0, 2, 10)
        if assocs is not None:
            for assoc in assocs:
                print(assoc)
        assocs_count = tao.assoc_count(obj1.get_id(), AssociationType.friend)
        assocs_count = db.count_associations(obj6.get_id(), InverseAssociationType.authored_by)
        print(assocs_count)

        db.close()


class RandomTestsGenerator:
    def __init__(self):
        print("Started executing random generated test...")
        random.seed(1)
        db = Database()
        tao = TAONode(objects_cache_size=1, associations_lists_cache_size=1, associations_counts_cache_size=1, db=db)
        curr_obj_id = -1
        curr_time = 0
        keys_values = {"dict": "with keys values"}

        write_reqs = ["assoc_add", "assoc_del", "obj_add", "obj_update", "obj_delete"]
        write_reqs_weights = [52.5, 8.3, 16.5, 20.7, 2]
        read_reqs = ["assoc_get", "assoc_range", "assoc_time_range", "assoc_count", "obj_get"]
        read_reqs_weights = [15.7, 40.9, 2.8, 11.7, 28.9]

        curr_obj_id += 1
        id1 = curr_obj_id
        tao.obj_add(id1, get_random_object_type(), keys_values)
        curr_obj_id += 1
        id1 = curr_obj_id
        tao.obj_add(id1, get_random_object_type(), keys_values)

        for operation in range(NUM_OPS):
            operation_probability = random.random()
            if operation_probability < 0.90:
                if DEBUG_FLAG:
                    print(" About to perform read operation: ", end="")
                op = random.choices(read_reqs, read_reqs_weights)
                if op[0] == "assoc_range":
                    id1 = random.randrange(0, curr_obj_id + 1)
                    if DEBUG_FLAG:
                        print("assoc_range")
                    tao.assoc_range(id1, get_random_assoc_type(), 0, 10)
                elif op[0] == "obj_get":
                    id1 = random.randrange(0, curr_obj_id + 1)
                    if DEBUG_FLAG:
                        print("obj_get")
                    tao.obj_get(id1)
                elif op[0] == "assoc_get":
                    id1 = random.randrange(0, curr_obj_id + 1)
                    existing_ids = list(range(curr_obj_id + 1))
                    existing_ids.remove(id1)
                    id2set = random.choices(existing_ids)
                    if DEBUG_FLAG:
                        print("assoc_get")
                    tao.assoc_get(id1, get_random_assoc_type(), id2set, 0, curr_time)
                elif op[0] == "assoc_count":
                    id1 = random.randrange(0, curr_obj_id + 1)
                    if DEBUG_FLAG:
                        print("assoc_count")
                    tao.assoc_count(id1, get_random_assoc_type())
                else:
                    id1 = random.randrange(0, curr_obj_id + 1)
                    if DEBUG_FLAG:
                        print("assoc_time_range")
                    tao.assoc_time_range(id1, get_random_assoc_type(), 0, curr_time, 10)
            else:
                op = random.choices(write_reqs, write_reqs_weights)
                if DEBUG_FLAG:
                    print(" About to perform write operation: ", end="")
                if op[0] == "assoc_add":
                    creation_time = curr_time
                    curr_time += 1
                    id1 = random.randrange(0, curr_obj_id + 1)
                    id2 = random.randrange(0, curr_obj_id + 1)
                    while id1 == id2:
                        id2 = random.randrange(0, curr_obj_id + 1)
                    if DEBUG_FLAG:
                        print("assoc_add")
                    tao.assoc_add(id1, get_random_assoc_type(), id2, creation_time, keys_values)
                elif op[0] == "obj_update":
                    id1 = random.randrange(0, curr_obj_id + 1)
                    if DEBUG_FLAG:
                        print("obj_update")
                    tao.obj_update(id1, get_random_object_type(), keys_values)
                elif op[0] == "obj_add":
                    curr_obj_id += 1
                    id1 = curr_obj_id
                    if DEBUG_FLAG:
                        print("obj_add")
                    tao.obj_add(id1, get_random_object_type(), keys_values)
                elif op[0] == "assoc_del":
                    id1 = random.randrange(0, curr_obj_id + 1)
                    id2 = random.randrange(0, curr_obj_id + 1)
                    while id1 == id2:
                        id2 = random.randrange(0, curr_obj_id + 1)
                    if DEBUG_FLAG:
                        print("assoc_del")
                    tao.assoc_del(id1, get_random_assoc_type(), id2)
                else:
                    id1 = random.randrange(0, curr_obj_id + 1)
                    if DEBUG_FLAG:
                        print("obj_delete")
                    tao.obj_delete(id1)

        db.close()
