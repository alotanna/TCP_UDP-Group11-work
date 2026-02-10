from socket import *
import json
import random
from datetime import datetime

serverPort = 13000

# Trivia question database organized by category
QUESTION_DATABASE = {
    "Science": [
        {
            "question": "What is the chemical symbol for gold?",
            "options": ["A) Au", "B) Ag", "C) Fe", "D) Gd"],
            "answer": "A",
            "difficulty": "easy"
        },
        {
            "question": "What planet is known as the Red Planet?",
            "options": ["A) Venus", "B) Mars", "C) Jupiter", "D) Saturn"],
            "answer": "B",
            "difficulty": "easy"
        },
        {
            "question": "What is the speed of light in vacuum?",
            "options": ["A) 300,000 km/s", "B) 150,000 km/s", "C) 500,000 km/s", "D) 250,000 km/s"],
            "answer": "A",
            "difficulty": "medium"
        },
        {
            "question": "What is the powerhouse of the cell?",
            "options": ["A) Nucleus", "B) Ribosome", "C) Mitochondria", "D) Endoplasmic Reticulum"],
            "answer": "C",
            "difficulty": "easy"
        },
        {
            "question": "What is the atomic number of carbon?",
            "options": ["A) 4", "B) 6", "C) 8", "D) 12"],
            "answer": "B",
            "difficulty": "medium"
        }
    ],
    "History": [
        {
            "question": "In which year did World War II end?",
            "options": ["A) 1943", "B) 1944", "C) 1945", "D) 1946"],
            "answer": "C",
            "difficulty": "easy"
        },
        {
            "question": "Who was the first President of the United States?",
            "options": ["A) Thomas Jefferson", "B) George Washington", "C) John Adams", "D) Benjamin Franklin"],
            "answer": "B",
            "difficulty": "easy"
        },
        {
            "question": "What year did the Berlin Wall fall?",
            "options": ["A) 1987", "B) 1988", "C) 1989", "D) 1990"],
            "answer": "C",
            "difficulty": "medium"
        },
        {
            "question": "Who was the first emperor of Rome?",
            "options": ["A) Julius Caesar", "B) Augustus", "C) Nero", "D) Caligula"],
            "answer": "B",
            "difficulty": "hard"
        },
        {
            "question": "What ancient wonder was located in Alexandria?",
            "options": ["A) Colossus of Rhodes", "B) Hanging Gardens", "C) Lighthouse of Alexandria", "D) Temple of Artemis"],
            "answer": "C",
            "difficulty": "medium"
        }
    ],
    "Geography": [
        {
            "question": "What is the capital of France?",
            "options": ["A) London", "B) Berlin", "C) Paris", "D) Madrid"],
            "answer": "C",
            "difficulty": "easy"
        },
        {
            "question": "Which is the longest river in the world?",
            "options": ["A) Amazon", "B) Nile", "C) Yangtze", "D) Mississippi"],
            "answer": "B",
            "difficulty": "medium"
        },
        {
            "question": "What is the smallest country in the world?",
            "options": ["A) Monaco", "B) Vatican City", "C) San Marino", "D) Liechtenstein"],
            "answer": "B",
            "difficulty": "medium"
        },
        {
            "question": "Which desert is the largest in the world?",
            "options": ["A) Sahara", "B) Gobi", "C) Arabian", "D) Antarctic"],
            "answer": "D",
            "difficulty": "hard"
        },
        {
            "question": "What is the deepest ocean trench?",
            "options": ["A) Puerto Rico Trench", "B) Java Trench", "C) Mariana Trench", "D) Tonga Trench"],
            "answer": "C",
            "difficulty": "medium"
        }
    ],
    "Mathematics": [
        {
            "question": "What is the square root of 144?",
            "options": ["A) 10", "B) 11", "C) 12", "D) 13"],
            "answer": "C",
            "difficulty": "easy"
        },
        {
            "question": "What is the value of pi (approximately)?",
            "options": ["A) 3.14", "B) 2.71", "C) 1.41", "D) 1.73"],
            "answer": "A",
            "difficulty": "easy"
        },
        {
            "question": "What is 15% of 200?",
            "options": ["A) 25", "B) 30", "C) 35", "D) 40"],
            "answer": "B",
            "difficulty": "medium"
        },
        {
            "question": "What is the next prime number after 7?",
            "options": ["A) 9", "B) 10", "C) 11", "D) 13"],
            "answer": "C",
            "difficulty": "easy"
        },
        {
            "question": "What is the derivative of x^2?",
            "options": ["A) x", "B) 2x", "C) x^2", "D) 2"],
            "answer": "B",
            "difficulty": "hard"
        }
    ],
    "General": [
        {
            "question": "How many days are in a leap year?",
            "options": ["A) 364", "B) 365", "C) 366", "D) 367"],
            "answer": "C",
            "difficulty": "easy"
        },
        {
            "question": "What is the largest mammal in the world?",
            "options": ["A) African Elephant", "B) Blue Whale", "C) Giraffe", "D) Polar Bear"],
            "answer": "B",
            "difficulty": "easy"
        },
        {
            "question": "How many continents are there?",
            "options": ["A) 5", "B) 6", "C) 7", "D) 8"],
            "answer": "C",
            "difficulty": "easy"
        },
        {
            "question": "What is the hardest natural substance?",
            "options": ["A) Gold", "B) Iron", "C) Diamond", "D) Platinum"],
            "answer": "C",
            "difficulty": "medium"
        },
        {
            "question": "How many keys are on a standard piano?",
            "options": ["A) 76", "B) 88", "C) 92", "D) 100"],
            "answer": "B",
            "difficulty": "medium"
        }
    ]
}

