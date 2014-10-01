package pl.edu.pw.elka;

import javax.persistence.*;
import java.util.HashSet;
import java.util.Set;

@Entity
@Table(name = "items", schema = "kundera@cassandra_pu")
public class Item {
    @Id
    @Column(name="itemId")
    private String itemId;

    @Column(name="name")
    private String name;

    @Column(name="price")
    private String price;

    @Column(name="description")
    private String description;

    @ManyToMany(mappedBy="wishlistItems", fetch = FetchType.EAGER)
    private Set<User> wishingUsers = new HashSet<User>();

    public String getItemId() {
        return itemId;
    }

    public void setItemId(String itemId) {
        this.itemId = itemId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getPrice() {
        return price;
    }

    public void setPrice(String price) {
        this.price = price;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Set<User> getWishingUsers() {
        return wishingUsers;
    }

    public void setWishingUsers(Set<User> wishingUsers) {
        this.wishingUsers = wishingUsers;
    }
}
