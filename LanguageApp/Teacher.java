package fr.inalco.m2.a2023;

import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

public class Teacher extends User {
	
    // Constants to easily change file paths 
    private static final String INSTRUCTIONS_FILE_PATH = "/home/dell/eclipse-workspace/projectVO/src/fr/inalco/m2/a2023/instructions_";
    private static final String TEACHER_ANSWERS_FILE_PATH = "/home/dell/eclipse-workspace/projectVO/src/fr/inalco/m2/a2023/teacher_answers_";

	// Constructor
    public Teacher(String username, String password, String firstName, String lastName) {
        super(username, password, firstName, lastName);
    }
    
    // Method for submitting an exercise if you're a teacher
    public void submitExercise(Map<String, Exercise> exercises) {
        Scanner inputScanner = new Scanner(System.in);

        // Loop to allow the teacher to submit more than one exercise
        while (true) {
            // Ask for the metadata in the correct order 
            System.out.println("Enter exercise metadata (languageCode:level:pointsPerCorrectAnswer:necessaryPoints):");
            String metadata = inputScanner.nextLine();
            String[] metadataParts = metadata.split(":");

            if (metadataParts.length == 4) {
            	// Extract metadata
                String languageCode = metadataParts[0];
                int level = Integer.parseInt(metadataParts[1]);
                int pointsPerCorrectAnswer = Integer.parseInt(metadataParts[2]);
                int necessaryPoints = Integer.parseInt(metadataParts[3]);

                // Ask what type of exercise he wants to create 
                System.out.println("Enter exercise type (verb conjugation OR synonyms):");
                String exerciseType = inputScanner.nextLine();

                // Create and store the exercise
                Exercise exercise = new Exercise(languageCode, level, pointsPerCorrectAnswer, necessaryPoints,
                        new ArrayList<>(), new ArrayList<>(), exerciseType, "", "");

                // Make sure the lists are initialized
                exercise.setInstructions(new ArrayList<>());
                exercise.setAnswers(new ArrayList<>());

                exercises.put(languageCode + "_" + level, exercise);

                // Initialize variables needed for the verb conjugation
                String verb = "";
                String tense = "";

                // Verb conjugation will need some precision that we will ask
                if ("verb conjugation".equalsIgnoreCase(exerciseType)) {
                    // Ask for the verb
                    System.out.println("Enter the verb:");
                    verb = inputScanner.nextLine();

                    // Ask for the tense
                    System.out.println("Enter the tense:");
                    tense = inputScanner.nextLine();

                    int instructionNumber = 1;
                    List<String> instructions = new ArrayList<>();
                    List<String> answers = new ArrayList<>();  // Store answers in a new list

                    // Print the form in which the exercise needs to be created
                    System.out.println("Enter the correct conjugation for the verb in the specified tense, the answer part should be between the '#', type 'done' when finished:");
                    String input;
                    while (!(input = inputScanner.nextLine()).equalsIgnoreCase("done")) { // ends when done is typed
                        // Shows each question of the exercise with an order number and replaces the answer with 3 dots
                        System.out.println(instructionNumber + ". " + input.replaceAll("#.*#", "..."));

                        // Replaces the answer part by 3 dots
                        instructions.add(input.replaceAll("#.*#", "..."));

                        // Takes the answer part and puts it in the list
                        answers.add(input);

                        instructionNumber++; // iterates the order number for each question of the exercise
                    }

                    // Add instructions and answers to the exercise
                    exercise.setInstructions(instructions);
                    exercise.setAnswers(answers);

                    // Save instructions and answers to their files
                    saveInstructionsToFile(languageCode, level, pointsPerCorrectAnswer, necessaryPoints, verb, tense, instructions);
                    saveTeacherInputAndAnswers(languageCode, level, pointsPerCorrectAnswer, necessaryPoints, verb, tense, instructions, answers);
                } else if ("synonyms".equalsIgnoreCase(exerciseType)) {
                    // To be added in the future... sorry !  :)
                    // The logic would be very similar, gives a word and its' synonym between #
                    System.out.println("Sorry, exercise type not available at the moment :(");
                    System.out.println("Do you want to try another exercise type? (yes/no):");
                    String tryAgain = inputScanner.nextLine().toLowerCase();
                    if (tryAgain.equals("yes")) {
                        continue; // try creating another exercise
                    } else {
                        return;
                    }
                } else {
                    System.out.println("Exercise type not recognized.");

                    // Ask if the teacher wants to try again
                    System.out.println("Do you want to try again? (yes/no):");
                    String tryAgain = inputScanner.nextLine().toLowerCase();
                    if (tryAgain.equals("yes")) {
                        continue;
                    } else {
                    System.out.println("See you next time!");

                        return;
                    }
                }

                System.out.println("Exercise submitted successfully!"); // if all goes well
            } else {
                System.out.println("Invalid input format for exercise metadata.");
            }

            // Ask the teacher if they want to submit another exercise
            System.out.println("Do you want to submit another exercise? (yes/no):");
            String anotherExercise = inputScanner.nextLine().toLowerCase();

            if (!anotherExercise.equals("yes")) {
                System.out.println("See you next time!");
                break; 
            }
        }
    }

    // Save a file only with the instructions
	private void saveInstructionsToFile(String languageCode, int level, int pointsPerCorrectAnswer, int necessaryPoints, String verb, String tense, List<String> instructions) {
	    String fileName = INSTRUCTIONS_FILE_PATH + languageCode + "_" + level + ".txt";
	    try (FileWriter writer = new FileWriter(fileName, true)) {
	        // Add the header line before each exercise with metadata and instruction
	        writer.write(languageCode + ":" + level + ":" + pointsPerCorrectAnswer + ":" + necessaryPoints + "\n");
	        writer.write("Please conjugate the verb \"" + verb + "\" in the \"" + tense + "\" tense:\n");
	
	        // Save instructions to a unique file
	        int instructionNumber = 1;
	        for (String instruction : instructions) {
	            writer.write(instructionNumber + ". " + instruction + "\n");
	            instructionNumber++;
	        }
	    } catch (IOException e) {
	        e.printStackTrace();
	        System.out.println("Error saving instructions to file.");
	    }
	}
	
	// Save a file with the instructions and teacher's answers that will permit the automatic correction for the student
	private void saveTeacherInputAndAnswers(String languageCode, int level, int pointsPerCorrectAnswer, int necessaryPoints, String verb, String tense, List<String> instructions, List<String> answers) {
	    String fileName = TEACHER_ANSWERS_FILE_PATH + languageCode + "_" + level + ".txt";
	    try (FileWriter writer = new FileWriter(fileName, true)) {
	        // Add the header line before each exercise with metadata and instruction
	        writer.write(languageCode + ":" + level + ":" + pointsPerCorrectAnswer + ":" + necessaryPoints + " \"Please conjugate the verb \"" + verb + "\" in the given tense \"" + tense + "\" tense\":\n");
	
	        // Save teacher input and answers to a unique file
	        int instructionNumber = 1;
	        for (int i = 0; i < instructions.size(); i++) {
	            writer.write(instructionNumber + ". " + instructions.get(i) + ":" + answers.get(i) + "\n");  // Use ':' as a separator
	            instructionNumber++;
	        }
	    } catch (IOException e) {
	        e.printStackTrace();
	        System.out.println("Error saving teacher input and answers to file.");
	    }
	}
}