# Player database to track scores
player_scores = {}
player_stats = {}

def get_categories():
    """Return list of available categories"""
    return list(QUESTION_DATABASE.keys())

def get_random_question(category):
    """Get a random question from specified category"""
    if category not in QUESTION_DATABASE:
        return None
    # Random selection keeps gameplay from repeating the same order
    return random.choice(QUESTION_DATABASE[category])

def check_answer(player_name, category, question_text, user_answer, correct_answer, difficulty):
    """Check if answer is correct and update player score"""
    # Find the correct answer from the database by matching the question
    actual_correct_answer = None
    actual_difficulty = difficulty
    
    if category in QUESTION_DATABASE:
        for q in QUESTION_DATABASE[category]:
            if q["question"] == question_text:
                actual_correct_answer = q["answer"]
                actual_difficulty = q["difficulty"]
                break
    
    # If we couldn't find the question, use the provided answer (fallback)
    # This prevents breaking if the client sent a question we don't have.
    if actual_correct_answer is None:
        actual_correct_answer = correct_answer
    
    is_correct = user_answer.upper() == actual_correct_answer.upper()
    
    # Initialize player stats on first encounter
    if player_name not in player_scores:
        player_scores[player_name] = 0
        player_stats[player_name] = {
            "total_questions": 0,
            "correct_answers": 0,
            "categories": {}
        }
    
    # Update statistics (overall + per-category)
    player_stats[player_name]["total_questions"] += 1
    
    if category not in player_stats[player_name]["categories"]:
        player_stats[player_name]["categories"][category] = {
            "attempted": 0,
            "correct": 0
        }
    
    player_stats[player_name]["categories"][category]["attempted"] += 1
    
    # Calculate points based on difficulty
    points = 0
    if is_correct:
        player_stats[player_name]["correct_answers"] += 1
        player_stats[player_name]["categories"][category]["correct"] += 1
        
        if actual_difficulty == "easy":
            points = 10
        elif actual_difficulty == "medium":
            points = 20
        elif actual_difficulty == "hard":
            points = 30
        
        player_scores[player_name] += points
    
    return {
        "correct": is_correct,
        "points_earned": points,
        "total_score": player_scores[player_name],
        "correct_answer": actual_correct_answer
    }

