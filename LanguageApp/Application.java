package fr.inalco.m2.a2023;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class Application {
    // Constants to easily change file paths 
    private static final String TEACHER_ACCOUNTS_FILE_PATH = "/home/dell/eclipse-workspace/projectVO/src/fr/inalco/m2/a2023/teacher_accounts.txt";
    private static final String STUDENT_ACCOUNTS_FILE_PATH = "/home/dell/eclipse-workspace/projectVO/src/fr/inalco/m2/a2023/student_accounts.txt";

    // Maps for storing user and exercise information
    private static Map<String, User> teacherAccounts = new HashMap<>();
    private static Map<String, User> studentAccounts = new HashMap<>();
    private static Map<String, Exercise> exercises = new HashMap<>();
    
    // Scanner for user input
    public static Scanner scanner = new Scanner(System.in);

    // Main point for the execution of the app
    public static void main(String[] args) {
    	// Loading teachers' and students' user informations
        loadUsernamesFromFile(TEACHER_ACCOUNTS_FILE_PATH, teacherAccounts);
        loadUsernamesFromFile(STUDENT_ACCOUNTS_FILE_PATH, studentAccounts);

        // Print welcome messages and options for the user to choose from
        System.out.println("Welcome to my app!");
        System.out.println("Please choose an option :");
        System.out.println("1. Create a teacher account");
        System.out.println("2. Create a student account");
        System.out.println("3. Login");
        System.out.println("4. Quit");
        System.out.print("Enter your number of choice (1/2/3/4): ");
        int choice = scanner.nextInt(); // Input number to select option
        scanner.nextLine();

        // Act according to users' choice
        switch (choice) {
            case 1:
            	// Creates a new teacher account
                createAccount("Teacher", teacherAccounts);
                break;
            case 2:
            	// Creates a new student account
                createAccount("Student", studentAccounts);
                break;
            case 3:
              while (true) {
            	// Logins either as a teacher or a student
                System.out.println("Teacher or student? Type in your role please");
                String role = scanner.nextLine();
                // Asks for the right login information
                System.out.println("Username:");
                String username = scanner.nextLine();
                System.out.println("Password:");
                String password = scanner.nextLine();

                User loggedInUser = null;

                // Checks if the username exists for the right role
                if ("Teacher".equalsIgnoreCase(role) && teacherAccounts.containsKey(username)) {
                    loggedInUser = teacherAccounts.get(username);
                } else if ("Student".equalsIgnoreCase(role) && studentAccounts.containsKey(username)) {
                    loggedInUser = studentAccounts.get(username);
                }

                // If login is successful (user exists and matches the password) prints a welcome message
                if (loggedInUser != null && loggedInUser.getPassword().equals(password)) {
                    System.out.println("Hello " + role.toLowerCase() + " " + loggedInUser.getFirstName() + " " + loggedInUser.getLastName() + ", you are logged in!");

                    if (role.equalsIgnoreCase("Teacher")) {
                        // Lets you submit an exercise if you're a teacher
                        ((Teacher) loggedInUser).submitExercise(exercises);
                    } else {
                        // Lets you take an exercise if you're a student
                        ((Student) loggedInUser).takeExercise(exercises);
                    }
                } else {
                    // If role is not recognized or wrong login, lets you try again if you wish
                	System.out.println("Not recognized. Do you want to try again? (yes/no):");
                	String retryResponse = scanner.nextLine().toLowerCase();

                	if ("yes".equals(retryResponse)) {
                	    continue;
                	} else {
                	    break;
                	}
                }
              }
            case 4:
            	// If you don't want to do anything
                System.out.println("See you next time!");
                break;
            default:
            	// If invalid choice
                System.out.println("Invalid choice. See you next time!");
                break;
        }

        scanner.close();
    }

    // Method for creating a new account 
    private static void createAccount(String role, Map<String, User> accounts) {
        System.out.println("Creating a " + role + " account:");
        System.out.println("First Name:");
        String firstName = scanner.nextLine();
        System.out.println("Last Name:");
        String lastName = scanner.nextLine();
        System.out.println("Username:");
        String username = scanner.nextLine();
        System.out.println("Password:");
        String password = scanner.nextLine();

        // Create a user according to the role 
        User newUser;       
        if (role.equalsIgnoreCase("Teacher")) {
            newUser = new Teacher(username, password, firstName, lastName);
        } else if (role.equalsIgnoreCase("Student")) {
            newUser = new Student(username, password, firstName, lastName);
        } else {
            System.out.println("I don't recognize this role!");
            return;
        }

        // Add the user to the map
        accounts.put(username, newUser);

        // Save the new account to either teacher or student file based on the role
        String accountsFilePath;

        if (role.equalsIgnoreCase("Teacher")) {
            accountsFilePath = TEACHER_ACCOUNTS_FILE_PATH;
        } else if (role.equalsIgnoreCase("Student")) {
            accountsFilePath = STUDENT_ACCOUNTS_FILE_PATH;
        } else {
            System.out.println("Unexpected role. Unable to determine account file path.");
            return;
        }
        // Write the new account in the form username:password:firstname:lastname
        try (FileWriter writer = new FileWriter(accountsFilePath, true)) {
            writer.write(newUser.getUsername() + ":" + newUser.getPassword() + ":" +
                    newUser.getFirstName() + ":" + newUser.getLastName() + "\n");
            System.out.println(role + " account created successfully!");

            // After creating an account ask if the user wants to quit or login
            System.out.println("Do you want to log in or quit the app? (login/quit):");
            String response = scanner.nextLine().toLowerCase();
            if ("login".equals(response)) {
                login();
            } else if ("quit".equals(response)) {
                System.out.println("See you next time!");
            } else {
                System.out.println("Invalid choice. See you next time!");
            }
        } catch (IOException e) {
            System.out.println("Error saving user information to file: " + accountsFilePath);
        }
    }
    
    // Method that allows to login
    private static void login() {
        System.out.println("Teacher or student? Type in your role please");
        String role = scanner.nextLine();

        System.out.println("Username:");
        String username = scanner.nextLine();
        System.out.println("Password:");
        String password = scanner.nextLine();

        boolean loginSuccessful = false;
        String firstName = "";
        String lastName = "";

        // If username matches the password it finds the users' first and last name
        if ("Teacher".equalsIgnoreCase(role)) {
            loginSuccessful = login(username, password, teacherAccounts);
            if (loginSuccessful) {
                Teacher teacher = (Teacher) teacherAccounts.get(username);
                firstName = teacher.getFirstName();
                lastName = teacher.getLastName();
            }
        } else if ("Student".equalsIgnoreCase(role)) {
            loginSuccessful = login(username, password, studentAccounts);
            if (loginSuccessful) {
                Student student = (Student) studentAccounts.get(username);
                firstName = student.getFirstName();
                lastName = student.getLastName();
            }
        }

     // If everything is successful shows a welcome message and lets the user do its' role (submit or take exercise)
        if (loginSuccessful) {
            if (role.equalsIgnoreCase("Teacher")) {
                Teacher teacherUser = new Teacher(username, password, firstName, lastName);
                System.out.println("Hello teacher " + teacherUser.getFirstName() + " " + teacherUser.getLastName() + ", you are logged in!");
                teacherUser.submitExercise(exercises);
            } else if (role.equalsIgnoreCase("Student")) {
                Student studentUser = new Student(username, password, firstName, lastName);
                System.out.println("Hello student " + studentUser.getFirstName() + " " + studentUser.getLastName() + ", you are logged in!");
                studentUser.takeExercise(exercises);
            }
        } else {
            System.out.println("Role not recognized or incorrect login information. Do you want to try again? (yes/no):");
            String response = scanner.nextLine().toLowerCase();
            if (!response.equals("yes")) {
                System.out.println("See you next time!");
            } else {
                login();
            }
        }

    }

    // Method for checking the login information
    private static boolean login(String username, String password, Map<String, ? extends User> accounts) {
        if (accounts.containsKey(username)) {
            User user = accounts.get(username);
            return user.getPassword().equals(password);
        }
        return false;
    }

    // Method for loading information from a file to the map
    private static void loadUsernamesFromFile(String filename, Map<String, User> accounts) {
        try (Scanner fileScanner = new Scanner(new File(filename))) {
            while (fileScanner.hasNextLine()) {
                String line = fileScanner.nextLine(); //for each line
                String[] parts = line.split(":"); // : is a separator
                if (parts.length == 4) {
                	// extract the right information
                    String username = parts[0];
                    String password = parts[1];
                    String firstName = parts[2];
                    String lastName = parts[3];

                    // Create a teacher or student object
                    User user;
                    if (filename.contains("teacher")) {
                        user = new Teacher(username, password, firstName, lastName);
                    } else if (filename.contains("student")) {
                        user = new Student(username, password, firstName, lastName);
                    } else {
                        System.out.println("I can't determine the user type.");
                        continue; 
                    }
                    // Add user to the map
                    accounts.put(username, user);
                }
            }
        } catch (IOException e) {
            System.out.println("Error when loading information from this file: " + filename);
        }
    }

    // Method to save a new account to a file according to role
    private static void saveAccountToFile(String role, User newUser) {
        String accountsFilePath;

        if (role.equalsIgnoreCase("Teacher")) {
            accountsFilePath = TEACHER_ACCOUNTS_FILE_PATH;
        } else if (role.equalsIgnoreCase("Student")) {
            accountsFilePath = STUDENT_ACCOUNTS_FILE_PATH;
        } else {
            System.out.println("I don't recognize the role and can't find the path.");
            return;
        }
        // Write the new account in the form username:password:firstname:lastname
        try (FileWriter writer = new FileWriter(accountsFilePath, true)) {
            writer.write(newUser.getUsername() + ":" + newUser.getPassword() + ":" +
                    newUser.getFirstName() + ":" + newUser.getLastName() + "\n");
            System.out.println(role + " account created successfully!");

            // Ask if the user wants to login or quit
            offerLoginOrQuit();
        } catch (IOException e) {
            System.out.println("Error saving user information to this file: " + accountsFilePath);
        }
    }

    // Method to offer login or quit options after creating an account
    private static void offerLoginOrQuit() {
        System.out.println("Do you want to log in or quit the app? (login/quit):");
        String response = scanner.nextLine().toLowerCase();
        if ("login".equals(response)) {
            login();
        } else if ("quit".equals(response)) {
            System.out.println("See you next time!");
        } else {
            System.out.println("Invalid choice. See you next time!");
        }
    }
}
