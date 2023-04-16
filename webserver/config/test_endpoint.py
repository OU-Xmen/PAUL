import requests

# [ Options ]
domain = "https://paulis.online/endpoint"

# List of games
valid_games = ['Puzzle', 'Asteroids', 'Tetris', 'Pong', 'Hangman', 'Mad Libs', 'Checkers', 'Chess', 'Guess the Number', 'Snake', 'Tic Tac Toe', 'Connect 4', 'Mancala', 'RPS', 'PAULatformer']

# Make POST request with name, score, and game to endpoint to add score
# r = requests.get(domain, params={'task':'put', 'name': 'HELP I AM TRAPPED IN A COMPUTER PLEASE LET ME OUT', 'score': 9001, 'game': 'Puzzle'})
# Print status code and response
# print(f"[Code {r.status_code}] {r.text}")

# Make GET request to endpoint to retrieve scores
r = requests.get(domain)
# Print status code and response
print(f"[Code {r.status_code}] {r.text}")
