A report on the final project for Theory of Computation Fall 2023

Author: Tan Nguyen

Tooling: Python version 3.10.11 and GraphViz library version 0.20.1

Sources: None

Required functions:
    main.py: A housing program that calling the other two functions for clarity

    cfg_to_pda.py: A program that convert a context-free grammar to push-down automata and graph it.
        storing_cfg(): Function to take in a text file and put each production into a list of string.
        storing_pda(): Function to convert each production in the list into a multiple list of states and transition lists of PDA in following steps:
            1. Make states [1, 2, 3], and initial edges: 0 -*,+!-> 1, 1 -*,+S-> 2.
            2. Add terminal production loops.
            3. Add non-terminal production loops.
            4. Add final state and edge: 3 -*,-!-> final state.
        graphing_pda(): Function to graph the PDA into a pdf file using the list of states and lists of transitions.

    cfg_to_cnf.py: A program that convert a context-free grammar to Chomsky Normal Forms.
        storing_cfg(): Function to take in a text file and put each production into a list of string.
        convert_cnf(): Function to convert each production into a Chomsky Normal Form in folowing steps:
            1. Separate the production in CNF and production that is not in CNF.
            2. Perform epsilon production reduction.
            3. Perform unit production reduction (chain, terminal, and redundant productions).
            4. Split multiple terminal productions into Chomsky Normal Forms.
            5. Turn any terminal into non-terminal and add more Chomsky Normal Forms.
            6. Split multiple non-terminal productions into Chomsky Normal Forms.
            Note: The additional non-terminal is labeled "Z" with an incremental number.
        printing_cnf(): Function to write the list of Chomsky Normal Form grammar into a file.

Status: 
    For the CFG to PDA program, the five tests does not produce any bugs.
    For the CFG to CNF, due to the naming scheme of additional non-terminal to have numerical number, if the actual terminal character is also a
    number, the program cannot terminate. Replace any numerical terminal with non-numerical character solves the problem.