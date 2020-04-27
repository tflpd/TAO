# Flags that enable logging and debugging printing
# More specifically this turns it on
DEBUG_FLAG = False
# And this provides more details thant just their keys for the objects and more detailed messages generally
VERBOSE_FLAG = False
# The number of operations that will be executed if the developer has chosen to run the randomly generated test
NUM_OPS = 100000
# Labels for the weights below - DO NOT CHANGE THEM
write_reqs = ["assoc_add", "assoc_del", "obj_add", "obj_update", "obj_delete"]
# Weights/probabilities for each of the above write operations. A developer can change their values to provide a
# different distribution of operations in the randomly generated test
write_reqs_weights = [52.5, 8.3, 16.5, 20.7, 2]
# Labels for the weights below - DO NOT CHANGE THEM
read_reqs = ["assoc_get", "assoc_range", "assoc_time_range", "assoc_count", "obj_get"]
# Weights/probabilities for each of the above read operations. A developer can change their values to provide a
# different distribution of operations in the randomly generated test
read_reqs_weights = [15.7, 40.9, 2.8, 11.7, 28.9]
# Size of the objects TAO cache - counted in distinct elements
OBJECTS_CACHE_SIZE = 100
# Size of the associations lists TAO cache - counted in distinct elements
ASSOCIATIONS_CACHE_SIZE = 100
# Size of the associations counts TAO cache - counted in distinct elements
ASSOCIATIONS_COUNTS_CACHE_SIZE = 100
# Flag to be used for debugging. When set to false thee random tests generator will provide the same random sequence
# of operations. When set to false the sequence will be random
RANDOM = False
