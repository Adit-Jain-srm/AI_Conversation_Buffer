"""
Streamlit Web Interface for AI Conversation Buffer

A modern, interactive web interface for the AI Conversation Buffer system.
Provides a user-friendly way to manage conversations with visual feedback.
"""

import streamlit as st
import json
from datetime import datetime
from conversation_buffer import ConversationBuffer, Stack, Queue


def initialize_session_state():
    """Initialize session state variables"""
    if 'buffer' not in st.session_state:
        st.session_state.buffer = None
    if 'context_size' not in st.session_state:
        st.session_state.context_size = 3
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'current_prompt' not in st.session_state:
        st.session_state.current_prompt = None
    if 'response_stack' not in st.session_state:
        st.session_state.response_stack = []


def create_buffer():
    """Create a new conversation buffer"""
    if st.session_state.context_size >= 1:
        st.session_state.buffer = ConversationBuffer(st.session_state.context_size)
        st.session_state.conversation_history = []
        st.session_state.current_prompt = None
        st.session_state.response_stack = []
        st.success(f"✅ Created new conversation buffer with context window size: {st.session_state.context_size}")
    else:
        st.error("❌ Context window size must be at least 1")


def add_prompt(prompt_text):
    """Add a new prompt to the conversation"""
    if st.session_state.buffer is None:
        st.error("❌ Please create a conversation buffer first")
        return
    
    if prompt_text.strip():
        st.session_state.buffer.add_prompt(prompt_text)
        st.session_state.current_prompt = prompt_text
        st.session_state.response_stack = []
        st.success(f"✅ Added prompt: '{prompt_text}'")
    else:
        st.error("❌ Please enter a valid prompt")


def add_response(response_text):
    """Add a response to the current prompt"""
    if st.session_state.buffer is None:
        st.error("❌ Please create a conversation buffer first")
        return
    
    if st.session_state.current_prompt is None:
        st.error("❌ No current prompt. Please add a prompt first.")
        return
    
    if response_text.strip():
        st.session_state.buffer.add_response(response_text)
        st.session_state.response_stack = list(st.session_state.buffer.responses.items)
        st.success(f"✅ Added response: '{response_text}'")
    else:
        st.error("❌ Please enter a valid response")


def undo_response():
    """Undo the most recent response"""
    if st.session_state.buffer is None:
        st.error("❌ Please create a conversation buffer first")
        return
    
    if st.session_state.buffer.responses.is_empty():
        st.warning("⚠️ No responses to undo")
        return
    
    undone_response = st.session_state.buffer.responses.peek()
    st.session_state.buffer.undo()
    st.session_state.response_stack = list(st.session_state.buffer.responses.items)
    st.warning(f"↩️ Undone: '{undone_response}'")


def finalize_conversation():
    """Finalize the current prompt-response pair"""
    if st.session_state.buffer is None:
        st.error("❌ Please create a conversation buffer first")
        return
    
    if st.session_state.current_prompt is None:
        st.error("❌ No current prompt to finalize")
        return
    
    if st.session_state.buffer.responses.is_empty():
        st.error("❌ No responses to finalize")
        return
    
    final_response = st.session_state.buffer.responses.peek()
    st.session_state.buffer.finalize()
    
    # Update session state
    st.session_state.current_prompt = None
    st.session_state.response_stack = []
    st.success(f"🔒 Finalized: '{final_response}'")


def show_history():
    """Display conversation history using the buffer's HISTORY command"""
    if st.session_state.buffer is None:
        st.error("❌ Please create a conversation buffer first")
        return
    
    # Use the buffer's history method
    st.session_state.buffer.history()


def run_demo_scenario():
    """Run the healthy recipe brainstorming demo scenario"""
    if st.session_state.buffer is None:
        st.error("❌ Please create a conversation buffer first")
        return
    
    # Demo scenario: Healthy recipe brainstorming
    st.info("🎬 Running Healthy Recipe Brainstorming Demo...")
    
    # Step 1: Add prompt
    st.session_state.buffer.add_prompt("Suggest a healthy salad")
    st.session_state.current_prompt = "Suggest a healthy salad"
    st.session_state.response_stack = []
    
    # Step 2: Add first response
    st.session_state.buffer.add_response("Caesar salad with croutons")
    st.session_state.response_stack = list(st.session_state.buffer.responses.items)
    
    # Step 3: UNDO (user says "Too many carbs!")
    st.session_state.buffer.undo()
    st.session_state.response_stack = list(st.session_state.buffer.responses.items)
    
    # Step 4: Add better response
    st.session_state.buffer.add_response("Kale salad with lemon dressing")
    st.session_state.response_stack = list(st.session_state.buffer.responses.items)
    
    # Step 5: FINALIZE
    st.session_state.buffer.finalize()
    st.session_state.current_prompt = None
    st.session_state.response_stack = []
    
    st.success("✅ Demo completed! Check the conversation history below.")


def get_buffer_status():
    """Get current buffer status"""
    if st.session_state.buffer is None:
        return {
            'context_window_size': 0,
            'finalized_pairs': 0,
            'current_prompt': None,
            'pending_responses': 0,
            'total_prompts': 0
        }
    
    return st.session_state.buffer.get_status()


