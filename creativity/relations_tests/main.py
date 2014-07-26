import random
from cassandra.cluster import Cluster
import time


def main():
    master_items = 10000
    slave_items = 1000
    density = 25
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    #session.execute('DROP KEYSPACE relations_test;')
    session.execute("CREATE KEYSPACE relations_test WITH REPLICATION = { 'class': 'SimpleStrategy', 'replication_factor': 1 };")
    session.execute("USE relations_test;")
    session.execute("CREATE TABLE relations_users (id text, name text, surname text, item_id text, item_name text, item_price text, PRIMARY KEY(id, item_id));")
    session.execute("CREATE TABLE relations_items (id text, name text, price text, PRIMARY KEY(id));")

    item_ids_for_users = {}

    for i in range(0, master_items):
        item_ids_for_users[i] = []
        relations = random.randint(0, density + 1)

        for j in range(0, relations):
            item_ids_for_users[i].append(random.randint(0, slave_items))

    before = time.time()

    for i in range(0, master_items):
        for j in range(0, len(item_ids_for_users[i])):
            item_id = str(item_ids_for_users[i][j])
            users_values = (str(i), 'Name: ' + str(i), 'Surname: ' + str(i), item_id, 'Name: ' + item_id, 'Price: ' + item_id)
            session.execute("INSERT INTO relations_users (id, name, surname, item_id, item_name, item_price) VALUES('%s', '%s', '%s', '%s', '%s', '%s');" % users_values)

    for i in range(0, slave_items):
        items_values = (str(i), 'Name: ' + str(i), 'Price: ' + str(i))
        session.execute("INSERT INTO relations_items (id, name, price) VALUES('%s', '%s', '%s');" % items_values)

    print 'Inserting fields ended in %s s' % str(time.time() - before)

    session.execute("TRUNCATE relations_items;")
    session.execute("TRUNCATE relations_users;")
    session.execute('DROP KEYSPACE relations_test;')

if __name__ == '__main__':
    main()
