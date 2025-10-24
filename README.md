# AI Conversation Buffer with Editing Feature

**Monthly Test 1 - Build4Hire Program by UnsaidTalks**  
**Author: Adit Jain**

A Python implementation of a conversation management system that handles user prompts and AI responses within a context window of size K. This system supports editing features like UNDO, FINALIZE, and HISTORY commands, mimicking real AI conversation tools.

## Features

- **Context Window Management**: Limits the number of active prompt-response pairs to prevent memory overflow
- **Stack-based Response Management**: Allows UNDO operations on the most recent AI responses
- **Queue-based Prompt Management**: Maintains chronological order of user prompts
- **Special Commands**: UNDO, FINALIZE, and HISTORY operations
- **Edge Case Handling**: Comprehensive error handling for empty stacks, overflow conditions, etc.

## Architecture

### Core Data Structures

1. **Stack (LIFO)**: Manages AI responses, allowing easy UNDO operations
2. **Queue (FIFO)**: Manages user prompts in chronological order
3. **ConversationBuffer**: Main class that orchestrates the conversation flow

### Key Components

- **Context Window (K)**: Maximum number of prompt-response pairs that can be active
- **Current Prompt**: The prompt being actively processed
- **Response Stack**: Stack of responses for the current prompt
- **Finalized Pairs**: Locked-in prompt-response combinations

## Installation

### Basic Installation (Command Line Interface)
No external dependencies required for the core functionality. This implementation uses only Python standard library.

```bash
# Clone or download the files
# Navigate to the project directory
cd AI_Conversation_Buffer

# Ensure you have Python 3.6+ installed
python --version
```

### Web Interface Installation (Streamlit)
For the web interface, install Streamlit:

```bash
# Install Streamlit
pip install streamlit>=1.28.0

# Or install from requirements.txt
pip install -r requirements.txt

# Navigate to the Code directory
cd Code
```

## Quick Start

### 🚀 Get Started in 3 Steps

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Navigate to Code Directory:**
   ```bash
   cd Code
   ```

3. **Launch Web Interface:**
   ```bash
   python run_streamlit.py
   ```

The web interface will open in your browser with an interactive demo!

## Usage

### Option 1: Web Interface (Recommended)

Launch the modern web interface:

```bash
# Navigate to the Code directory
cd Code

# Easy launcher (installs Streamlit if needed)
python run_streamlit.py

# Or run directly
streamlit run streamlit_app.py
```

The web interface provides:
- 🎛️ Interactive controls in the sidebar
- 📊 Real-time status display
- 💬 Visual conversation management
- 📝 Live response stack display
- 📚 Expandable conversation history
- 🎬 Interactive demo scenario

### Option 2: Command Line Interface

```bash
# Navigate to the Code directory
cd Code

# Run the command line interface
python conversation_buffer.py
```

The application will prompt you for:
1. Context window size (K)
2. Commands to manage the conversation

### Available Commands

- `ADD_PROMPT <text>` - Add a new user prompt
- `ADD_RESPONSE <text>` - Add an AI response to the current prompt
- `UNDO` - Remove the most recent response
- `FINALIZE` - Lock in the current prompt-response pair
- `HISTORY` - Display the conversation history
- `STATUS` - Show current buffer status
- `QUIT` - Exit the application

### Example Session

```
Enter context window size (K): 2

Enter command: ADD_PROMPT Suggest a healthy salad
Prompt added: 'Suggest a healthy salad'

Enter command: ADD_RESPONSE Caesar salad with croutons
Response added: 'Caesar salad with croutons'

Enter command: UNDO
Undone: 'Caesar salad with croutons'

Enter command: ADD_RESPONSE Kale salad with lemon dressing
Response added: 'Kale salad with lemon dressing'

Enter command: FINALIZE
Finalized: 'Kale salad with lemon dressing'

Enter command: HISTORY
=== CONVERSATION HISTORY ===
1. Prompt: 'Suggest a healthy salad'
   Response: 'Kale salad with lemon dressing'

==========================================
```

## Running Tests

```bash
# Navigate to the Code directory
cd Code

# Run the test suite
python test_conversation_buffer.py
```

The test suite includes:
- Unit tests for Stack and Queue implementations
- Integration tests for ConversationBuffer
- Edge case testing (empty stacks, overflow conditions)
- Demo scenario simulation

## Code Structure

```
├── Code/
│   ├── conversation_buffer.py    # Main implementation
│   ├── streamlit_app.py         # Web interface (Streamlit)
│   └── run_streamlit.py         # Easy launcher for web interface
├── requirements.txt              # Python dependencies
└── README.md                    # This file
```

**Note:** All executable code is located in the `Code/` directory. Make sure to navigate to this directory before running any commands.

### Key Classes