def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="AI Conversation Buffer",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.title("🤖 AI Conversation Buffer")
    st.markdown("**Manage AI conversations with editing capabilities**")
    
    # Key Components Explanation
    with st.expander("📖 How it Works", expanded=False):
        st.markdown("""
        **Key Components:**
        - **User Prompts**: Stored in Queue (FIFO) - chronological order
        - **AI Responses**: Stored in Stack (LIFO) - allows UNDO of most recent
        - **Context Window (K)**: Limits active prompt-response pairs
        - **Commands**: UNDO, FINALIZE, HISTORY
        
        **Example Scenario:**
        1. Add prompt: "Suggest a healthy salad"
        2. Add response: "Caesar salad with croutons"
        3. Click UNDO (user says "Too many carbs!")
        4. Add response: "Kale salad with lemon dressing"
        5. Click FINALIZE (user approves)
        6. View HISTORY to see finalized pairs
        """)
    
    st.markdown("---")
    
    # Sidebar for controls
    with st.sidebar:
        st.header("🎛️ Controls")
        
        # Context window size
        st.subheader("Context Window")
        new_context_size = st.number_input(
            "Context Window Size (K)",
            min_value=1,
            max_value=10,
            value=st.session_state.context_size,
            help="Maximum number of prompt-response pairs to keep in memory"
        )
        
        if new_context_size != st.session_state.context_size:
            st.session_state.context_size = new_context_size
        
        # Create/Reset buffer
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🆕 Create Buffer", type="primary"):
                create_buffer()
        
        with col2:
            if st.button("🔄 Reset All"):
                st.session_state.buffer = None
                st.session_state.conversation_history = []
                st.session_state.current_prompt = None
                st.session_state.response_stack = []
                st.rerun()
        
        st.markdown("---")
        
        # Status display
        st.subheader("📊 Status")
        status = get_buffer_status()
        
        st.metric("Context Window", status['context_window_size'])
        st.metric("Finalized Pairs", status['finalized_pairs'])
        st.metric("Pending Responses", status['pending_responses'])
        
        if status['current_prompt']:
            st.info(f"**Current Prompt:** {status['current_prompt']}")
        else:
            st.info("No current prompt")
        
        st.markdown("---")
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        
        if st.button("↩️ UNDO", help="Remove the most recent response"):
            undo_response()
            st.rerun()
        
        if st.button("🔒 FINALIZE", help="Lock in the current prompt-response pair"):
            finalize_conversation()
            st.rerun()
        
        if st.button("📚 HISTORY", help="Show conversation history"):
            show_history()
        
        st.markdown("---")
        
        # Demo scenario
        st.subheader("🎬 Demo Scenario")
        if st.button("🍽️ Run Healthy Recipe Demo", help="Run the example scenario"):
            run_demo_scenario()
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("💬 Add Conversation")
        
        # Add prompt
        st.subheader("Add Prompt")
        prompt_text = st.text_area(
            "Enter your prompt:",
            placeholder="e.g., Suggest a healthy salad",
            height=100,
            key="prompt_input"
        )
        
        if st.button("➕ Add Prompt", type="primary"):
            add_prompt(prompt_text)
            st.rerun()
        
        st.markdown("---")
        
        # Add response
        st.subheader("Add Response")
        response_text = st.text_area(
            "Enter AI response:",
            placeholder="e.g., Kale salad with lemon dressing",
            height=100,
            key="response_input"
        )
        
        if st.button("🤖 Add Response"):
            add_response(response_text)
            st.rerun()
    
    with col2:
        st.header("📝 Current State")
        
        # Current prompt display
        if st.session_state.current_prompt:
            st.subheader("Current Prompt")
            st.info(f"**{st.session_state.current_prompt}**")
            
            # Response stack display (LIFO - Last In, First Out)
            if st.session_state.response_stack:
                st.subheader("Response Stack (LIFO - Last In, First Out)")
                st.caption("🟢 = Current (top of stack), ⚪ = Undone responses")
                
                # Show stack from top to bottom (most recent first)
                for i, response in enumerate(reversed(st.session_state.response_stack)):
                    status_icon = "🟢" if i == 0 else "⚪"
                    status_text = " (CURRENT)" if i == 0 else " (UNDONE)"
                    st.write(f"{status_icon} {response}{status_text}")
            else:
                st.info("No responses yet")
        else:
            st.info("No current prompt")
    
    # Conversation history
    st.markdown("---")
    st.header("📚 Conversation History")
    
    if st.session_state.buffer and st.session_state.buffer.finalized_pairs:
        st.subheader("Finalized Pairs (FIFO Order - Oldest to Newest)")
        for i, pair in enumerate(st.session_state.buffer.finalized_pairs, 1):
            with st.expander(f"Pair {i}: {pair['prompt'][:50]}...", expanded=False):
                st.write(f"**Prompt:** {pair['prompt']}")
                st.write(f"**Response:** {pair['response']}")
        
        # Show context window info
        st.info(f"📊 Context Window: {len(st.session_state.buffer.finalized_pairs)}/{st.session_state.buffer.K} pairs")
    else:
        st.info("No conversation history yet")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>AI Conversation Buffer System | Built with Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
