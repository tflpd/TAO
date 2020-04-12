class Node:
    def __init__(self, objects_cache_size, associations_lists_cache_size, associations_counts_cache_size):
        self.obj_size = objects_cache_size
        self.assoc_lists_size = associations_lists_cache_size
        self.assoc_counts_size = associations_counts_cache_size
