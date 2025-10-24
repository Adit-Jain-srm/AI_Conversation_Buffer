"""
AI Conversation Buffer with Editing Feature

This module implements a system to manage user prompts and AI responses
within a context window of size K. It supports UNDO, FINALIZE, and HISTORY commands.
"""

class Stack:
    """Custom implementation of a stack (LIFO - Last In, First Out)"""
    
    def __init__(self):
        self.items = []
    
    def push(self, item):
        """Add an item to the top of the stack"""
        self.items.append(item)
    
    def pop(self):
        """Remove and return the top item from the stack"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items.pop()
    
    def peek(self):
        """Return the top item without removing it"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items[-1]
    
    def is_empty(self):
        """Check if the stack is empty"""
        return len(self.items) == 0
    
    def size(self):
        """Return the number of items in the stack"""
        return len(self.items)
    
    def __str__(self):
        return str(self.items)


class Queue:
    """Custom implementation of a queue (FIFO - First In, First Out)"""
    
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        """Add an item to the rear of the queue"""
        self.items.append(item)
    
    def dequeue(self):
        """Remove and return the front item from the queue"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items.pop(0)
    
    def front(self):
        """Return the front item without removing it"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items[0]
    
    def is_empty(self):
        """Check if the queue is empty"""
        return len(self.items) == 0
    
    def size(self):
        """Return the number of items in the queue"""
        return len(self.items)
    
    def __str__(self):
        return str(self.items)


class ConversationBuffer:
    """
    Manages user prompts and AI responses within a context window of size K.
    Supports UNDO, FINALIZE, and HISTORY commands.
    """
    
    def __init__(self, context_window_size):
        """
        Initialize the conversation buffer with a context window size.
        
        Args:
            context_window_size (int): Maximum number of prompt-response pairs allowed
        """
        if context_window_size < 1:
            raise ValueError("Context window size must be at least 1")
        
        self.K = context_window_size
        self.prompts = Queue()  # FIFO for prompts
        self.responses = Stack()  # LIFO for responses (allows UNDO)
        self.finalized_pairs = []  # Store finalized prompt-response pairs
        self.current_prompt = None  # Track the current prompt being processed
    
    def add_prompt(self, prompt):
        """
        Add a new prompt to the conversation.
        
        Args:
            prompt (str): The user prompt to add
        """
        # If we have a current prompt with responses, finalize it first
        if self.current_prompt is not None and not self.responses.is_empty():
            self._finalize_current_pair()
        
        # Check if we need to remove oldest finalized pair to make room
        # Context window K limits the number of finalized prompt-response pairs
        if len(self.finalized_pairs) >= self.K:
            self.finalized_pairs.pop(0)  # Remove oldest finalized pair
        
        # Add new prompt
        self.prompts.enqueue(prompt)
        self.current_prompt = prompt
        print(f"Prompt added: '{prompt}'")
    
    def add_response(self, response):
        """
        Add a new AI response for the current prompt.
        
        Args:
            response (str): The AI response to add
        """
        if self.current_prompt is None:
            raise ValueError("No current prompt. Add a prompt first.")
        
        self.responses.push(response)
        print(f"Response added: '{response}'")
    
    def undo(self):
        """
        Remove the most recent AI response (UNDO command).
        """
        if self.responses.is_empty():
            print("No responses to undo!")
            return
        
        undone_response = self.responses.pop()
        print(f"Undone: '{undone_response}'")
    
    def finalize(self):
        """
        Finalize the current prompt-response pair (FINALIZE command).
        """
        if self.current_prompt is None:
            print("No current prompt to finalize!")
            return
        
        if self.responses.is_empty():
            print("No responses to finalize!")
            return
        
        # Get the final response (top of stack)
        final_response = self.responses.peek()
        
        # Add to finalized pairs
        self.finalized_pairs.append({
            'prompt': self.current_prompt,
            'response': final_response
        })
        
        print(f"Finalized: '{final_response}'")
        
        # Clear current state
        self.current_prompt = None
        self.responses = Stack()  # Clear the stack
    
    def _finalize_current_pair(self):
        """Internal method to finalize current pair without user command"""
        if self.current_prompt is not None and not self.responses.is_empty():
            final_response = self.responses.peek()
            self.finalized_pairs.append({
                'prompt': self.current_prompt,
                'response': final_response
            })
            self.current_prompt = None
            self.responses = Stack()
    
    def history(self):
        """
        Print the current context window (HISTORY command).
        """
        print("\n=== CONVERSATION HISTORY ===")
        
        if not self.finalized_pairs and self.current_prompt is None:
            print("No conversation history available.")
            return
        
        # Show finalized pairs
        for i, pair in enumerate(self.finalized_pairs, 1):
            print(f"{i}. Prompt: '{pair['prompt']}'")
            print(f"   Response: '{pair['response']}'")
            print()
        
        # Show current prompt and responses if any
        if self.current_prompt is not None:
            print(f"{len(self.finalized_pairs) + 1}. Prompt: '{self.current_prompt}'")
            if not self.responses.is_empty():
                # Show all responses in the stack (most recent first)
                responses_list = list(self.responses.items)
                responses_list.reverse()  # Show in order they were added
                for j, response in enumerate(responses_list):
                    status = " (CURRENT)" if j == len(responses_list) - 1 else " (UNDONE)"
                    print(f"   Response{j+1}: '{response}'{status}")
            else:
                print("   Response: (No responses yet)")
        
        print("=" * 30)
    
    def get_status(self):
        """
        Get current status of the conversation buffer.
        
        Returns:
            dict: Status information
        """
        return {
            'context_window_size': self.K,
            'finalized_pairs': len(self.finalized_pairs),
            'current_prompt': self.current_prompt,
            'pending_responses': self.responses.size(),
            'total_prompts': self.prompts.size()
        }


