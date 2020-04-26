import time
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
##

def main():
    start = time.time()
    # unit_test = UnitTests()
    # paper_example_test = PaperExample()
    random_test = RandomTestsGenerator()
    end = time.time()
    print("Execution time: " + str(end - start))


if __name__ == "__main__":
    main()
