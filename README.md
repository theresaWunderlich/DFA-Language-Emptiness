# CS 357 Project: DFA Language Emptiness Checker

This project implements an algorithm to determine if the language accepted by a given Deterministic Finite Automaton (DFA) is empty.

## Description

A DFA's language, L(M), is the set of all strings that the machine accepts. This language is considered **empty** if the DFA accepts no strings at all.

This program solves the emptiness problem by treating the DFA as a directed graph, where states are vertices and transitions are edges. The algorithm performs a graph traversal (specifically, a Breadth-First Search) starting from the DFA's start state to find all reachable states.

It then checks if this set of reachable states has any states in common with the DFA's set of accepting states.
* If the **intersection is empty**, no accept state is reachable, and the language is **empty**.
* If the **intersection is not empty**, at least one accept state is reachable, and the language is **not empty**.

## Requirements

* **Python 3.x**
* No external libraries are required. The program uses the built-in `json`, `sys`, and `collections.deque` modules.

## Usage

The program is executed from the command line. It requires a single argument: the file path to a JSON file representing the DFA.

```bash
python dfa_emptiness.py <path_to_dfa_file.json>
```

Upon successful execution, the program will:
1.  Print a confirmation message to the console (e.g., "Analysis complete. Language is not empty.").
2.  Generate a new JSON output file in the same directory, named `<input_file>_output.json`.

## Input File Format

The program requires the input file to be in JSON format, representing the DFA's 5-tuple. The root object must contain the following keys:

* `"states"`: An array of objects. Each object represents a state and must contain a `"state"` key for its name, as well as keys for each symbol in the alphabet to define transitions.
* `"alphabet"`: An array of strings, where each string is a symbol.
* `"start_state"`: A string that exactly matches the name of one of the defined states.
* `"accept_states"`: An array of objects, where each object contains a `"state"` key whose value is the name of an accepting state.

### Example Input (`test_case_1.json`)

[cite_start]This example corresponds to Test Case 1 from the project proposal [cite: 308-329].

```json
{
  "states": [
    {
      "state": "q0",
      "a": "q1",
      "b": "q0"
    },
    {
      "state": "q1",
      "a": "q1",
      "b": "q1"
    }
  ],
  "alphabet": ["a", "b"],
  "start_state": "q0",
  "accept_states": [
    {
      "state": "q1"
    }
  ]
}
```

## Output File Format

The program produces a single JSON output file containing a single key-value pair:

* `"language_is_empty"`: A boolean value (`true` or `false`).
    * `true`: No accept states are reachable from the start state.
    * `false`: At least one accept state is reachable.

### Example Output (`test_case_1_output.json`)

```json
{
  "language_is_empty": false
}
```

## Error Handling

The program will validate the input file and will terminate gracefully, printing a clear error message to the console (stderr) if any of the following conditions occur:

* The wrong number of command-line arguments is provided.
* The specified input file does not exist.
* The file is not a valid JSON document.
* The JSON object is missing any of the required keys (`"states"`, `"alphabet"`, `"start_state"`, `"accept_states"`).
* A state object in the `"states"` array is missing its `"state"` key.
* The specified `"start_state"` is not found in the list of states.
* A state listed in `"accept_states"` is not found in the list of states.