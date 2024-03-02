package fr.inalco.m2.a2023;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Map;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Student extends User {
	
    // Constants to easily change file paths
    private static final String TEACHER_ANSWERS_FILE_PATH = "/home/dell/eclipse-workspace/projectVO/src/fr/inalco/m2/a2023/teacher_answers_";
   
    int correctAnswer = 0; //initialize a counter for the correct answer counting

    // Constructor
    public Student(String username, String password, String firstName, String lastName) {
        super(username, password, firstName, lastName);
    }

    // Method for a student to take an exercise
    public void takeExercise(Map<String, Exercise> exercises) {
        Scanner inputScanner = new Scanner(System.in);

        while (true) {
            // Get exercise metadata to find the right exercise by language and level
            System.out.println("Enter exercise metadata for the language and level you wish for (languageCode:level):");
            String metadata = inputScanner.nextLine();
            String[] metadataParts = metadata.split(":");

            if (metadataParts.length == 2) {
                String languageCode = metadataParts[0];
                int level = Integer.parseInt(metadataParts[1]);

                // Check if the exercise exists in the map
                Exercise exercise = exercises.get(languageCode + "_" + level);

                // If there's an instruction let the student take the exercise
                if (checkSavedInstructions(languageCode, level)) {
                    takeAnswersFromFile(languageCode, level);
                } else {
                    System.out.println("Exercise not found for the given metadata.");
                }
            } else {
                System.out.println("Invalid format for exercise metadata.");
            }

            // Ask the student if they want to take another exercise
            System.out.println("Do you want to take another exercise? (yes/no):");
            String anotherExercise = inputScanner.nextLine().toLowerCase();

            if (!anotherExercise.equals("yes")) {
                System.out.println("OK! You did a good job :-)");
                break; 
            }
        }
    }

    // Check if the instructions for the exercise are saved
    private boolean checkSavedInstructions(String languageCode, int level) {
        try (BufferedReader reader = new BufferedReader(new FileReader("/home/dell/eclipse-workspace/projectVO/src/fr/inalco/m2/a2023/instructions_" + languageCode + "_" + level + ".txt"))) {
            String line;
            while ((line = reader.readLine()) != null) {
                // Check if the line starts with the given metadata
                if (line.startsWith(languageCode + ":" + level)) {
                    return true;
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return false;
    }

    // Takes answers from the file where they are saved with the instructions
    private void takeAnswersFromFile(String languageCode, int level) {
        try (BufferedReader reader = new BufferedReader(new FileReader(TEACHER_ANSWERS_FILE_PATH + languageCode + "_" + level + ".txt"))) {
            String line;
            boolean printInstructions = false;

            // Read the file and print exercise when the given metadata is encountered
            while ((line = reader.readLine()) != null) {
                if (line.startsWith(languageCode + ":" + level)) {
                    printInstructions = true;
                    System.out.println(line);  // Print exercise description
                    System.out.println("Please type in your answers:");
                } else if (line.isEmpty() && printInstructions) {
                    break;
                } else if (printInstructions) {
                    evaluateAnswer(line);
                }
            }

            // Print the final score after finishing the exercise
            printFinalScore();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Evaluate the student's answer given the answers provided by the teacher
    private void evaluateAnswer(String teacherAnswer) {
        Scanner inputScanner = new Scanner(System.in);

        // Extract instruction number, question part, and answer
        String[] parts = teacherAnswer.split(":");
        if (parts.length == 2) {
            String instructionNumber = parts[0].trim();
            String question = parts[1].trim();
            String answer = extractCorrectAnswer(question);

            // Print the exercise
            if (!question.startsWith("[1-9]")) {
                System.out.println(instructionNumber);
            }
            System.out.print("Input answer: ");
            String studentAnswer = inputScanner.nextLine();

            // Checks if the student's answer is identical to the right one and shows score after each response
            if (studentAnswer.trim().equalsIgnoreCase(answer)) {
                System.out.println("Correct!");
                correctAnswer++; // adds +1 to the score if correct 
                System.out.println("Current score: " + correctAnswer);
            } else {
                System.out.println("Incorrect! Correct answer: " + answer); // shows right answer if false
                System.out.println("Current score: " + correctAnswer);
            }
        }
    }

    // Extract the answer part from the question
    private String extractCorrectAnswer(String question) {
        // REGEX finds the answer that is situated between '#' symbols
        Pattern pattern = Pattern.compile("#(.*?)#");
        Matcher matcher = pattern.matcher(question);

        if (matcher.find()) {
            return matcher.group(1).trim();
        }

        // Return the whole question if no match is found
        return question.trim();
    }

    // Print final score after the end of the exercise
    private void printFinalScore() {
        System.out.println("Final Score: " + correctAnswer);
    }
}