def main():
    """
    Main function to demonstrate the Conversation Buffer system.
    """
    print("AI Conversation Buffer System")
    print("=" * 40)
    
    # Get context window size from user
    while True:
        try:
            k = int(input("Enter context window size (K): "))
            if k >= 1:
                break
            else:
                print("Context window size must be at least 1.")
        except ValueError:
            print("Please enter a valid number.")
    
    buffer = ConversationBuffer(k)
    
    print(f"\nContext window size set to {k}")
    print("\nCommands:")
    print("- ADD_PROMPT <text> - Add a new prompt")
    print("- ADD_RESPONSE <text> - Add a response to current prompt")
    print("- UNDO - Remove the most recent response")
    print("- FINALIZE - Finalize current prompt-response pair")
    print("- HISTORY - Show conversation history")
    print("- STATUS - Show current status")
    print("- QUIT - Exit the program")
    print("\n" + "=" * 40)
    
    while True:
        try:
            command = input("\nEnter command: ").strip().upper()
            
            if command == "QUIT":
                print("Goodbye!")
                break
            
            elif command == "HISTORY":
                buffer.history()
            
            elif command == "STATUS":
                status = buffer.get_status()
                print(f"Context Window Size: {status['context_window_size']}")
                print(f"Finalized Pairs: {status['finalized_pairs']}")
                print(f"Current Prompt: {status['current_prompt']}")
                print(f"Pending Responses: {status['pending_responses']}")
                print(f"Total Prompts: {status['total_prompts']}")
            
            elif command == "UNDO":
                buffer.undo()
            
            elif command == "FINALIZE":
                buffer.finalize()
            
            elif command.startswith("ADD_PROMPT "):
                prompt = command[11:].strip()
                if prompt:
                    buffer.add_prompt(prompt)
                else:
                    print("Please provide a prompt text.")
            
            elif command.startswith("ADD_RESPONSE "):
                response = command[13:].strip()
                if response:
                    buffer.add_response(response)
                else:
                    print("Please provide a response text.")
            
            else:
                print("Unknown command. Please try again.")
        
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
