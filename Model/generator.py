"""
COMP4107 Final
.--------------.
| generator.py |
'--------------'
Short:
	File storing our model's generator

Long: 
	Creates a generator for all files found at the path provided.
	Input path must be a full path to one of the sub-folders found 
	inside the Data folder (i.e Training, Validation, or Testing)
	Uses all files in the folder as input data 

Author(s): 
	Jacob Schroeder 101151781
	Rohan Gulyani 101143438
"""
"""
# NOTE: Currently the generator is grabbing each data file as a batch, we will want to switch
		that to individual pokemon (not hard since we have the set up)
"""
import json
import os
import numpy as np
import tensorflow as tf
import numpy as np
from keras.models import Model

# Set path to reference this project's main folder
PATH = "/home/schroeds/Downloads/4107Final/"
BATCH_SIZE = 1

class PokemonGenerator(tf.keras.utils.Sequence):

  def __init__(self, data_type): # data_type is one of Training, Validation, or Testing
    self.dataset_filepath = os.path.join(PATH, data_type)
    self.batch_size = BATCH_SIZE
    self.input_files = os.listdir(self.dataset_filepath)
    self.input_count = len(self.input_files)
    self.indexes = np.arange(self.input_count)
    
    # Load all data source files needed on init so we don't have to keep opening/closing them
    self.item_encoding = json.load(open(os.path.join(PATH, "Pokedex", "itemEncoding.json")))
    self.ability_encoding = json.load(open(os.path.join(PATH, "Pokedex", "abilityEncoding.json")))
    self.move_encoding = json.load(open(os.path.join(PATH, "Pokedex", "moveEncoding.json")))
    self.type_encoding = json.load(open(os.path.join(PATH, "Pokedex", "typeEncoding.json")))
    self.pokedex = json.load(open(os.path.join(PATH, "Pokedex", "pokedex.json")))

  def __len__(self):
    return self.input_count // self.batch_size # Floor division ensures we always have enough data for batch

  def __getitem__(self, index):
    # index is the index of the batch to be retrieved

    batch_file = open(os.path.join(self.dataset_filepath, self.input_files[index]), mode="r")
    data = batch_file.readlines()
    pokemon = []
    y = []
    for line in data[5:65] # Shave off first 5 common lines and ensure only include the top 60 pokemon
    	pokemon.append(line.split("|")[2].strip())
    	y.append(float(line.split("|")[4].strip())) # Grab raw total usage occurances from data file

    x = []
    for mon in pokemon:
    	# Grab the pokemon's stats from the file
    	stats = [self.pokedex[mon]['hp'], 
    			 self.pokedex[mon]['atk'], 
    			 self.pokedex[mon]['def'], 
    			 self.pokedex[mon]['spa'], 
    			 self.pokedex[mon]['spd'], 
    			 self.pokedex[mon]['spe']]
    	
    	# Create a one-hot encoded array of length moves and encode the pokemon's moves
    	moves = np.zeros(len(self.move_encoding))
    	moveTypes = ["move1", "move2", "move3", "move4"]
    	for move in moveTypes:
    		if self.pokedex[mon][move] != "none":
    			moves[self.move_encoding[self.pokedex[mon][move]]] = 1

    	# Create a one-hot encoded array of length abilities and encode the pokemon's ability
    	ability = np.zeros(len(self.ability_encoding))
    	ability[self.ability_encoding[self.pokedex[mon]["ability"]]]
    	
    	# Create a one-hot encoded array of length abilities and encode the pokemon's ability
    	item = np.zeros(len(self.item_encoding))
    	item[self.item_encoding[self.pokedex[mon]["item"]]]
    	
		# Create a one-hot encoded array of length abilities and encode the pokemon's ability
    	types = np.zeros(len(self.type_encoding))
    	typeTypes = ["type1", "type2"]
    	for tipe in typeTypes:
    		if self.pokedex[mon][tipe] != "none":
    			types[self.type_encoding[self.pokedex[mon][tipe]]] = 1

    	xline = stats + moves + ability + item + types
    	x.append(xline)

    return x, y