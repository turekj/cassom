package pl.edu.pw.elka;

import javax.persistence.*;
import java.util.HashSet;
import java.util.Set;

@Entity
@Table(name = "users", schema = "kundera@cassandra_pu")
public class User {
    @Id
    @Column(name = "userId")
    private String userId;

    @Column(name = "name")
    private String name;

    @Column(name = "surname")
    private String surname;

    @ManyToMany(cascade = CascadeType.ALL)
    @JoinTable(name = "wishlist", joinColumns = {@JoinColumn(name = "userId",
            referencedColumnName = "userId")},
            inverseJoinColumns = {@JoinColumn(name = "itemId", referencedColumnName = "itemId")},
            foreignKey = @ForeignKey(name = "userId_fk"), inverseForeignKey = @ForeignKey(name = "itemId_fk"))
    private Set<Item> wishlistItems = new HashSet<Item>();

    public String getUserId() {
        return userId;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getSurname() {
        return surname;
    }

    public void setSurname(String surname) {
        this.surname = surname;
    }

    public Set<Item> getWishlistItems() {
        return wishlistItems;
    }

    public void setWishlistItems(Set<Item> wishlistItems) {
        this.wishlistItems = wishlistItems;
    }
}
