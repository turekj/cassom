import random
from cassandra.cluster import Cluster
import time


def main():
    master_items = 10000
    slave_items = 1000
    density = 5
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    #session.execute('DROP KEYSPACE migrations_test;')
    session.execute("CREATE KEYSPACE migrations_test WITH REPLICATION = { 'class': 'SimpleStrategy', 'replication_factor': 1 };")
    session.execute("USE migrations_test;")
    session.execute("CREATE TABLE migrations_users (id text, name text, surname text, item_id text, item_name text, item_price text, PRIMARY KEY(id, item_id));")
    session.execute("CREATE TABLE migrations_items (id text, name text, price text, PRIMARY KEY(id));")

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
            session.execute("INSERT INTO migrations_users (id, name, surname, item_id, item_name, item_price) VALUES('%s', '%s', '%s', '%s', '%s', '%s');" % users_values)

    for i in range(0, slave_items):
        items_values = (str(i), 'Name: ' + str(i), 'Price: ' + str(i))
        session.execute("INSERT INTO migrations_items (id, name, price) VALUES('%s', '%s', '%s');" % items_values)

    print 'Inserting fields ended in %s s' % str(time.time() - before)

    before = time.time()

    session.execute("ALTER TABLE migrations_items ADD color text;")
    session.execute("ALTER TABLE migrations_users ADD item_color text;")

    print 'Altered tables in %s s' % str(time.time() - before)

    before = time.time()

    for i in range(0, slave_items):
        items_update = ('Color: ' + str(i), str(i))
        session.execute("UPDATE migrations_items SET color = '%s' WHERE id = '%s';" % items_update)

    for i in range(0, master_items):
        migrations_users = session.execute("SELECT * FROM migrations_users WHERE id = '%s';" % str(i))

        for user in migrations_users:
            items = session.execute("SELECT * FROM migrations_items WHERE id = '%s';" % str(user.item_id))

            for item in items:
                users_update = (item.color, str(i), item.id)
                session.execute("UPDATE migrations_users SET item_color = '%s' WHERE id = '%s' AND item_id = '%s';" % users_update)

    print 'Updated data model ended in %s s' % str(time.time() - before)

    rand_user = random.randint(0, master_items)

    users = session.execute("SELECT * from migrations_users WHERE id = '%s';" % str(rand_user))

    for user in users:
        print 'Color for user %s is equal to %s' % (str(user.id), str(user.item_color))

    session.execute("TRUNCATE migrations_items;")
    session.execute("TRUNCATE migrations_users;")
    session.execute('DROP KEYSPACE migrations_test;')

if __name__ == '__main__':
    main()