#### `Stack`
- `push(item)` - Add item to top
- `pop()` - Remove and return top item
- `peek()` - View top item without removing
- `is_empty()` - Check if stack is empty
- `size()` - Get number of items

#### `Queue`
- `enqueue(item)` - Add item to rear
- `dequeue()` - Remove and return front item
- `front()` - View front item without removing
- `is_empty()` - Check if queue is empty
- `size()` - Get number of items

#### `ConversationBuffer`
- `add_prompt(prompt)` - Add new user prompt
- `add_response(response)` - Add AI response
- `undo()` - Remove most recent response
- `finalize()` - Lock in current pair
- `history()` - Display conversation history
- `get_status()` - Get current buffer status

## Example Scenarios

### Scenario 1: Healthy Recipe Brainstorming

```python
buffer = ConversationBuffer(2)  # Context window of 2

# User asks for healthy salad
buffer.add_prompt("Suggest a healthy salad")
buffer.add_response("Caesar salad with croutons")
buffer.undo()  # "Too many carbs!"
buffer.add_response("Kale salad with lemon dressing")
buffer.finalize()  # User approves

# Add protein suggestion
buffer.add_prompt("Add a protein")
buffer.add_response("Grilled chicken")
buffer.finalize()

# Context window overflow - oldest pair removed
buffer.add_prompt("Make it vegetarian")
buffer.add_response("Add chickpeas or tofu")
buffer.finalize()
```

### Scenario 2: Code Review Process

```python
buffer = ConversationBuffer(3)  # Larger context window

buffer.add_prompt("Review this Python function")
buffer.add_response("The function looks good")
buffer.undo()  # "Actually, let me check the logic"
buffer.add_response("There's a potential bug in line 5")
buffer.add_response("Consider adding error handling")
buffer.finalize()  # Final review submitted
```

## Edge Cases Handled

1. **Empty Stack UNDO**: Gracefully handles UNDO when no responses exist
2. **Context Window Overflow**: Automatically removes oldest pairs when limit exceeded
3. **Finalize Without Responses**: Prevents finalizing empty response stacks
4. **Rapid Prompt Changes**: Auto-finalizes previous pairs when new prompts arrive
5. **Multiple UNDOs**: Handles consecutive UNDO operations safely

## Design Decisions

### Why Stack for Responses?
- Enables easy UNDO of the most recent response
- Mimics real-world editing behavior (like text editors)
- LIFO nature matches user expectation for "undo last action"

### Why Queue for Prompts?
- Maintains chronological order of user inputs
- FIFO behavior ensures oldest conversations are removed first
- Matches natural conversation flow

### Context Window Management
- Prevents memory overflow in long conversations
- Simulates real AI model limitations
- Ensures system remains responsive

## Performance Considerations

- **Time Complexity**: O(1) for all basic operations (push, pop, enqueue, dequeue)
- **Space Complexity**: O(K) where K is the context window size
- **Memory Management**: Automatic cleanup of old conversations
- **Scalability**: Handles any context window size efficiently

## Future Enhancements

1. **Token Counting**: Implement token-based limits instead of pair counts
2. **Persistent Storage**: Save conversations to disk
3. **Advanced Commands**: Add EDIT, REPLACE, and MERGE operations
4. **Conversation Analytics**: Track response patterns and user behavior

## Testing

The test suite covers:
- ✅ Basic stack and queue operations
- ✅ Conversation buffer functionality
- ✅ Edge cases and error conditions
- ✅ Context window overflow behavior
- ✅ Command validation and error handling
- ✅ Integration scenarios

## Contributing

This is a learning project demonstrating:
- Custom data structure implementation
- System design for conversation management
- Error handling and edge case management
- Test-driven development practices

## Submission Details

**Monthly Test 1 - Build4Hire Program by UnsaidTalks**  
**Author: Adit Jain**

This project demonstrates:
- **Data Structures**: Custom Stack and Queue implementations
- **System Design**: Context window management and conversation flow
- **Python Programming**: Clean code, error handling, and testing
- **Web Development**: Streamlit interface for user interaction
- **Testing**: Comprehensive test suite with 23 test cases

## Technical Implementation

### Core Features Delivered:
✅ Custom Stack and Queue classes from scratch  
✅ Context window management with overflow handling  
✅ UNDO, FINALIZE, and HISTORY commands  
✅ Interactive command-line interface  
✅ Modern web interface with Streamlit  
✅ Comprehensive test suite (23 tests)  
✅ Edge case handling and error management  

### Bonus Features:
✅ Web interface with real-time status display  
✅ Session state management  
✅ Visual conversation history  
✅ Easy launcher scripts  
✅ Cross-platform compatibility  

## License

This project is submitted as part of the Build4Hire Program by UnsaidTalks.