"""
COMP4107 Final
.--------------.
| organizer.py |
'--------------'
Short:
	Convert the data sets we had available to us into
	a dataset which is usable for our model 

Long: 
	First creates a dictionary of all pokemon names, types,
	and stats found in statDex.json, then reads through setDex.json
	and fills the afformentioned csv with all relevant pokemon's
	abilities, moves, and held item. Finally we compound a full
	list of types, moves, held items, and abilities, and use it to
	convert those qualitative values, to useful quantatative values. 

Author(s): 
	Jacob Schroeder 101151781
	Rohan Gulyani 101143438
"""

import json

STATDEX = 'statDex.json'
SETDEX = 'setDex.json'
POKEDEX = 'pokedex.json'

def main():
	dct = readSetDex(SETDEX, readStatDex(STATDEX))
	with open(POKEDEX, "w") as f:
		json.dump(dct, f)

def readSetDex(fname, statDct):
	"""
	readStatDex - Produce a dictonary of all useful information in SETDEX

	in: 
		fname - file name to read data from
		dct - dictionary produced by readStatDex

	out:
		dct - dictonary with all relevant pokemon's relevant information
			for our model
	"""
	# Open json file
	f = open(fname)
	data = json.load(f)

	# Create and fill output dict
	dct = {}
	for name in data:
		dct[name] = statDct[name] # Only fill final dct up with pokemon found in both lists

		# Some sets provide more than one "role" for each pokemon, we select the first
		# one aribitrarily as these different sets have a lot of overlap
		roleUsed = ''
		for role in data[name]['roles']:
			roleUsed = role
			break

		# Not all Pokemon have 4 moves (Ex: Ditto can only learn 1)
		moves = data[name]['roles'][roleUsed]['moves']
		if len(moves) < 4:
			for i in range(4-len(moves)):
				moves.append("none")

		# Not all Pokemon have an item
		if not 'items' in data[name]['roles'][roleUsed]:
			item = 'none'
		else:
			item = data[name]['roles'][roleUsed]['items'][0]

		dct[name]["ability"] = data[name]['roles'][roleUsed]['abilities'][0] # Only add the ability used in the role
		dct[name]["move1"] = moves[0]
		dct[name]["move2"] = moves[1]
		dct[name]["move3"] = moves[2]
		dct[name]["move4"] = moves[3]
		dct[name]["item"] = item

	return dct

def readStatDex(fname):
	"""
	readStatDex - Produce a dictonary of all useful information in STATDEX

	in: 
		fname - file name to read data from

	out:
		dct - dictonary with keys of each pokemon's name, corresponding
			to their type(s) and stats
	"""
	# Open json file
	f = open(fname)
	data = json.load(f)
	
	# Create and fill output dict
	dct = {}
	for i in data:
		
		# Not all Pokemon have two types
		types = data[i]['types']		
		if len(types) < 2:
			type2 = "none"
		else:
			type2 = types[1]
		type1 = types[0] 

		# Fill all relevant information
		dct[data[i]['name']] = {
			"type1": type1, 
			"type2": type2, 
			"hp":  data[i]['baseStats']['hp'], 
			"atk": data[i]['baseStats']['atk'], 
			"def": data[i]['baseStats']['def'], 
			"spa": data[i]['baseStats']['spa'], 
			"spd": data[i]['baseStats']['spd'], 
			"spe": data[i]['baseStats']['spe']}

	return dct

# For redundancy
if __name__ == "__main__":
	main()