import time

from src.TAO_cache import TAONode
from src.database import Database
from src.structs import Object, Association
from src.LRU_cache import LRUCache
from src.structs import AssociationType, ObjectType, InverseAssociationType
from src.tests import UnitTests, PaperExample, RandomTestsGenerator

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
    #unit_test = UnitTests()
    #paper_example_test = PaperExample()
    start = time.time()
    random_test = RandomTestsGenerator()
    end = time.time()
    print("Duration: " + str(end - start))



if __name__ == "__main__":
    main()
