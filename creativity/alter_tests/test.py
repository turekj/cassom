from cassandra.cluster import Cluster
import time
from cassandra.query import BatchStatement
import mysql.connector


def main():
    items = 100000
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    #session.execute('DROP KEYSPACE alter_test;')
    session.execute(
        "CREATE KEYSPACE alter_test WITH REPLICATION = { 'class': 'SimpleStrategy', 'replication_factor': 1 };")
    session.execute("USE alter_test;")
    session.execute("CREATE TABLE alter_users (id text, name text, surname text, PRIMARY KEY(id));")

    before = time.time()

    batch = BatchStatement()

    for i in range(0, items):
        users_values = (str(i), 'Name: ' + str(i), 'Surname: ' + str(i))
        batch.add("INSERT INTO alter_users (id, name, surname) VALUES('%s', '%s', '%s');" % users_values)

        if i > 0 and i % 50000 == 0:
            session.execute(batch)
            batch = BatchStatement()

    session.execute(batch)

    print 'Inserting fields ended in %s s' % str(time.time() - before)

    before = time.time()

    session.execute("ALTER TABLE alter_users ADD email text;")

    print 'Altered table in %s s' % str(time.time() - before)

    session.execute("TRUNCATE alter_users;")
    session.execute('DROP KEYSPACE alter_test;')

    test_mysql(items)


def test_mysql(items):
    conn = mysql.connector.Connect(host='127.0.0.1', user='root', password='', database='alter_tests')

    c = conn.cursor()

    before = time.time()

    for i in range(0, items):
        users_values = ('Name: ' + str(i), 'Surname: ' + str(i))
        c.execute("INSERT INTO users (name, surname) VALUES ('%s', '%s');" % users_values)

        if i > 0 and i % 50000 == 0:
            print 'processed ' + str(i)
            conn.commit()

    conn.commit()

    print 'Inserting fields ended in %s s' % str(time.time() - before)

    before = time.time()

    c.execute("ALTER TABLE users ADD email VARCHAR(255);")
    conn.commit()

    print 'Altered table in %s s' % str(time.time() - before)

    c.close()


if __name__ == '__main__':
    main()
