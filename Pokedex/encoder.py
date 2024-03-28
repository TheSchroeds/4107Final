"""
COMP4107 Final
.------------.
| encoder.py |
'------------'
Short:
	Fills all encoding files with usable mappings for all qualatative data

Long: 
	Loads the pokedex.json file then reads through all data, noting all unique
	items, moves, type, and abilities that it finds. It uses this data to fill all the
	Encoding.json files with dictonaries which map the qualatative input data to
	an array position which then can be later used to one-hot encode all our qualatative
	data. This ensures that the positions of our hot-hot encoded values do not change.

Author(s): 
	Jacob Schroeder 101151781
	Rohan Gulyani 101143438
"""

import json
import os

# Set path to reference this project's main folder
PATH = "/home/schroeds/Downloads/4107Final/"

def main():
	dex = read_pokedex()
	
	items = fill_items(dex)
	with open(os.path.join(PATH, "Pokedex", "itemEncoding.json"), mode="w") as it:
		json.dump(items, it)

	moves = fill_moves(dex)
	with open(os.path.join(PATH, "Pokedex", "moveEncoding.json"), mode="w") as mo:
		json.dump(moves, mo)

	abilities = fill_abilities(dex)
	with open(os.path.join(PATH, "Pokedex", "abilityEncoding.json"), mode="w") as ab:
		json.dump(abilities, ab)

	types = fill_types(dex)
	with open(os.path.join(PATH, "Pokedex", "typeEncoding.json"), mode="w") as ty:
		json.dump(types, ty)

	print("The following information can be used to set the lengths of the one-hot encoded arrays")
	print(f"Items: Total={len(items)}")
	print(f"Moves: Total={len(moves)}")
	print(f"Abilities: Total={len(abilities)}")
	print(f"Types: Total={len(types)}")

def read_pokedex():
	f = open(os.path.join(PATH, "Pokedex", "pokedex.json"))
	dex = json.load(f)
	return dex

def fill_items(dex):
	items = {}
	index = 0

	for pokemon in dex:
		if dex[pokemon]["item"] != "none" and dex[pokemon]["item"] not in items:
			items[dex[pokemon]["item"]] = index
			index += 1
	
	return items

def fill_moves(dex):
	moves = {}
	index = 0
	moveTypes = ["move1", "move2", "move3", "move4"]

	for pokemon in dex:
		for move in moveTypes:
			if dex[pokemon][move] != "none" and dex[pokemon][move] not in moves:
				moves[dex[pokemon][move]] = index
				index += 1

	return moves

def fill_abilities(dex):
	abilities = {}
	index = 0

	for pokemon in dex:
		if dex[pokemon]["ability"] != "none" and dex[pokemon]["ability"] not in abilities:
			abilities[dex[pokemon]["ability"]] = index
			index += 1
	
	return abilities

def fill_types(dex):
	types = {}
	index = 0
	typetypes = ["type1", "type2"]

	for pokemon in dex:
		for tipe in typetypes:
			if dex[pokemon][tipe] != "none" and dex[pokemon][tipe] not in types:
				types[dex[pokemon][tipe]] = index
				index += 1

	return types

# For redundancy
if __name__ == "__main__":
	main()