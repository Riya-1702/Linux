import streamlit as st
import subprocess
import os
import sys
import tempfile
import shlex
from datetime import datetime

# Configure page


# Initialize session state
if 'command_history' not in st.session_state:
    st.session_state.command_history = []

def execute_safe_command(command):
    """Execute safe Linux commands and return output"""
    # List of safe commands that can be executed
    safe_commands = {
        'ls', 'pwd', 'whoami', 'date', 'cal', 'uptime', 'id', 'w', 'who',
        'df', 'free', 'uname', 'ps', 'echo', 'cat', 'head', 'tail', 'wc',
        'sort', 'uniq', 'grep', 'find', 'which', 'locate', 'history'
    }
    
    try:
        # Parse the command
        cmd_parts = shlex.split(command.strip())
        if not cmd_parts:
            return "No command entered"
        
        base_cmd = cmd_parts[0]
        
        # Handle special cases
        if base_cmd == 'clear':
            return "Terminal cleared (simulated)"
        
        if base_cmd == 'history':
            return "\n".join([f"{i+1}: {cmd}" for i, cmd in enumerate(st.session_state.command_history[-10:])])
        
        if base_cmd == 'help':
            return "Available commands: " + ", ".join(sorted(safe_commands))
        
        # Check if command is in safe list
        if base_cmd not in safe_commands:
            return f"Command '{base_cmd}' is not available in this simulator for security reasons.\nUse 'help' to see available commands."
        
        # Special handling for some commands
        if base_cmd == 'cat':
            if len(cmd_parts) > 1:
                # Create temporary file for demonstration
                with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
                    f.write("This is a sample file content.\nLine 2 of the file.\nLine 3 of the file.")
                    temp_path = f.name
                
                try:
                    result = subprocess.run(['cat', temp_path], capture_output=True, text=True, timeout=5)
                    os.unlink(temp_path)
                    return result.stdout if result.returncode == 0 else result.stderr
                except:
                    os.unlink(temp_path)
                    return "Sample file content:\nThis is a sample file content.\nLine 2 of the file.\nLine 3 of the file."
            else:
                return "Usage: cat [filename]"
        
        if base_cmd == 'echo':
            return ' '.join(cmd_parts[1:]) if len(cmd_parts) > 1 else ""
        
        # Execute the command
        result = subprocess.run(cmd_parts, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            return result.stdout.strip() if result.stdout.strip() else "Command executed successfully (no output)"
        else:
            return f"Error: {result.stderr.strip()}"
            
    except subprocess.TimeoutExpired:
        return "Command timed out"
    except Exception as e:
        return f"Error executing command: {str(e)}"

# Main page - Interactive Terminal
st.title("Interactive Linux Terminal")
st.write("Practice Linux commands in a safe environment!")

# Create two columns
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Terminal")
    
    # Command input
    command = st.text_input(
        "Enter Linux command:",
        placeholder="e.g., ls -la, pwd, whoami",
        help="Type a Linux command and press Enter to execute"
    )
    
    if st.button("Execute Command") or command:
        if command.strip():
            # Add to history
            st.session_state.command_history.append(command)
            
            # Execute command
            with st.spinner("Executing command..."):
                output = execute_safe_command(command)
            
            # Display command and output
            st.code(f"$ {command}", language="bash")
            st.text_area("Output:", output, height=200, disabled=True)
    
    # Command history
    if st.session_state.command_history:
        st.subheader("Command History")
        with st.expander("View recent commands"):
            for i, cmd in enumerate(reversed(st.session_state.command_history[-10:]), 1):
                if st.button(f"{cmd}", key=f"history_{i}"):
                    st.rerun()

with col2:
    st.subheader("Quick Commands")
    st.write("Click to try these commands:")
    
    quick_commands = [
        "pwd", "whoami", "date", "ls", "df -h", "free -h", 
        "uname -a", "uptime", "ps aux", "echo 'Hello Linux!'"
    ]
    
    for cmd in quick_commands:
        if st.button(f"`{cmd}`", key=f"quick_{cmd}".replace(" ", "_").replace("-", "_").replace("`", "")):
            st.session_state.command_history.append(cmd)
            output = execute_safe_command(cmd)
            st.code(f"$ {cmd}", language="bash")
            st.text(output)