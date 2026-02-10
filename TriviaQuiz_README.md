# Trivia Quiz Game - Client-Server Application

## Overview

This is a multiplayer trivia quiz game built using TCP client-server architecture. Players can test their knowledge across multiple categories, earn points based on question difficulty, and compete on a global leaderboard.

## System Architecture

### Server (TriviaQuizServer.py)
- Manages question database with 25 questions across 5 categories
- Tracks player scores and statistics
- Validates answers and calculates points
- Maintains global leaderboard
- Handles multiple client connections sequentially

### Client (TriviaQuizClient.py)
- Interactive menu-driven interface
- Category selection
- Real-time answer validation
- Personal statistics tracking
- Leaderboard viewing

## Features

### 1. Question Database
- 5 categories: Science, History, Geography, Mathematics, General
- 25 total questions
- 3 difficulty levels: Easy (10 pts), Medium (20 pts), Hard (30 pts)
- Multiple choice format (A/B/C/D)

### 2. Scoring System
- Easy questions: 10 points
- Medium questions: 20 points
- Hard questions: 30 points
- Cumulative scoring across all sessions
- Per-category performance tracking

### 3. Player Statistics
- Total score
- Questions attempted
- Correct answers
- Overall accuracy percentage
- Category-wise breakdown

### 4. Global Leaderboard
- Top 10 players by total score
- Real-time updates
- Persistent across sessions (while server runs)

## How to Run

### Step 1: Start the Server

```bash
python TriviaQuizServer.py
```

You should see:
```
==============================================================
TRIVIA QUIZ SERVER
==============================================================
Server started on port 13000
Categories available: Science, History, Geography, Mathematics, General
Total questions: 25
==============================================================
Server ready at 2026-02-09 14:30:00
Waiting for connections...
==============================================================
```

### Step 2: Start the Client

Open a new terminal and run:

```bash
python TriviaQuizClient.py
```

### Step 3: Play the Game

1. Enter your player name
2. Select option 1 to start a quiz
3. Choose a category
4. Answer questions using A, B, C, or D
5. View your statistics and leaderboard ranking

## Usage Examples

### Starting a Quiz Session

```
Enter your player name: Alice

Welcome, Alice!

==============================================================
TRIVIA QUIZ GAME - MAIN MENU
==============================================================
1. Start Quiz
2. View Leaderboard
3. View My Statistics
4. Quit
==============================================================

Enter your choice (1-4): 1

==============================================================
SELECT CATEGORY
==============================================================
1. Science
2. History
3. Geography
4. Mathematics
5. General
==============================================================

Enter category number: 1

Starting quiz in category: Science
Answer questions by typing A, B, C, or D
Type 'quit' to return to main menu

------------------------------------------------------------
QUESTION 1 (Difficulty: EASY)
Points available: 10
------------------------------------------------------------
What is the chemical symbol for gold?

  A) Au
  B) Ag
  C) Fe
  D) Gd
------------------------------------------------------------

Your answer (A/B/C/D or 'quit'): A

CORRECT! You earned 10 points.
Your total score: 10 points
Session: 1/1 correct (100.0%)
```

### Viewing Statistics

```
Enter your choice (1-4): 3

==============================================================
PLAYER STATISTICS - Alice
==============================================================
Total Score:        150
Questions Answered: 12
Correct Answers:    9
Accuracy:           75.0%

------------------------------------------------------------
PERFORMANCE BY CATEGORY
------------------------------------------------------------
Category             Attempted    Correct      Accuracy    
------------------------------------------------------------
Science              5            4            80.0%       
History              4            3            75.0%       
Mathematics          3            2            66.7%       
==============================================================
```

### Viewing Leaderboard

```
Enter your choice (1-4): 2

==============================================================
GLOBAL LEADERBOARD - TOP 10 PLAYERS
==============================================================
Rank   Player Name                    Score     
------------------------------------------------------------
1      Alice                          150       
2      Bob                            120       
3      Charlie                        95        
==============================================================
```

## Technical Details

### Network Communication

**Protocol:** TCP (Transmission Control Protocol)

**Port:** 13000

**Data Format:** JSON

### Request-Response Pattern

All communication follows this pattern:

1. Client sends JSON request
2. Server processes request
3. Server sends JSON response
4. Connection closes

### API Endpoints (Actions)

#### 1. Get Categories
**Request:**
```json
{
  "action": "get_categories"
}
```

**Response:**
```json
{
  "status": "success",
  "categories": ["Science", "History", "Geography", "Mathematics", "General"]
}
```

#### 2. Get Question
**Request:**
```json
{
  "action": "get_question",
  "category": "Science"
}
```

**Response:**
```json
{
  "status": "success",
  "category": "Science",
  "question": "What is the chemical symbol for gold?",
  "options": ["A) Au", "B) Ag", "C) Fe", "D) Gd"],
  "difficulty": "easy"
}
```

#### 3. Submit Answer
**Request:**
```json
{
  "action": "submit_answer",
  "player_name": "Alice",
  "category": "Science",
  "question": "What is the chemical symbol for gold?",
  "answer": "A",
  "correct_answer": "VALIDATE",
  "difficulty": "easy"
}
```

**Response:**
```json
{
  "status": "success",
  "correct": true,
  "points_earned": 10,
  "total_score": 150,
  "correct_answer": "A"
}
```

#### 4. Get Leaderboard
**Request:**
```json
{
  "action": "get_leaderboard",
  "top_n": 10
}
```

**Response:**
```json
{
  "status": "success",
  "leaderboard": [
    {"rank": 1, "player": "Alice", "score": 150},
    {"rank": 2, "player": "Bob", "score": 120}
  ]
}
```

