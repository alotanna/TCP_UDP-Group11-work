from socket import *
import json

# Server configuration
serverName = '10.255.56.101'
serverPort = 13000

def send_request(request_data):
    """Send request to server and return response"""
    clientSocket = socket(AF_INET, SOCK_STREAM)
    
    try:
        # Each request opens a short-lived TCP connection for simplicity
        clientSocket.connect((serverName, serverPort))
        # Serialize the request as JSON so the server can parse it
        clientSocket.send(json.dumps(request_data).encode())
        
        # Server sends a JSON response (assumed to fit in 4096 bytes)
        response = clientSocket.recv(4096).decode()
        return json.loads(response)
    
    except ConnectionRefusedError:
        print("\nERROR: Could not connect to server.")
        print("Please make sure the server is running.")
        return None
    
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        return None
    
    finally:
        clientSocket.close()

def display_menu():
    """Display main menu"""
    print("TRIVIA QUIZ GAME - MAIN MENU\n")
    print("1. Start Quiz")
    print("2. View Leaderboard")
    print("3. View My Statistics")
    print("4. Quit\n")

def get_player_name():
    """Get and validate player name"""
    while True:
        name = input("\nEnter your player name: ").strip()
        if name:
            return name
        print("ERROR: Name cannot be empty")

def select_category():
    """Let player select a category"""
    # Ask the server for the current list of categories
    response = send_request({"action": "get_categories"})
    
    if response is None or response.get("status") != "success":
        print("\nERROR: Could not retrieve categories from server.")
        return None
    
    categories = response.get("categories", [])
    
    print("\n")
    print("SELECT CATEGORY\n")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")
    print(" " * 60)
    
    while True:
        try:
            choice = input("\nEnter category number: ").strip()
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(categories):
                # Convert numeric choice back to category string
                return categories[choice_num - 1]
            else:
                print(f"ERROR: Please enter a number between 1 and {len(categories)}")
        
        except ValueError:
            print("ERROR: Please enter a valid number")

def play_quiz(player_name):
    """Main quiz gameplay loop"""
    category = select_category()
    
    if category is None:
        return
    
    print(f"\n\nStarting quiz in category: {category}")
    print("Answer questions by typing A, B, C, or D")
    print("Type 'quit' to return to main menu\n")
    
    questions_answered = 0
    correct_count = 0
    total_points = 0
    
    while True:
        # Get a question from server
        question_response = send_request({
            "action": "get_question",
            "category": category
        })
        
        if question_response is None or question_response.get("status") != "success":
            print("\nERROR: Could not retrieve question from server.")
            break
        
        question = question_response.get("question")
        options = question_response.get("options")
        difficulty = question_response.get("difficulty")
        
        # Display question
        print("\n")
        print(f"QUESTION {questions_answered + 1} (Difficulty: {difficulty.upper()})")
        # Points are based on difficulty (our server would use same scale)
        points_available = {"easy": 10, "medium": 20, "hard": 30}.get(difficulty, 10)
        print(f"Points available: {points_available}")
        print(" ")
        print(f"{question}")
        print()
        for option in options:
            print(f"  {option}")
        print(" ")
        
        # Get user answer
        user_answer = input("\nYour answer (A/B/C/D or 'quit'): ").strip().upper()
        
        if user_answer.lower() == 'quit':
            print("\nReturning to main menu")
            break
        
        if user_answer not in ['A', 'B', 'C', 'D']:
            print("ERROR: Please enter A, B, C, or D")
            continue
        
        # Submit answer for validation (server checks against its question bank)
        # We send the question text/difficulty so server can match the right item
        submit_response = send_request({
            "action": "submit_answer",
            "player_name": player_name,
            "category": category,
            "question": question,
            "answer": user_answer,
            "correct_answer": "VALIDATE",  # Server will check against its database
            "difficulty": difficulty
        })
        
        if submit_response and submit_response.get("status") == "success":
            is_correct = submit_response.get("correct")
            points_earned = submit_response.get("points_earned")
            total_score = submit_response.get("total_score")
            correct_answer = submit_response.get("correct_answer")
            
            questions_answered += 1
            
            if is_correct:
                correct_count += 1
                total_points += points_earned
                print(f"\nCORRECT! You earned {points_earned} points.")
            else:
                print(f"\nINCORRECT. The correct answer was {correct_answer}.")
            
            print(f"Your total score: {total_score} points")
            # Local session accuracy (server keeps global stats)
            print(f"Session: {correct_count}/{questions_answered} correct ({correct_count/questions_answered*100:.1f}%)")
        else:
            print("\nERROR: Could not validate answer.")
        
        # Ask if they want to continue every 5 questions
        if questions_answered % 5 == 0:
            print("\n")
            print(f"PROGRESS REPORT")
            print(" " * 60)
            print(f"Questions answered: {questions_answered}")
            print(f"Correct answers: {correct_count}")
            print(f"Accuracy: {correct_count/questions_answered*100:.1f}%")
            print(f"Points this session: {total_points}")
            print(" ")
            # Small checkpoint so players can stop without losing context
            cont = input("\nContinue with more questions? (yes/no): ").strip().lower()
            if cont not in ['yes', 'y']:
                print("\n")
                print("QUIZ SESSION COMPLETE")
                print(" ")
                print(f"Final results:")
                print(f"  Questions: {questions_answered}")
                print(f"  Correct: {correct_count}")
                print(f"  Points earned: {total_points}")
                print(" ")
                break

