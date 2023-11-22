"""Module providing a function to graph the automata"""
import graphviz
from graphviz import Source


def storing_cfg():
    """Store the CFG data into a list"""

    with open("test_file.txt", "r", encoding="utf-8") as input_file:
        # Read file
        production_list = input_file.read().splitlines()
        input_file.close()

    return production_list


def storing_pda(production_list: list[str]):
    """Store the PDA data into a list"""

    state_list = ["1", "2", "3"]

    # Convert production list to pda lists
    # First step, append edge 0 -*,+!-> 1, edge 1 -*,+S-> 2
    tail_list = ["1", "2"]
    head_list = ["2", "3"]
    label_list = ["*,+!", "*,+S"]

    # Then, append the terminals
    for item in production_list:
        if any(char.islower() for char in item):
            for character in item:
                if character.islower():
                    tail_list.append("3")
                    head_list.append("3")
                    label_list.append(character + ",-" + character)

    # Then, append the loops
    count = 3
    for item in production_list:
        total = item.split("->")
        left_terminal = total[0].strip()
        right_terminal = total[1].strip()

        tail_list.append("3")
        count = count + 1
        label_list.append("*,-" + left_terminal)
        head_list.append(str(count))
        for terminal in right_terminal:
            tail_list.append(str(count))
            count = count + 1
            label_list.append("*,+" + terminal)
            head_list.append(str(count))

        # Take out the last head and loop back to state 3
        head_list.pop()
        head_list.append("3")

    # Finally, append the final state 3 -*,-!-> 4
    tail_list.append("3")
    head_list.append(str(count))
    label_list.append("*,-!")

    return [state_list, tail_list, head_list, label_list]


def graphing_pda(node_list: list):
    """Graph the PDA list into a graphviz data"""

    dot = graphviz.Digraph("pda-graph", comment="The Push-down Automata")
    dot.graph_attr["rankdir"] = "LR"
    dot.graph_attr["nodesep"] = "0.5"
    dot.node_attr["shape"] = "circle"
    state_list = node_list[0]
    tail_list = node_list[1]
    head_list = node_list[2]
    label_list = node_list[3]

    # Create nodes/states
    for index, state in enumerate(state_list):
        dot.node(state)

    # Create edges
    for index, label in enumerate(label_list):
        dot.edge(tail_list[index], head_list[index], label=label)

    # Display PDA file
    s = Source(dot.source, filename="pda.gv", format="pdf")
    s.view()


if __name__ == "__main__":
    productions = storing_cfg()
    nodes = storing_pda(productions)
    graphing_pda(nodes)
