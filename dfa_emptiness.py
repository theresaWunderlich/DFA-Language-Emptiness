import json
import sys
from collections import deque

def main():
    """Main function to coordinate program execution."""
    if len(sys.argv) != 2:
        print("Error: Invalid number of arguments", file=sys.stderr)
        print("Usage: python dfa_emptiness.py <input_file.json>", file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        # Load and parse the DFA from input file
        states, transitions, start_state, accept_states = getDFA(input_file)
        
        # Find all reachable states from start state
        reachable = findReachableStates(states, transitions, start_state)
        
        # Check if language is empty
        is_empty = isLanguageEmpty(reachable, accept_states)
        
        # Generate output file
        generateOutput(is_empty, input_file)
        
        print(f"Analysis complete. Language is {'empty' if is_empty else 'not empty'}.")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def getDFA(input_file):
    """
    Load and parse the DFA from the input JSON file.
    
    Args:
        input_file: Path to the input JSON file
        
    Returns:
        tuple: (states, transitions, start_state, accept_states)
            - states: set of state names
            - transitions: dict mapping (state, symbol) -> next_state
            - start_state: name of start state
            - accept_states: set of accept state names
    """
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        raise Exception(f"Input file '{input_file}' does not exist")
    except json.JSONDecodeError:
        raise Exception("Input file is not valid JSON")
    
    # Validate required keys
    required_keys = ["states", "alphabet", "start_state", "accept_states"]
    for key in required_keys:
        if key not in data:
            raise Exception(f"Input file is missing required key: '{key}'")
    
    # Extract states
    states = set()
    transitions = {}
    
    for state_obj in data["states"]:
        if "state" not in state_obj:
            raise Exception("State object missing 'state' key")
        
        state_name = state_obj["state"]
        states.add(state_name)
        
        # Extract transitions for this state
        for symbol in data["alphabet"]:
            if symbol in state_obj:
                next_state = state_obj[symbol]
                transitions[(state_name, symbol)] = next_state
    
    # Extract start state
    start_state = data["start_state"]
    if start_state not in states:
        raise Exception(f"Start state '{start_state}' not in states")
    
    # Extract accept states
    accept_states = set()
    for accept_obj in data["accept_states"]:
        if "state" not in accept_obj:
            raise Exception("Accept state object missing 'state' key")
        accept_state = accept_obj["state"]
        if accept_state not in states:
            raise Exception(f"Accept state '{accept_state}' not in states")
        accept_states.add(accept_state)
    
    return states, transitions, start_state, accept_states

def findReachableStates(states, transitions, start_state):
    """
    Find all states reachable from the start state using BFS.
    
    Args:
        states: set of all state names
        transitions: dict mapping (state, symbol) -> next_state
        start_state: name of start state
        
    Returns:
        set: all states reachable from start_state
    """
    reachable = set()
    queue = deque([start_state])
    reachable.add(start_state)
    
    while queue:
        current_state = queue.popleft()
        
        # Check all possible transitions from current state
        for (state, symbol), next_state in transitions.items():
            if state == current_state and next_state not in reachable:
                reachable.add(next_state)
                queue.append(next_state)
    
    return reachable

def isLanguageEmpty(reachable_states, accept_states):
    """
    Determine if the DFA's language is empty.
    
    Args:
        reachable_states: set of states reachable from start state
        accept_states: set of accept states
        
    Returns:
        bool: True if language is empty, False otherwise
    """
    # Language is empty if no accept state is reachable
    intersection = reachable_states.intersection(accept_states)
    return len(intersection) == 0

def generateOutput(is_empty, input_file):
    """
    Generate the output JSON file with the result.
    
    Args:
        is_empty: boolean indicating if language is empty
        input_file: path to input file (used to create output filename)
    """
    output_data = {
        "language_is_empty": is_empty
    }
    
    # Create output filename based on input filename
    if input_file.endswith('.json'):
        output_file = input_file[:-5] + '_output.json'
    else:
        output_file = input_file + '_output.json'
    
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"Output written to: {output_file}")

if __name__ == "__main__":
    main()