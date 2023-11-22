class CFGToCNF:
    """Class to convert CFG to CNF"""

    def __init__(self, file_path: str) -> None:
        self.special_characters = "!@#$%^&*()+?_=,"
        self.file_path = file_path

    def storing_cfg(self):
        """Store the CFG data into a list"""

        with open(self.file_path, "r", encoding="utf-8") as input_file:
            # Read file
            production_list = input_file.read().splitlines()
            input_file.close()

        return production_list

    def convert_to_cnf(self, production_list: list[str]):
        """Convert CFG to CNF"""
        cnf_list: list[str] = []

        # First, separate the production in CNF and production is not in CNF
        for item in production_list:
            total = item.split("->")
            right_non_terminal = total[1].strip()

            if len(right_non_terminal) == 1 and right_non_terminal.islower():
                cnf_list.append(item)
                continue

            if len(right_non_terminal) == 2 and right_non_terminal.isupper():
                cnf_list.append(item)
                continue

        production_list = [item for item in production_list if item not in cnf_list]

        # Then, perform epsilon production reduction
        for item in production_list:
            total = item.split("->")
            left_non_terminal = total[0].strip()
            right_non_terminal = total[1].strip()

            if right_non_terminal == "":
                for middle_production in production_list:
                    whole = middle_production.split("->")
                    left_middle = whole[0].strip()
                    right_middle = whole[1].strip()
                    if (
                        right_middle.find(left_non_terminal) != -1
                        and len(right_middle) == 3
                        and right_middle.index(left_non_terminal) == 1
                        and right_middle[0].islower()
                        and right_middle[2].islower()
                    ):
                        right_middle = right_middle.replace(left_non_terminal, "", 1)
                        new_production = left_middle + " -> " + right_middle
                        production_list.append(new_production)
                        production_list.remove(middle_production)
                        continue
        production_list.remove(item)

        # Then, perform unit production reduction
        indirect_list = []
        removed_production: list[str] = []
        # Reduce chain unit production
        for item in production_list:
            total = item.split("->")
            left_non_terminal = total[0].strip()
            right_non_terminal = total[1].strip()

            if len(right_non_terminal) == 1 and right_non_terminal.isupper():
                indirect_list.append(item)
                production_list.remove(item)

                for middle_production in production_list:
                    whole = middle_production.split("->")
                    left_middle = whole[0].strip()
                    right_middle = whole[1].strip()

                    if len(right_middle) == 1 and left_middle == right_non_terminal:
                        new_production = left_non_terminal + " -> " + right_middle
                        production_list.remove(middle_production)
                        production_list.append(new_production)
                        indirect_list.pop()

                if len(indirect_list) > 0:
                    production_list.extend(indirect_list)
                    indirect_list.clear()

        # Reduce the terminal unit production
        removed_production.clear()
        for item in production_list:
            total = item.split("->")
            left_non_terminal = total[0].strip()
            right_non_terminal = total[1].strip()

            if len(right_non_terminal) == 1 and right_non_terminal.isupper():
                indirect_list.append(item)
                production_list.remove(item)

                for middle_production in cnf_list:
                    whole = middle_production.split("->")
                    left_middle = whole[0].strip()
                    right_middle = whole[1].strip()

                    if len(right_middle) == 1 and left_middle == right_non_terminal:
                        new_production = left_non_terminal + " -> " + right_middle
                        cnf_list.append(new_production)
                        removed_production.append(middle_production)
                        indirect_list.pop()
                        break

                if len(indirect_list) > 0:
                    production_list.extend(indirect_list)
                    indirect_list.clear()

        cnf_list = [item for item in cnf_list if item not in removed_production]

        # Remove redundant unit production
        removed_production.clear()
        for item in production_list:
            total = item.split("->")
            left_non_terminal = total[0].strip()
            right_non_terminal = total[1].strip()

            if len(right_non_terminal) == 1 and right_non_terminal.isupper():
                removed_production.append(item)

        production_list = [
            item for item in production_list if item not in removed_production
        ]

        # Then, split multiple terminal productions into single ones
        count = 1
        removed_production.clear()
        for item in production_list:
            total = item.split("->")
            left_non_terminal = total[0].strip()
            right_non_terminal = total[1].strip()

            if right_non_terminal.islower():
                new_main_production = left_non_terminal + " -> "
                for index, character in enumerate(right_non_terminal):
                    count = count + 1
                    new_production = "Z" + str(count) + " -> " + character
                    new_main_production += "Z" + str(count)
                    cnf_list.append(new_production)

                removed_production.append(item)
                cnf_list.append(new_main_production)

        cnf_list = list(set(cnf_list))
        production_list = [
            item for item in production_list if item not in removed_production
        ]
        removed_production.clear()

        # Then, turns any terminal into terminal production
        removed_production.clear()
        add_production: list[str] = []
        in_change = False
        for item in production_list:
            total = item.split("->")
            left_non_terminal = total[0].strip()
            right_non_terminal = total[1].strip()

            for character in right_non_terminal:
                new_main_production = left_non_terminal + " -> " + right_non_terminal
                if character.islower() or character in self.special_characters:
                    in_change = True
                    count += 1
                    new_production = "Z" + str(count) + " -> " + character
                    cnf_list.append(new_production)
                    new_main_production = new_main_production.replace(
                        character, "Z" + str(count)
                    )
                    right_non_terminal = new_main_production.split("->")[1].strip()

            if in_change is True:
                add_production.append(new_main_production)
                removed_production.append(item)

        production_list = [
            item for item in production_list if item not in removed_production
        ]

        production_list.extend(add_production)
        add_production.clear()
        removed_production.clear()

        # Finally, split the multiple non-terminals into many non-terminals productions
        while len(production_list) != 0:
            current_count = count
            for index, item in enumerate(production_list):
                total = item.split("->")
                left_non_terminal = total[0].strip()
                right_non_terminal = total[1].strip()

                if len(right_non_terminal) > 2:
                    for index, character in enumerate(
                        right_non_terminal[0 : len(right_non_terminal) - 1]
                    ):
                        # Handle Z terminal in the middle
                        if (
                            character == "Z"
                            and (index != 0)
                            and not character.isnumeric()
                        ):
                            number = ""
                            for numeric in right_non_terminal[
                                index + 1 : len(right_non_terminal)
                            ]:
                                if numeric.isnumeric():
                                    number += numeric
                                    continue
                                else:
                                    break
                            current_count = int(number)
                            count += 1
                            new_right = right_non_terminal[
                                index : len(right_non_terminal)
                            ]
                            new_production = (
                                left_non_terminal
                                + " -> "
                                + right_non_terminal[index - 1]
                                + "Z"
                                + str(count)
                            )
                            cnf_list.append(new_production)
                            left_non_terminal = "Z" + str(count)
                            new_main_production = left_non_terminal + " -> " + new_right

                            # Check if the remain production is in CNF
                            if (
                                len(
                                    "".join(
                                        char for char in new_right if not char.isdigit()
                                    )
                                )
                                == 2
                            ):
                                cnf_list.append(new_main_production)
                                removed_production.append(item)
                            else:
                                add_production.append(new_main_production)
                                removed_production.append(item)

                            production_list.extend(add_production)
                            production_list = [
                                item
                                for item in production_list
                                if item not in removed_production
                            ]
                            add_production.clear()
                            break

                        # Handle Z terminal on the left
                        if (
                            character == "Z"
                            and index == 0
                            and not character.isnumeric()
                        ):
                            number = ""
                            for numeric in right_non_terminal[
                                index + 1 : len(right_non_terminal)
                            ]:
                                if numeric.isnumeric():
                                    number += numeric
                                else:
                                    break
                            current_count = int(number)
                            count += 1
                            new_production = (
                                left_non_terminal
                                + " -> "
                                + "Z"
                                + str(current_count)
                                + "Z"
                                + str(count)
                            )
                            left_non_terminal = "Z" + str(count)
                            new_right = right_non_terminal[
                                index + len(number) + 1 : len(right_non_terminal)
                            ]
                            new_main_production = left_non_terminal + " -> " + new_right

                            # Check if the remain production is in CNF
                            cnf_list.append(new_production)
                            if (
                                len(
                                    "".join(
                                        char for char in new_right if not char.isdigit()
                                    )
                                )
                                == 2
                            ):
                                cnf_list.append(new_main_production)
                                removed_production.append(item)
                            else:
                                add_production.append(new_main_production)
                                removed_production.append(item)

                            production_list.extend(add_production)
                            production_list = [
                                item
                                for item in production_list
                                if item not in removed_production
                            ]
                            add_production.clear()
                            break

                        # Handle multiples normal non-terminal
                        if (
                            character != "Z"
                            and (index != 0)
                            and not character.isnumeric()
                        ):
                            current_count = count
                            count += 1
                            new_right = right_non_terminal[
                                index : len(right_non_terminal)
                            ]
                            new_production = (
                                left_non_terminal
                                + " -> "
                                + right_non_terminal[index - 1]
                                + "Z"
                                + str(count)
                            )
                            cnf_list.append(new_production)
                            left_non_terminal = "Z" + str(count)
                            new_main_production = left_non_terminal + " -> " + new_right

                            # Check if the remain production is in CNF
                            if (
                                len(
                                    "".join(
                                        char for char in new_right if not char.isdigit()
                                    )
                                )
                                == 2
                            ):
                                cnf_list.append(new_main_production)
                                removed_production.append(item)
                            else:
                                add_production.append(new_main_production)
                                removed_production.append(item)

                            production_list.extend(add_production)
                            production_list = [
                                item
                                for item in production_list
                                if item not in removed_production
                            ]
                            add_production.clear()
                            break

        return cnf_list

    def printing_cnf(self, cnf_list: list[str]):
        """Print out the CNF"""

        with open("result_cnf.txt", "w", encoding="utf-8") as output_file:
            for item in cnf_list:
                output_file.write(item + "\n")

            output_file.close()
