"""
COMP4107 Final
.-----------.
| sanity.py |
'-----------'
Short:
	Ensures all pokemon referenced in the data files exist in pokedex.json

Long: 
	Reads the names of the top 60 pokemon in each usage statistic file, then
	checks the file contents of pokedex.json to ensure that there is an entry
	for that specific file. Does this for all data files we use so that we
	ensure we are not missing information on any pokemon we may encounter.

Author(s): 
	Jacob Schroeder 101151781
	Rohan Gulyani 101143438
"""

import json
import os

# Set path to reference this project's main folder
PATH = "/home/schroeds/Downloads/4107Final/"

def read_file(file_path):
	f = open(file_path, "r")
	data = f.readlines()
	pokemon = []
	for line in data[5:65]: # Shave the first 5 lines common to all files
		pokemon.append(line.split("|")[2].strip())
	return pokemon

def main():
	f = open(os.path.join(PATH, "Pokedex", "pokedex.json"))
	dex = json.load(f)
	insane = False

	for folder in os.listdir(os.path.join(PATH, "Data")):
		if not os.path.isfile(os.path.join(PATH, "Data", folder)):
			for file in os.listdir(os.path.join(PATH, "Data", folder)):
				pokemon = read_file(os.path.join(PATH, "Data", folder, file))
				for mon in pokemon:
					if mon not in dex:
						print(f"ERROR: Unable to find {mon} in {folder}/{file}!")
						insane = True
	if not insane:
		print("All Pokemon found, no issues in the data to report!")

# For redundancy
if __name__ == "__main__":
	main()