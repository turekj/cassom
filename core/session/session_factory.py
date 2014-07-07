from core.session.cluster_factory import ClusterFactory


class SessionFactory(object):
    def __init__(self, config=None):
        self.config = config
        self.cluster_factory = ClusterFactory(config)
        self.session = None

    def create_session(self):
        return self.cluster_factory.create_cluster().connect()
