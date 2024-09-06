"""
Helper Functions for Trivia Quiz Game

This module contains helper functions for the trivia quiz game, including 
fetching questions from the Open Trivia Database API, running the quiz with 
multiple players, and writing the results to a CSV file.

Functions:
    - get_questions: Fetch trivia questions from the API.
    - quiz: Conduct the quiz and track player scores.
    - calculate_winner: Calculates and declears the winner.
    - write_score_to_csv: Export the player scores to a CSV file.

Dependencies:
    - requests: Required for fetching trivia questions from the API.

Author: Maria Aho
Date: 2024-09-05
"""

import csv
from html import unescape
import json
from random import shuffle

from requests import get


# The docstrings were written by ChatGPT AI, and edited by the author.

def get_questions(no_questions=3):
    """
    Fetches trivia questions from the Open Trivia Database API.

    This function makes a GET request to the Open Trivia Database API to 
    retrieve a specified number of trivia questions. The number of questions 
    can be customized, but it has a maximum limit of 50. By default, it fetches
    3 questions.

    Args:
        no_questions (int): The number of trivia questions to retrieve. 
        Defaults to 3. Maximum is 50.

    Returns:
        requests.Response: The response object from the Open Trivia Database 
        API, containing the trivia questions if the request is successful.

    Raises:
        Prints an error message if the API call fails (i.e., status code is not 
        200).
    """
    response = get(f'https://opentdb.com/api.php?amount={no_questions}')
    if response.status_code != 200:
        print(
            f"Something went wrong! Didn't get the questions, got status code "
            f"{response.status_code}"
            )
    return response


def quiz(response, player_list:list):
    """
    Conducts a trivia quiz for multiple players based on questions from a 
    provided API response.

    This function processes trivia questions from the API response, cleans up 
    any HTML entities, and presents them as multiple-choice questions to a list
    of players. Each player's answer is checked for correctness, and their 
    scores are recorded. After each question, the correct answer is displayed.

    Args:
        response (requests.Response): The response object from an API call 
                                      (typically containing trivia questions).
        player_list (list): A list of player names. Each player will answer 
                            each trivia question.

    Returns:
        dict: A dictionary where each key is a player's name, and each value is
        a nested dictionary containing the player's score per question. The 
        format is:
            {
                'player_name': {
                    'question_number': points (1 for correct, 0 for incorrect)
                }
            }

    Flow:
        - The function starts by initializing a `score` dictionary to track 
          each player's points.
        - It processes each question from the `response`, cleaning HTML 
          entities and shuffling answer choices.
        - Each player is prompted with a multiple-choice question and their 
          answer is compared to the correct answer.
        - Players' scores are updated based on their responses (1 point for 
          correct answers).
        - After each question, the correct answer is displayed.

    Example Usage:
        >>> response = requests.get('https://opentdb.com/api.php?amount=5')
        >>> player_list = ['Alice', 'Bob']
        >>> scores = quiz(response, player_list)
        >>> print(scores)
        {
            'Alice': {'1': 1, '2': 0, '3': 1, '4': 1, '5': 0},
            'Bob': {'1': 1, '2': 1, '3': 0, '4': 0, '5': 1}
        }
    """
    # prepare a dictionary to keep score
    score = {}
    for player in player_list:
        score[player] = {}

    # initialize counter for the questions
    question_number = 1
    # Parse the questions and answers from the given response
    for item in response.json()["results"]:
        # Get the question from the response, and clean the html entities
        question = unescape(item["question"])
        # Get the correct and incorrect answers from the response, and
        # clean the html entities
        correct_answer = unescape(item["correct_answer"])
        choices = [unescape(choice) for choice in item["incorrect_answers"]]
        # Combine the correct and incorrect answers, and shuffle
        choices.append(correct_answer)
        shuffle(choices)
        # Form a multiple choice question
        question_with_choices = (
            f"{question} Choices are: {', '.join(choices)}"
        )

        # Ask each player the question 
        for player in player_list: 
            answer = input(f'{player}: {question_with_choices}\n')
            # Check if the answer is correct, ignoring lower/upper case mistakes
            if answer.upper() == correct_answer.upper():
                player_points = 1
            else:
                player_points = 0
            # Add the question number and points to the score dictionary
            score[player][str(question_number)] = player_points
        # Keep score of the question number
        question_number += 1
        # Print out the correct answer
        print(f"\nCorrect answer is: {correct_answer}\n")
    return score    


