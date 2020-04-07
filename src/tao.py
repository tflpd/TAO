from src.database import Database
from src.structs import Object, Association

OBJECTS_TYPES = {"user", "post", "comment", "location", "checkin", "page"}

ASSOCIATION_TYPES = {"liked", "tagged_at", "authored", "friend", "checked_in", "has_comment"}
INV_ASSOCIATION_TYPES = {"liked_by", "tagged", "authored_by", "friend", "locationed"}


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
##

def main():
    db = Database()

    obj1 = Object(1, "user", {'name': 'thanos'})
    obj2 = Object(2, "user", {'name': 'anna'})
    asoc1 = Association(obj1.get_id(), "friend", obj2.get_id(), 10, {"status": "haha"})
    asoc2 = Association(obj1.get_id(), "friend", 3, 10, {"status": "hihi"})
    #print(asoc1)

    db.create_object(obj1)
    db.create_object(obj2)
    db.add_association(asoc1)
    db.add_association(asoc2)
    asocs = db.get_associations(obj1.get_id(), "friend", [obj2.get_id(), 3], 0, 0)
    for asoc in asocs:
        print(asoc)

    db.close()


if __name__ == "__main__":
    main()