#### 5. Get Player Statistics
**Request:**
```json
{
  "action": "get_stats",
  "player_name": "Alice"
}
```

**Response:**
```json
{
  "status": "success",
  "stats": {
    "player_name": "Alice",
    "total_score": 150,
    "total_questions": 12,
    "correct_answers": 9,
    "accuracy": 75.0,
    "categories": {
      "Science": {"attempted": 5, "correct": 4}
    }
  }
}
```

### Error Handling

All errors follow this format:

```json
{
  "status": "error",
  "message": "Description of error"
}
```

Common errors:
- Invalid JSON format
- Unknown action
- Missing required fields
- Invalid category
- Connection refused (server not running)

## Configuration

### Changing Server Address

**For same machine:**
```python
serverName = 'localhost'  # Default
```

**For different machines:**
```python
serverName = '192.168.1.100'  # Replace with actual server IP
```

### Changing Port

Update both files:
```python
serverPort = 13000  # Change to desired port
```

## File Structure

```
trivia-quiz/
├── TriviaQuizServer.py    # Server application
├── TriviaQuizClient.py    # Client application
└── README.md              # This file
```

## Data Persistence

**Current Implementation:**
- Data persists while server is running
- Player scores and statistics reset when server restarts

**Future Enhancement:**
To make data persistent across server restarts, you could:
1. Save player data to JSON file periodically
2. Load data from file on server startup
3. Use SQLite database for better data management

Example enhancement:
```python
import json

# Save data
def save_data():
    with open('player_data.json', 'w') as f:
        json.dump({
            'scores': player_scores,
            'stats': player_stats
        }, f)

# Load data
def load_data():
    try:
        with open('player_data.json', 'r') as f:
            data = json.load(f)
            return data['scores'], data['stats']
    except FileNotFoundError:
        return {}, {}
```

## Extending the Game

### Easy Extensions

1. **Add More Questions**
   - Edit QUESTION_DATABASE in server
   - Add new categories
   - Increase question pool per category

2. **Customize Scoring**
   - Modify point values in check_answer()
   - Add bonus multipliers
   - Implement streak bonuses

3. **Change Difficulty Distribution**
   - Adjust ratio of easy/medium/hard questions
   - Add "expert" difficulty level

### Intermediate Extensions

1. **Timed Questions**
   - Add time limit per question
   - Bonus points for fast answers
   - Auto-submit after timeout

2. **Multiplayer Modes**
   - Head-to-head competition
   - Team play
   - Real-time battles

3. **Question Categories**
   - Allow subcategories (e.g., Physics under Science)
   - Custom category creation
   - Difficulty-based filtering

### Advanced Extensions

1. **Multi-threading**
   - Handle multiple concurrent clients
   - Separate thread per connection
   - Thread-safe data access

2. **Database Integration**
   - SQLite for questions and players
   - Persistent storage
   - Advanced queries and analytics

3. **Web Interface**
   - Convert to Flask/Django
   - HTML/CSS frontend
   - WebSocket for real-time updates

4. **Authentication**
   - User login system
   - Password protection
   - Session management

## Example Multi-threading Implementation

```python
import threading

def handle_client(connectionSocket, clientAddress):
    """Handle individual client in separate thread"""
    try:
        data = connectionSocket.recv(4096).decode()
        request = json.loads(data)
        response = process_request(request)
        connectionSocket.send(json.dumps(response).encode())
    except Exception as e:
        print(f"Error handling client {clientAddress}: {e}")
    finally:
        connectionSocket.close()

# Main server loop
while True:
    connectionSocket, clientAddress = serverSocket.accept()
    client_thread = threading.Thread(
        target=handle_client,
        args=(connectionSocket, clientAddress)
    )
    client_thread.start()
```

## Troubleshooting

### "Connection refused" error
**Problem:** Server is not running or wrong IP/port

**Solution:**
- Verify server is running
- Check IP address and port number
- Ensure firewall allows connection

### "Address already in use"
**Problem:** Port is already in use

**Solution:**
- Change port number in both files
- Stop other program using the port
- Wait a few seconds and try again

### Invalid JSON errors
**Problem:** Malformed data transmission

**Solution:**
- Check network stability
- Verify JSON encoding/decoding
- Add error handling in both client and server

### Questions repeat
**Problem:** Random selection can repeat questions

**Solution:**
- Track asked questions per session
- Implement question pool management
- Ensure questions aren't repeated until pool exhausted

## Testing

### Test Scenarios

1. **Single Player**
   - Start server
   - Start one client
   - Answer 10 questions
   - Check score accuracy

2. **Multiple Players**
   - Start server
   - Start multiple clients
   - Each player answers questions
   - Verify leaderboard updates

3. **Error Handling**
   - Try invalid answers
   - Test with empty inputs
   - Disconnect mid-game

4. **Statistics Accuracy**
   - Answer known questions
   - Verify point calculations
   - Check accuracy percentages

## Learning Outcomes

This project demonstrates:

1. **Network Programming**
   - TCP socket communication
   - Client-server architecture
   - Request-response pattern

2. **Data Management**
   - JSON serialization
   - In-memory data structures
   - State management

3. **Software Design**
   - Modular functions
   - Error handling
   - User interface design

4. **Python Skills**
   - Socket programming
   - Dictionary/list operations
   - String formatting
   - Exception handling

## Comparison with Original Experiment

**Original (String Conversion):**
- Simple uppercase transformation
- No data persistence
- Single request-response
- No state management

**Trivia Game (Enhanced):**
- Complex game logic
- Persistent player data
- Multiple request types
- State management across sessions
- Scoring system
- Statistics tracking

## Credits

Built as an extension of the basic UDP/TCP client-server networking experiment.

## License

Free to use for educational purposes.