def calculate_winner(score):
    """
    Calculates the total scores for each player and determines the highest 
    scorer(s). Iterates through the `score` dictionary (which stores the points
    for each player) to compute the total score for each player. It then 
    identifies the player(s) with the highest score. If multiple players share 
    the highest score, they are all considered winners. If the highest score is 
    0, it informs the users that no points were earned.

    Variables:
    highest_score (int): A variable to track the highest score found so far, 
                         initialized to -1.
    persons_with_highest_score (list): A list to store the names of players 
                                       with the highest score.
    player_point_sums (dict): A dictionary to store the total points for each 
                              player.

    Flow:
    1. Loop through each player and their respective score dictionary in the 
       `score` dictionary.
    2. Calculate the sum of their points.
    3. Compare the total score with `highest_score`. If the total score is 
       higher, update `highest_score` and reset the `persons_with_highest_score`
       list to the current player.
    4. If a player's total score equals the current highest score, append them 
       to `persons_with_highest_score`.
    5. After evaluating all players, print the player(s) with the highest score.
    6. If the highest score is 0, print a message indicating no points were 
       earned. Otherwise, congratulate the winners.

    Example:
    Given a `score` dictionary like this:
        score = {
            'Sheldon': {'1': 0, '2': 1, '3': 1},
            'Leonard': {'1': 0, '2': 0, '3': 0},
            'Penny': {'1': 1, '2': 1, '3': 1}
        }
    The output would be:
        Player(s) with the highest score (3):
        Penny
        Congratulations!

    Raises:
    Prints a message if no player scores more than 0 points.
    """
    # Initialize variable to store the highest score 
    highest_score = -1
    # Initialize list variable to store the persons with the highest score
    persons_with_highest_score = []
    # Initialize dictionary variable to store the sum of scores for each person
    player_point_sums = {}
    for person, scores in score.items():
        total_score = sum(scores.values())
        player_point_sums[person] = total_score
        if total_score > highest_score:
            highest_score = total_score
            persons_with_highest_score = [person]
        elif total_score == highest_score:
            persons_with_highest_score.append(person)
    # Print the results. Player cannot be a winner with 0 points.
    if highest_score == 0:
        print("Sorry, no points. Better luck next time!")
    else:    
        print(f"Player(s) with the highest score ({highest_score}):")
        for person in persons_with_highest_score:
            print(person)
        print("Congratulations!")


def write_score_to_csv(score):
    """
    Writes player scores to a CSV file.

    This function takes a dictionary of player scores, dynamically creates 
    headers for the CSV based on the number of questions, and writes the scores
    for each player along with their total points to the file `quiz_score.csv`.

    Args:
        score (dict): A dictionary where each key is a player's name, and each 
                      value is another dictionary that contains question 
                      numbers as keys and points (0 or 1) as values.
                      Example:
                      {
                          'Player1': {'1': 1, '2': 0, '3': 1},
                          'Player2': {'1': 0, '2': 1, '3': 1}
                      }

    Process:
        1. The function dynamically generates the headers for the CSV file by 
           inspecting the keys of the first player' score dictionary. These 
           keys represent the question numbers.
        2. The headers include the player's name, each question, and a 'Total' 
           column for the sum of the player's points.
        3. The function opens the file `quiz_score.csv` in write mode and 
           writes the headers and the player scores.
        4. For each player, it calculates the total score (sum of the player's 
           points) and writes the player's name, question scores, and total 
           points to the CSV file.
        5. Prints a message to indicate that the CSV file has been written.

    CSV Structure:
        - The first row contains headers: 'Name', 'Question 1', 'Question 2', 
          ..., 'Total'.
        - Each subsequent row contains the player's name, their score for each 
        question, and the total score.
    
    Example Output in `quiz_score.csv`:
        Name, Question 1, Question 2, Question 3, Total
        Player1, 1, 0, 1, 2
        Player2, 0, 1, 1, 2

    Prints:
        A message indicating that the results have been written to 
        `quiz_score.csv`.
    """
    # Dynamically creates the headers based on the keys of the first 
    # person's score (all players have the same number of questions, but 
    # the number of questions may vary). Adds'total' for the sum of points.
    # ChatGPT AI helped with use of `iter()` and `next()`, and mixing f string
    # with list comprehension. I didn't know that could be done!
    questions = list(next(iter(score.values())).keys())
    headers = ['Name'] + [f'Question {q_no}' for q_no in questions] + ['Total']
    with open('quiz_score.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        # Write the player's name and their points into a row in the csv file
        for person, scores in score.items():
            # Calculate the total score by summing the values of the score 
            # dictionary
            total = sum(scores.values())
            writer.writerow([person] + list(scores.values()) + [total])
    print('You can check the results in quiz_score.csv')        



if __name__== "__main__":

    player_list = ["Sheldon", "Leonard", "Penny"]
    response = get_questions(4)
    print(
        f"\nResponse printed pretty: " 
        f"\n{json.dumps(response.json(), indent=2, sort_keys=True)}\n"
        )
    score = quiz(response, player_list)
    print(score)
    
    # score = {
    #     'Sheldon': {'1': 0, '2': 1, '3': 1, '4': 1}, 
    #     'Leonard': {'1': 0, '2': 0,'3': 1, '4': 1}, 
    #     'Penny': {'1': 1, '2': 1, '3': 1, '4': 1}}
    
    calculate_winner(score)
    write_score_to_csv(score)