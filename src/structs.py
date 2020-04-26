import random
from src.flags import VERBOSE_FLAG

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
        if VERBOSE_FLAG:
            return "{LOG} OBJECT [ID]: " + str(self.object_id) + " [TYPE]: " + str(
                self.otype) + " [KEYS-VALUES]: " + str(self.keys_values)
        else:
            return "{LOG} OBJECT [ID]: " + str(self.object_id)

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
        if VERBOSE_FLAG:
            return "{LOG} ASSOCIATION [ID1]: " + str(self.object_id1) + " [TYPE]: " + str(self.atype) + " [ID2]: " + \
                   str(self.object_id2) + " [TIME]: " + str(self.creation_time) + " [KEYS-VALUES]: " + str(
                self.keys_values)
        else:
            return "{LOG} ASSOCIATION [ID1]: " + str(self.object_id1) + " [TYPE]: " + str(self.atype) + " [ID2]: " + \
                   str(self.object_id2)

    def __eq__(self, other):
        if not isinstance(other, Association):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.object_id1 == other.object_id1 and self.atype == other.atype and self.object_id2 == other.object_id2


class AssociationType:
    liked = "liked"
    tagged_at = "tagged_at"
    authored = "authored"
    friend = "friend"
    checked_in = "checked_in"
    poked = "poked"
    has_comment = "has_comment"  # Note this type doesn't have an inverse


def get_random_assoc_type():
    assoc_probability = random.random()
    if assoc_probability < 0.14:
        return AssociationType.liked
    elif assoc_probability < 0.28:
        return AssociationType.tagged_at
    elif assoc_probability < 0.42:
        return AssociationType.authored
    elif assoc_probability < 0.56:
        return AssociationType.friend
    elif assoc_probability < 0.70:
        return AssociationType.checked_in
    elif assoc_probability < 0.84:
        return AssociationType.poked
    else:
        return AssociationType.has_comment


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


class ObjectType:
    user = "user"
    post = "post"
    comment = "comment"
    location = "location"
    checkin = "checkin"
    page = "page"


def get_random_object_type():
    obj_probability = random.random()
    if obj_probability < 0.16:
        return ObjectType.user
    elif obj_probability < 0.32:
        return ObjectType.post
    elif obj_probability < 0.48:
        return ObjectType.page
    elif obj_probability < 0.64:
        return ObjectType.location
    elif obj_probability < 0.80:
        return ObjectType.checkin
    else:
        return ObjectType.comment


def key_found_in_cache(key):
    # If it is a key of an Object
    if type(key) is int:
        return "{LOG} OBJECT [ID]: " + str(key) + " was found in cache"
    # If it is a key of an Association
    elif len(key) == 2:
        return "{LOG} ASSOCIATION [ID1]: " + str(key[0]) + " [TYPE]: " + str(key[1]) + " was found in cache"
    else:
        return "{MSG} KEY: " + str(key) + " has an unexpected amount of arguments"


def key_found_in_storage(key):
    # If it is a key of an Object
    if type(key) is int:
        return "{LOG} OBJECT [ID]: " + str(key) + " was found in storage"
    # If it is a key of an Association
    elif len(key) == 2:
        return "{LOG} ASSOCIATION [ID1]: " + str(key[0]) + " [TYPE]: " + str(key[1]) + " was found in storage"
    else:
        return "{MSG} KEY: " + key + " has an unexpected amount of arguments"


def assocs_to_str(assocs):
    try:
        string = ""
        for assoc in assocs:
            string += " " + str(assoc)
        return string
    except:
        print("Not valid associations list")
        return "N/A"
