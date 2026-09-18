import json

with open("data/biodiversity_knowledge.json", "r") as file:
    knowledge = json.load(file)

print(knowledge)