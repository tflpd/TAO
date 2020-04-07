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

class Object:
    def __init__(self, object_id, object_type, keys_values):
        self.object_id = object_id
        self.otype = object_type
        self.keys_values = keys_values

    def __str__(self):
        return "OBJECT [ID]: " + str(self.object_id) + " [TYPE]: " + str(self.otype) + " [KEYS-VALUES]: " + str(self.keys_values)

    def get_id(self):
        return self.object_id


class Association:
    def __init__(self, obj1, association_type, obj2, creation_time, keys_values):
        self.object_id1 = obj1
        self.atype = association_type
        self.object_id2 = obj2
        self.creation_time = creation_time
        self.keys_values = keys_values

    def __str__(self):
        return "ASSOCIATION [ID1]: " + str(self.object_id1) + " [TYPE]: " + str(self.atype) + " [ID2]: " +\
               str(self.object_id2) + " [TIME]: " + str(self.creation_time) + " [KEYS-VALUES]: " + str(self.keys_values)