def get_leaderboard(top_n=10):
    """Get top N players by score"""
    # Sort descending by score; return only the top N entries
    sorted_players = sorted(player_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_players[:top_n]

def get_player_stats(player_name):
    """Get detailed statistics for a player"""
    if player_name not in player_stats:
        return None
    
    stats = player_stats[player_name]
    # Guard against division by zero if they haven't answered any questions yet
    accuracy = (stats["correct_answers"] / stats["total_questions"] * 100) if stats["total_questions"] > 0 else 0
    
    return {
        "player_name": player_name,
        "total_score": player_scores[player_name],
        "total_questions": stats["total_questions"],
        "correct_answers": stats["correct_answers"],
        "accuracy": round(accuracy, 2),
        "categories": stats["categories"]
    }

def process_request(request_data):
    """Process client request and return appropriate response"""
    try:
        action = request_data.get("action")
        # Each action maps to a specific server feature (like a mini API)
        
        if action == "get_categories":
            return {
                "status": "success",
                "categories": get_categories()
            }
        
        elif action == "get_question":
            category = request_data.get("category", "General")
            question = get_random_question(category)
            
            if question is None:
                return {
                    "status": "error",
                    "message": f"Category '{category}' not found"
                }
            
            return {
                "status": "success",
                "category": category,
                "question": question["question"],
                "options": question["options"],
                "difficulty": question["difficulty"]
            }
        
        elif action == "submit_answer":
            player_name = request_data.get("player_name")
            category = request_data.get("category")
            question_text = request_data.get("question")
            user_answer = request_data.get("answer")
            correct_answer = request_data.get("correct_answer")
            difficulty = request_data.get("difficulty")
            
            # Basic validation to avoid crashes from missing fields
            if not all([player_name, category, user_answer, correct_answer]):
                return {
                    "status": "error",
                    "message": "Missing required fields"
                }
            
            result = check_answer(player_name, category, question_text, user_answer, correct_answer, difficulty)
            result["status"] = "success"
            return result
        
        elif action == "get_leaderboard":
            top_n = request_data.get("top_n", 10)
            leaderboard = get_leaderboard(top_n)
            
            return {
                "status": "success",
                "leaderboard": [{"rank": i+1, "player": name, "score": score} 
                               for i, (name, score) in enumerate(leaderboard)]
            }
        
        elif action == "get_stats":
            player_name = request_data.get("player_name")
            stats = get_player_stats(player_name)
            
            if stats is None:
                return {
                    "status": "error",
                    "message": f"No statistics found for player '{player_name}'"
                }
            
            return {
                "status": "success",
                "stats": stats
            }
        
        else:
            return {
                "status": "error",
                "message": f"Unknown action: {action}"
            }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Server error: {str(e)}"
        }

# Create TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(10)

print("TRIVIA QUIZ SERVER")
print(" " * 60)
print(f"Server started on port {serverPort}")
print(f"Categories available: {', '.join(get_categories())}")
print(f"Total questions: {sum(len(questions) for questions in QUESTION_DATABASE.values())}")
print(" " * 60)
print(f"Server ready at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("Waiting for connections...")
print(" " * 60)

while True:
    connectionSocket, clientAddress = serverSocket.accept()
    
    try:
        # Receive request from client
        data = connectionSocket.recv(4096).decode()
        request = json.loads(data)
        
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Connection from {clientAddress[0]}:{clientAddress[1]}")
        print(f"Action: {request.get('action')}")
        if request.get('player_name'):
            print(f"Player: {request.get('player_name')}")
        
        # Process request
        response = process_request(request)
        
        # Send response
        connectionSocket.send(json.dumps(response).encode())
        
        print(f"Response: {response.get('status')}")
    
    except json.JSONDecodeError:
        error_response = {"status": "error", "message": "Invalid JSON format"}
        connectionSocket.send(json.dumps(error_response).encode())
        print(f"[ERROR] Invalid JSON from {clientAddress[0]}")
    
    except Exception as e:
        error_response = {"status": "error", "message": str(e)}
        connectionSocket.send(json.dumps(error_response).encode())
        print(f"[ERROR] {str(e)}")
    
    finally:
        connectionSocket.close()
