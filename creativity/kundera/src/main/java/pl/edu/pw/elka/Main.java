package pl.edu.pw.elka;

import com.datastax.driver.core.Cluster;
import com.datastax.driver.core.Session;
import org.apache.commons.lang.time.StopWatch;

import java.util.*;

public class Main {
    private static final int MAX_USERS_PERSISTED = 10000;
    private static final int MAX_USERS_FETCHED = 10000;
    private static final int MAX_ITEMS = 5000;
    private static final int MAX_ITEMS_PER_WISHLIST = 11;

    public static void main(String[] args) {
        Main main = new Main();
        main.persistUsersKundera();
    }

    private void persistUsersKundera() {
        List<Item> items = createItems();
        List<User> users = createUsers(items);

        Cluster cluster = Cluster.builder().addContactPoint("127.0.0.1").build();
        Session session = cluster.connect();
        //session.execute("DROP KEYSPACE performance_test;");
        session.execute("CREATE KEYSPACE performance_test WITH REPLICATION = { 'class' : 'SimpleStrategy', " +
                "'replication_factor' : 3 };");
        session.execute("CREATE TABLE performance_test.users (userId text PRIMARY KEY, name text, surname text);");
        session.execute("CREATE TABLE performance_test.wishlist (userId text, wishlistId text, name text, " +
                "price text, PRIMARY KEY(userId, wishlistId));");
        session.execute("CREATE TABLE performance_test.items (itemId text PRIMARY KEY, name text, price text, " +
                "description text);");

        StopWatch watch = new StopWatch();
        watch.start();

        String usersQuery = "INSERT INTO performance_test.users (userId, name, surname) VALUES";
        String itemsQuery = "INSERT INTO performance_test.items (itemId, name, price, description) VALUES";
        String wishlistQuery = "INSERT INTO performance_test.wishlist (userId, wishlistId, name, price) VALUES";

        for (User user : users) {
            session.execute(usersQuery + "('" + user.getUserId() + "','" + user.getName() + "','" + user.getSurname() + "');");

            for (Item item : user.getWishlistItems()) {
                session.execute(itemsQuery + "('" + item.getItemId() + "','" + item.getName() + "'," +
                        "'" + item.getPrice() + "','" + item.getDescription() + "');");
                session.execute(wishlistQuery + "('" + user.getUserId() + "','" + item.getItemId() + "'," +
                        "'" + item.getName() + "','" + item.getPrice() + "');");
            }
        }

        watch.split();

        System.out.println("Users persisted in: " + watch.getSplitTime() + "ms");

        watch.stop();

        Set<Integer> userIds = new HashSet<Integer>();
        Random random = new Random();

        for (int i = 0; i < MAX_USERS_FETCHED; ++i) {
            userIds.add(random.nextInt(MAX_USERS_PERSISTED));
        }

        Iterator<Integer> userIdIterator = userIds.iterator();

        watch.reset();
        watch.start();

        while (userIdIterator.hasNext()) {
            Integer id = userIdIterator.next();
            session.execute("SELECT * FROM performance_test.wishlist WHERE userId = '" + id.toString() + "';");
        }

        watch.split();

        System.out.println("Users fetched in: " + watch.getSplitTime() + "ms");

        session.execute("DROP KEYSPACE performance_test;");
        session.close();
        cluster.close();
    }

    private List<User> createUsers(List<Item> items) {
        StopWatch watch = new StopWatch();
        List<User> users = new ArrayList<User>();
        Random random = new Random();

        watch.start();

        for (int i = 0; i < MAX_USERS_PERSISTED; ++i) {
            User user = new User();
            user.setUserId("" + i);
            user.setName("Name of user: " + i);
            user.setSurname("Surname of user: " + i);

            int likedItems = random.nextInt(MAX_ITEMS_PER_WISHLIST);
            List<Integer> itemsToLike = new ArrayList<Integer>();

            for (int j = 0; j < likedItems; ++j) {
                int itemId = random.nextInt(MAX_ITEMS);

                if (!itemsToLike.contains(itemId)) {
                    itemsToLike.add(itemId);
                }
            }

            for (Integer itemId : itemsToLike) {
                Item item = items.get(itemId);
                user.getWishlistItems().add(item);
            }

            users.add(user);
        }

        watch.split();

        System.out.println("Users created in: " + watch.getSplitTime() + "ms");

        return users;
    }

    private List<Item> createItems() {
        StopWatch watch = new StopWatch();
        List<Item> items = new ArrayList<Item>();

        watch.start();

        for (int i = 0; i < MAX_ITEMS; ++i) {
            Item item = new Item();
            item.setItemId("" + i);
            item.setName("Item: " + i);
            item.setDescription("Description of item: " + i);
            item.setPrice("" + (i / 100.0f));
            items.add(item);
        }

        watch.split();

        System.out.println("Items created in: " + watch.getSplitTime() + "ms");

        return items;
    }
}
