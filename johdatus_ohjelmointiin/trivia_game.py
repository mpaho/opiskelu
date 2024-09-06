"""
Trivia Quiz Game

This script serves as the entry point for running the trivia quiz game. It 
relies on helper functions defined in `trivia_game_helpers.py` for fetching 
questions, conducting the quiz, and writing the results to a CSV file.

Helper functions:
    - `get_questions`: Fetches trivia questions from the Open Trivia Database 
       API.
    - `quiz`: Conducts the quiz with multiple players and tracks their scores.
    - `calculate_winner`: Calculates and declears the winner.
    - `write_score_to_csv`: Saves player scores to a CSV file.

Usage:
    Run this script to start a trivia quiz with multiple players.
    Example:
        python trivia_game.py

Dependencies:
    - trivia_game_helpers: Contains the helper functions used in this script.
    - requests: Used by `get_questions` to fetch trivia questions from the Open
      Trivia Database API.

Author: Maria Aho
Date: 2024-09-05
"""

# Docstring was provided by ChatGPT AI and edited by the author

import trivia_game_helpers as helpers



# Get information about the players, and the game length
print("Welcome to a trivia game!")
player_list = []
# Ask for the number of players until a number is given
while True:
    try:
        no_players = int(input('How many players? '))
        break
    except ValueError:
        print("Please, give a number")
number = 0
for player in range(no_players):
    number += 1
    # Ask for each player's name, and only accept a unique name
    while True:
        name = input(f"Player {number} name: ")
        if name not in player_list:
            player_list.append(name)
            break
        else:
            print("The name is already taken. Please give another name.\n")

# Ask for the number of questions until a number <= 50 is given
while True:
    try:
        no_questions = int(input(
            'How many questions would you like to have? '
            ))
    except ValueError:
        print("Please, give a number")
    if no_questions <= 50:
        print(
            f"\nThank you! Lets play the trivia game. All the contestants get" 
            f" to answer the same {no_questions} questions. Each correct "
            f"answer will earn you 1 point. If you don't know, guess! Eternal " 
            f"glory awaits whoever wins!\n")
        break
    else: 
        print("Sorry, the maximum number of questions is 50.")


# Get the quiz questions and answers from open trivia API:
response = helpers.get_questions(no_questions)

# Do the quiz for all the players, and save the results in 'score'
score = helpers.quiz(response, player_list)

# Calculate and publish the winner(s)
helpers.calculate_winner(score)

# Write the score to a csv file
helpers.write_score_to_csv(score)