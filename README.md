# TAO

## Introduction

The subject of this project is a read-optimized graph data store, called TAO (The Associations and Objects), which was implemented by Facebook and can be found [here](https://www.usenix.org/system/files/conference/atc13/atc13-bronson.pdf). TAO is a system that relies heavily on caching to serve large numbers of low-latency queries. It implements a graph data model in which nodes are identified by fixed-length persistent identifiers (64-bit integers) and it encodes a specific mapping of its graph model to persistent storage and takes responsibility for persistence. In this data model, the main components are objects and associations. Associations naturally model actions that can happen at most once or record state transitions, such as the acceptance of an event invitation, while repeatable actions are better represented as objects. TAO also exposes a minimal API that does not support a complete set of graph queries, but provides sufficient expressiveness to handle most application needs while allowing a scalable and efficient implementation.

## Implementation

This is intended to be a reference implementation (on which future implementations can be based for better understanding of the requirements and the components of TAO) rather than an experimental implementation, thus Python was the chosen language as it enhances readability. This implementation includes the storage, cache, caching policy and API aspects of TAO while it does not involve the distributed system aspect of it. Following as close as possible TAO the cache eviction policy is LRU. Regarding the storage SQLite is being used instead of SQL.

## Installation

Requirements: Python 3.7
Instructions:

1. Make sure you have the expected requirements
2. Clone this repository to your machine using `git clone https://github.com/tflpd/TAO.git`

## Usage

- Navigate in the source folder using `cd TAO/src/`
- Start the execution of the application using `python3 TAO.py`

The user can decide one of the three following modes of execution:

- Unit Tests. This will execute a combination of simple unit tests to ensure basic functionality
- Paper Example. This will create the sample graph that is shown in paper's _Figure 1_ and will execute on it some queries. The reader may take a look at the natural language explanation of each query that can be found as a comment above it
- Random Tests Generator. This will generate and execute a random workload based on the configuration of the different tunable knobs. Currently, the distribution of the requests is based on the real life relative frequencies of client requests to TAO from all Facebook products that can be found in paper's _Figure 3_

In order to change the mode of execution the user has to comment/uncomment the respective lines in the `TAO.py` file. This should be fairly simple, however it is not elegant and will be changed soon to be requested as an input from the user.

There exist the following tunable knobs that can be found in the `flags.py` file and can be modified according to the following instructions (here you see their default values):

_Flags that enable logging and debugging printing
More specifically this turns it on_
`DEBUG_FLAG = False`
_And this provides more details than just their keys for the objects and more detailed messages generally_
`VERBOSE_FLAG = False`
_The number of operations that will be executed if the developer has chosen to run the randomly generated test_
`NUM_OPS = 100000`
_Labels for the weights below - DO NOT CHANGE THEM_
`write_reqs = ["assoc_add", "assoc_del", "obj_add", "obj_update", "obj_delete"]`
_Weights/probabilities for each of the above write operations. A developer can change their values to provide a different distribution of operations in the randomly generated test_
`write_reqs_weights = [52.5, 8.3, 16.5, 20.7, 2]`
_Labels for the weights below - DO NOT CHANGE THEM_
`read_reqs = ["assoc_get", "assoc_range", "assoc_time_range", "assoc_count", "obj_get"]`
_Weights/probabilities for each of the above read operations. A developer can change their values to provide a different distribution of operations in the randomly generated test_
`read_reqs_weights = [15.7, 40.9, 2.8, 11.7, 28.9]`
_Size of the objects TAO cache - counted in distinct elements_
`OBJECTS_CACHE_SIZE = 100`
_Size of the associations lists TAO cache - counted in distinct elements_
`ASSOCIATIONS_CACHE_SIZE = 100`
_Size of the associations counts TAO cache - counted in distinct elements_
`ASSOCIATIONS_COUNTS_CACHE_SIZE = 100`
_Flag to be used for debugging. When set to false the random tests generator will provide the same random sequence of operations. When set to true the sequence will be random_
`RANDOM = False`
