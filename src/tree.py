import json
import os

class Node:
    def __init__(self, question=None, yes=None, no=None, plant=None):
        self.question = question
        self.yes = yes
        self.no = no
        self.plant = plant

def tree(remaining_plants):
    if len(remaining_plants) == 1:
        return Node(plant=remaining_plants[0]["name"])
    if len(remaining_plants) == 0:
        return None
        
    first = remaining_plants[0]
    next_trait = list(first["traits"].keys())[0]
    expected = first["traits"][next_trait]
    clean = next_trait.replace("_", " ")
    question = f"Is the {clean} '{expected}'?"
    
    yes_plants = []
    no_plants = []
    
    for plant in remaining_plants:
        remaining_traits = {k: v for k, v in plant["traits"].items() if k != next_trait}
        updated_plant = {"name": plant["name"], "traits": remaining_traits}
        
        if plant["traits"].get(next_trait) == expected:
            yes_plants.append(updated_plant)
        else:
            no_plants.append(updated_plant)
            
    return Node(
        question = question,
        yes = tree(yes_plants),
        no = tree(no_plants)
    )

def ask(question_text):
    while True:
        answer = input(question_text + " (yes/no): ").strip().lower()
        if answer in ["yes", "no"]:
            return answer
        else:
            print("Please answer 'yes' or 'no'.")

def identify(node, observations):
    if node.plant is not None:
        return node.plant
        
    answer = ask(node.question)
    if answer == "yes":
        return identify(node.yes, observations)
    else:
        return identify(node.no, observations)

if __name__ == "__main__":
    # 1. Get the absolute directory where tree.py lives
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 2. Build the precise path up one level to the data folder
    file_path = os.path.abspath(os.path.join(script_dir, "..", "data", "austin_plants.json"))
    with open(file_path, "r") as f:
        austin_plants_data = json.load(f)

    root_node = tree(austin_plants_data["plants"])
    observations = {}
    identified_plant = identify(root_node, observations)

    if identified_plant:
        print(f"The most likely identified plant is: {identified_plant}")
    else:
        print("Could not identify the plant.")
