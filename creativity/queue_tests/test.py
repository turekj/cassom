from cassandra.cluster import Cluster
import time
from time_uuid import TimeUUID


def main():
    items = 10000
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    #session.execute('DROP KEYSPACE queue_test;')
    session.execute("CREATE KEYSPACE queue_test WITH REPLICATION = { 'class': 'SimpleStrategy', 'replication_factor': 1 };")
    session.execute("USE queue_test;")
    session.execute("CREATE TABLE queue (id text, event_at timeuuid, payload text, PRIMARY KEY(id, event_at));")

    timeuuid = TimeUUID.with_utcnow()

    for i in range(0, items - 1):
        timeuuid = TimeUUID.with_utcnow()
        query = "INSERT INTO queue (id, event_at, payload) VALUES ('queue_1', " + str(timeuuid) + ", 'payload" + str(i) + "');"
        session.execute(query)
        session.execute("DELETE FROM queue WHERE id = 'queue_1' AND event_at = " + str(timeuuid) + ";")

    query = "INSERT INTO queue (id, event_at, payload) VALUES ('queue_1', " + str(TimeUUID.with_utcnow()) + ", 'payload10000');"
    session.execute(query)

    before = time.time()
    result = session.execute("SELECT * FROM queue WHERE id = 'queue_1' LIMIT 1;")
    print 'Not enqueued executed in %s ms' % str(time.time() - before)
    print 'Result: %s' % str(result[0])

    before = time.time()
    result = session.execute("SELECT * FROM queue WHERE id = 'queue_1' AND event_at > " + str(timeuuid) + " LIMIT 1;")
    print 'Enqueued executed in %s ms' % str(time.time() - before)
    print 'Result: %s' % str(result[0])

    session.execute('DROP KEYSPACE queue_test;')

if __name__ == '__main__':
    main()