def view_leaderboard():
    """Display the global leaderboard"""
    # Request top N players from server
    response = send_request({
        "action": "get_leaderboard",
        "top_n": 10
    })
    
    if response is None or response.get("status") != "success":
        print("\nERROR: Could not retrieve leaderboard from server.")
        return
    
    leaderboard = response.get("leaderboard", [])
    
    print("\n")
    print("GLOBAL LEADERBOARD - TOP 10 PLAYERS")
    print(f"{'Rank':<6} {'Player Name':<30} {'Score':<10}")
    print(" ")
    
    if not leaderboard:
        print("No players yet. Be the first to play!")
    else:
        for entry in leaderboard:
            rank = entry['rank']
            player = entry['player']
            score = entry['score']
            print(f"{rank:<6} {player:<30} {score:<10}")
    
    print(" ")

def view_statistics(player_name):
    """Display player's personal statistics"""
    # Ask server for the player's stored stats
    response = send_request({
        "action": "get_stats",
        "player_name": player_name
    })
    
    if response is None or response.get("status") != "success":
        print(f"\nNo statistics found for player '{player_name}'")
        print("Play some games to build your stats!")
        return
    
    stats = response.get("stats", {})
    
    print("\n")
    print(f"PLAYER STATISTICS - {stats['player_name']}")
    print(" ")
    print(f"Total Score:        {stats['total_score']}")
    print(f"Questions Answered: {stats['total_questions']}")
    print(f"Correct Answers:    {stats['correct_answers']}")
    print(f"Accuracy:           {stats['accuracy']}%")
    print("\n")
    print("PERFORMANCE BY CATEGORY")
    print(" ")
    print(f"{'Category':<20} {'Attempted':<12} {'Correct':<12} {'Accuracy':<12}")
    print(" ")
    
    categories = stats.get('categories', {})
    if not categories:
        print("No category data yet.")
    else:
        for category, cat_stats in categories.items():
            attempted = cat_stats['attempted']
            correct = cat_stats['correct']
            accuracy = (correct / attempted * 100) if attempted > 0 else 0
            print(f"{category:<20} {attempted:<12} {correct:<12} {accuracy:<12.1f}%")
    
    print(" ")

def main():
    """this is the main application loop"""
    print("\n")
    print("WELCOME TO TRIVIA QUIZ GAME")
    print(" ")
    print("Test your knowledge across multiple categories!")
    print("Earn points based on difficulty:")
    print("  Easy: 10 points , Medium: 20 points , Hard: 30 points")
    print(" ")
    
    # Capture name once per session; stats are tracked by this name
    player_name = get_player_name()
    print(f"\nWelcome, {player_name}!")
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            play_quiz(player_name)
        
        elif choice == '2':
            view_leaderboard()
        
        elif choice == '3':
            view_statistics(player_name)
        
        elif choice == '4':
            print("\n")
            print("Thank you for playing")
            print("Byeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee!")
            break
        
        else:
            print("\nERROR: Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
