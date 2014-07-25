import random
from cassandra.cluster import Cluster
import time


def main():
    master_items = 10000
    slave_items = 1000
    density = 10
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    session.execute('DROP KEYSPACE relations_test;')
    session.execute("CREATE KEYSPACE relations_test WITH REPLICATION = { 'class': 'SimpleStrategy', 'replication_factor': 1 };")
    session.execute("USE relations_test;")
    session.execute("CREATE TABLE relations_users (id text, name text, surname text, item_id text, item_name text, item_price text, PRIMARY KEY(id, item_id));")
    session.execute("CREATE TABLE relations_items (id text, name text, price text, PRIMARY KEY(id));")
    session.execute("CREATE TABLE relations_join (user_id text, item_id text, PRIMARY KEY(user_id, item_id));")
    session.execute("CREATE TABLE relations_users_items (user_id text, item_id text, item_name text, item_price text, PRIMARY KEY(user_id, item_id));")

    for i in range(0, master_items):
        relations = random.randint(0, density + 1)

        for j in range(0, relations):
            item_id = random.randint(0, slave_items)

            join_values = (str(i), str(item_id))
            users_values = (str(i), 'Name: ' + str(i), 'Surname: ' + str(i), str(item_id), 'Name: ' + str(item_id), 'Price: ' + str(item_id))
            users_items_values = (str(i), str(item_id), 'Name: ' + str(item_id), 'Price: ' + str(item_id))

            session.execute("INSERT INTO relations_join (user_id, item_id) VALUES ('%s', '%s');" % join_values)
            session.execute("INSERT INTO relations_users (id, name, surname, item_id, item_name, item_price) VALUES('%s', '%s', '%s', '%s', '%s', '%s');" % users_values)
            session.execute("INSERT INTO relations_users_items (user_id, item_id, item_name, item_price) VALUES ('%s', '%s', '%s', '%s');" % users_items_values)

    for i in range(0, slave_items):
        session.execute("INSERT INTO relations_items (id, name, price) VALUES('%s', '%s', '%s');" % (str(i), 'Name: ' + str(i), 'Price: ' + str(i)))

    before = time.time()

    for i in range(0, master_items):
        session.execute("SELECT * FROM relations_users WHERE id = '%s';" % str(i))

    print 'Denormalized fields execution ended in %s s' % str(time.time() - before)

    before = time.time()

    for i in range(0, master_items):
        session.execute("SELECT * FROM relations_users WHERE id = '%s';" % str(i))
        session.execute("SELECT * FROM relations_users_items WHERE user_id = '%s';" % str(i))

    print 'Denormalized table execution ended in %s s' % str(time.time() - before)

    before = time.time()

    for i in range(0, master_items):
        session.execute("SELECT * FROM relations_users WHERE id = '%s';" % str(i))
        item_ids = session.execute("SELECT * FROM relations_join WHERE user_id = '%s';" % str(i))

        for item_id in item_ids:
            session.execute("SELECT * FROM relations_items WHERE id = '%s';" % item_id.item_id)

    print 'Normalized execution ended in %s s' % str(time.time() - before)

    session.execute("TRUNCATE relations_users_items;")
    session.execute("TRUNCATE relations_join;")
    session.execute("TRUNCATE relations_items;")
    session.execute("TRUNCATE relations_users;")
    session.execute('DROP KEYSPACE relations_test;')

if __name__ == '__main__':
    main()
