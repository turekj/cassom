from cassandra.cluster import Cluster


class ClusterFactory(object):
    def __init__(self, config=None):
        self.config = config

    def create_cluster(self):
        return Cluster(self.config.contact_points)
