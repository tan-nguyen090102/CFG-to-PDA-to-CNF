"""Module providing a function to graph the push-down automata from context-free grammar"""
import graphviz
from graphviz import Source


class CFGToPDA:
    """Class to convert CFG to PDA"""

    def __init__(self) -> None:
        self.special_characters = "!@#$%^&*()+?_=,"

    def storing_cfg(self):
        """Store the CFG data into a list"""

        with open("test_file.txt", "r", encoding="utf-8") as input_file:
            # Read file
            production_list = input_file.read().splitlines()
            input_file.close()

        return production_list

    def storing_pda(self, production_list: list[str]):
        """Store the PDA data into a list"""

        state_list = ["1", "2", "3"]

        # Convert production list to pda lists
        # First, append edge 0 -*,+!-> 1, edge 1 -*,+S-> 2
        tail_list = ["1", "2"]
        head_list = ["2", "3"]
        label_list = ["*, +!", "*, +S"]

        # Then, append the terminal productions
        for item in production_list:
            if any(char.islower() for char in item) or any(
                char in self.special_characters for char in item
            ):
                for character in item:
                    if character.islower() or character in self.special_characters:
                        tail_list.append("3")
                        head_list.append("3")
                        label_list.append(character + ", -" + character)

        # Then, append the loop productions
        count = 3
        for item in production_list:
            total = item.split("->")
            left_non_terminal = total[0].strip()
            right_non_terminal = total[1].strip()

            # If the terminal is epsilon, ignore the production
            if right_non_terminal == "":
                production_list.remove(item)
                break

            tail_list.append("3")
            count = count + 1
            state_list.append(str(count))
            label_list.append("*, -" + left_non_terminal)
            head_list.append(str(count))
            for non_terminal in right_non_terminal:
                tail_list.append(str(count))
                count = count + 1
                state_list.append(str(count))
                label_list.append("*, +" + non_terminal)
                head_list.append(str(count))

            # Take out the last head and loop back to state 3
            head_list.pop()
            state_list.pop()
            head_list.append("3")

        # Finally, append the edge 3 -*,-!-> final state
        tail_list.append("3")
        head_list.append(str(count))
        state_list.append(str(count))
        label_list.append("*, -!")

        return [state_list, tail_list, head_list, label_list]

    def graphing_pda(self, node_list: list):
        """Graph the PDA list into a graphviz data"""

        dot = graphviz.Digraph("pda-graph", comment="The Push-down Automata")
        dot.graph_attr["rankdir"] = "LR"
        dot.graph_attr["nodesep"] = "0.5"
        dot.graph_attr["splines"] = "true"
        dot.graph_attr["overlap"] = "scale"
        dot.graph_attr["ranksep"] = "2.5"
        dot.node_attr["shape"] = "circle"
        state_list = node_list[0]
        tail_list = node_list[1]
        head_list = node_list[2]
        label_list = node_list[3]

        # Create starting arrow
        dot.node("hidden", shape="plaintext", label="")
        dot.edge("hidden", "1")

        # Create nodes/states
        for index, state in enumerate(state_list):
            if state_list[index] == state_list[len(state_list) - 1]:
                dot.attr("node", shape="doublecircle")
                dot.node(state)
            else:
                dot.attr("node", shape="circle")
                dot.node(state)

        # Create edges
        for index, label in enumerate(label_list):
            dot.edge(tail_list[index], head_list[index], label=label)

        # Display PDA file
        s = Source(dot.source, filename="pda.gv", format="pdf")
        s.view()
