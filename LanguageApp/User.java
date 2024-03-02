package fr.inalco.m2.a2023;

public class User {
	// Instancing variables
    private String username;
    private String password;
    private String firstName;
    private String lastName;

    // Constructors
    public User(String username, String password, String firstName, String lastName) {
        this.username = username;
        this.password = password;
        this.firstName = firstName;
        this.lastName = lastName;
    }

    // Getters

    public String getUsername() {
        return username;
    }

    public String getPassword() {
        return password;
    }

    public String getFirstName() {
        return firstName;
    }

    public String getLastName() {
        return lastName;
    }
}

