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


class AssociationType:
    liked = "liked"
    tagged_at = "tagged_at"
    authored = "authored"
    friend = "friend"
    checked_in = "checked_in"
    poked = "poked"
    has_comment = "has_comment"  # Note this type doesn't have an inverse


class InverseAssociationType:
    liked_by = "liked_by"
    tagged = "tagged"
    authored_by = "authored_by"
    friend = "friend"
    locationed = "locationed"
    poked_by = "poked_by"


def invert_assoc(association_type):
    if association_type == AssociationType.liked:
        return InverseAssociationType.liked_by
    if association_type == AssociationType.tagged_at:
        return InverseAssociationType.tagged
    if association_type == AssociationType.authored:
        return InverseAssociationType.authored_by
    if association_type == AssociationType.friend:
        return InverseAssociationType.friend
    if association_type == AssociationType.checked_in:
        return InverseAssociationType.locationed
    if association_type == AssociationType.poked:
        return InverseAssociationType.poked_by
    if association_type == AssociationType.has_comment:  # Note this type doesn't have an inverse
        return AssociationType.has_comment
