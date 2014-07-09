import logging
import re
from cassandra.cluster import Cluster
from core.engine.engine_configuration import EngineConfiguration


class Engine(object):
    def __init__(self):
        self.configuration = None
        self.cluster = None
        self.session = None

    @staticmethod
    def create_engine(connection_string):
        engine = Engine()

        engine.create_config(connection_string)
        engine.create_cluster()
        engine.create_session()

        return engine

    def create_config(self, connection_string):
        self.configuration = EngineConfiguration()

        match = re.search('cassandra://([^/:]+)(:\d+)?/([^?/]+)', connection_string)
        groups = len(match.groups())

        if groups != 3:
            raise AttributeError('Invalid connection string %s' % connection_string)

        self.configuration.contact_point = match.group(1)

        if match.group(2):
            self.configuration.port = int(match.group(2).replace(':', ''))

        self.configuration.keyspace_name = match.group(3)

    def create_cluster(self):
        if self.configuration.port is None:
            self.cluster = Cluster([self.configuration.contact_point])
        else:
            self.cluster = Cluster([self.configuration.contact_point], port=self.configuration.port)

    def create_session(self):
        self.session = self.cluster.connect()

    def execute_query(self, query):
        logger = logging.getLogger(__name__)
        logger.debug('Executing query %s' % query)
        return self.session.execute(query)
