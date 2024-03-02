package fr.inalco.m2.a2023;

import java.util.List;

public class Exercise {
	// Instancing variables
    private String languageCode;
    private int level;
    private int pointsPerCorrectAnswer;
    private int necessaryPoints;
    private List<String> instructions;
    private List<String> answers;
    private String exerciseType;
    private String verb;
    private String tense;

    // Constructors
    public Exercise(String languageCode, int level, int pointsPerCorrectAnswer, int necessaryPoints,
                    List<String> instructions, List<String> answers, String exerciseType, String verb, String tense) {
        this.languageCode = languageCode;
        this.level = level;
        this.pointsPerCorrectAnswer = pointsPerCorrectAnswer;
        this.necessaryPoints = necessaryPoints;
        this.instructions = instructions;
        this.answers = answers;
        this.exerciseType = exerciseType;
        this.verb = verb;
        this.tense = tense;
    }
    // Getters
    public String getLanguageCode() {
        return languageCode;
    }

    public int getLevel() {
        return level;
    }

    public int getPointsPerCorrectAnswer() {
        return pointsPerCorrectAnswer;
    }

    public int getNecessaryPoints() {
        return necessaryPoints;
    }

    public List<String> getInstructions() {
        return instructions;
    }

    public List<String> getAnswers() {
        return answers;
    }

    public String getExerciseType() {
        return exerciseType;
    }

    public String getVerb() {
        return verb;
    }

    public String getTense() {
        return tense;
    }

    // Setters
    public void setInstructions(List<String> instructions) {
        this.instructions = instructions;
    }

    public void setAnswers(List<String> answers) {
        this.answers = answers;
    }
    
    // Makes the description for the exercise
    public String getDescription() {
        return "Please conjugate the verb " + verb + " in the " + tense + " tense";
    }
    
}
