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
BATCH_SIZE = 4

class PokemonGenerator(tf.keras.utils.Sequence):

	def __init__(self, data_type): # data_type is one of Training, Validation, or Testing
		self.dataset_filepath = os.path.join(PATH, "Data", data_type)
		self.batch_size = BATCH_SIZE
		self.input_files = os.listdir(self.dataset_filepath)
		self.input_count = len(self.input_files)
		self.indexes = np.arange(self.input_count)

		# Create a dictonary containing the total pokemon usages for the top 60 pokemon in a file
		self.usage_totals = {}
		file_num = 0
		for file in self.input_files:
			data = open(os.path.join(self.dataset_filepath, file)).readlines()
			cur_tot = 0
			for line in data[5:65]:
				cur_tot += float(line.split("|")[4].strip())
			self.usage_totals[file_num] = cur_tot
			file_num += 1
		
		# Load all data source files needed on init so we don't have to keep opening/closing them
		self.item_encoding = json.load(open(os.path.join(PATH, "Pokedex", "itemEncoding.json")))
		self.ability_encoding = json.load(open(os.path.join(PATH, "Pokedex", "abilityEncoding.json")))
		self.move_encoding = json.load(open(os.path.join(PATH, "Pokedex", "moveEncoding.json")))
		self.type_encoding = json.load(open(os.path.join(PATH, "Pokedex", "typeEncoding.json")))
		self.pokedex = json.load(open(os.path.join(PATH, "Pokedex", "pokedex.json")))

	def __len__(self):
		# # of input files * # of pokemon used in each file (60) / batch size
		return self.input_count * 60 // self.batch_size # Floor division ensures we always have enough data for batch

	def __getitem__(self, index):
		# index is the index of the batch to be retrieved

		line_index = index % (60 // self.batch_size)
		file_index = index // (60 // self.batch_size)

		batch_file = open(os.path.join(self.dataset_filepath, self.input_files[file_index]), mode="r")
		data = batch_file.readlines()
		pokemon = []
		y = []
		for line in data[line_index + 5 : line_index + 5 + self.batch_size]: # Shave off first 5 common lines and ensure only include the top 60 pokemon
			pokemon.append(line.split("|")[2].strip())
			y.append(float(line.split("|")[4].strip()) / self.usage_totals[file_index]) # Normalize usage to range 0-1 using total usage in file

		x = []
		for mon in pokemon:
			# Grab the pokemon's stats from the file (255 is the max size for any stat)
			stats = [self.pokedex[mon]['hp']/255, 
					 self.pokedex[mon]['atk']/255, 
					 self.pokedex[mon]['def']/255, 
					 self.pokedex[mon]['spa']/255, 
					 self.pokedex[mon]['spd']/255, 
					 self.pokedex[mon]['spe']/255]
			
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

			xline = np.concatenate((stats, moves, ability, item, types))
			x.append(xline)
		return np.array(x), np.array(y)

class PokemonGeneratorEncoder(tf.keras.utils.Sequence):

	def __init__(self, data_type): # data_type is one of Training, Validation, or Testing
		self.dataset_filepath = os.path.join(PATH, "Data", data_type)
		self.batch_size = BATCH_SIZE
		self.input_files = os.listdir(self.dataset_filepath)
		self.input_count = len(self.input_files)
		self.indexes = np.arange(self.input_count)

		# Create a dictonary containing the total pokemon usages for the top 60 pokemon in a file
		self.usage_totals = {}
		file_num = 0
		for file in self.input_files:
			data = open(os.path.join(self.dataset_filepath, file)).readlines()
			cur_tot = 0
			for line in data[5:65]:
				cur_tot += float(line.split("|")[4].strip())
			self.usage_totals[file_num] = cur_tot
			file_num += 1
		
		# Load all data source files needed on init so we don't have to keep opening/closing them
		self.item_encoding = json.load(open(os.path.join(PATH, "Pokedex", "itemEncoding.json")))
		self.ability_encoding = json.load(open(os.path.join(PATH, "Pokedex", "abilityEncoding.json")))
		self.move_encoding = json.load(open(os.path.join(PATH, "Pokedex", "moveEncoding.json")))
		self.type_encoding = json.load(open(os.path.join(PATH, "Pokedex", "typeEncoding.json")))
		self.pokedex = json.load(open(os.path.join(PATH, "Pokedex", "pokedex.json")))

	def __len__(self):
		# # of input files * # of pokemon used in each file (60) / batch size
		return self.input_count * 60 // self.batch_size # Floor division ensures we always have enough data for batch

	def __getitem__(self, index):
		# index is the index of the batch to be retrieved

		line_index = index % (60 // self.batch_size)
		file_index = index // (60 // self.batch_size)

		batch_file = open(os.path.join(self.dataset_filepath, self.input_files[file_index]), mode="r")
		data = batch_file.readlines()
		pokemon = []

		for line in data[line_index + 5 : line_index + 5 + self.batch_size]: # Shave off first 5 common lines and ensure only include the top 60 pokemon
			pokemon.append(line.split("|")[2].strip())

		x = []
		for mon in pokemon:
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

			xline = np.concatenate((moves, ability, item, types))
			x.append(xline)
		return np.array(x), np.array(x)

class PokemonGeneratorDimReduced(tf.keras.utils.Sequence):

	def __init__(self, data_type, encoder): # data_type is one of Training, Validation, or Testing
		self.dataset_filepath = os.path.join(PATH, "Data", data_type)
		self.batch_size = BATCH_SIZE
		self.input_files = os.listdir(self.dataset_filepath)
		self.input_count = len(self.input_files)
		self.indexes = np.arange(self.input_count)
		self.encoder = encoder # Auto encoder model created using pokemon_autoencoder()

		# Create a dictonary containing the total pokemon usages for the top 60 pokemon in a file
		self.usage_totals = {}
		file_num = 0
		for file in self.input_files:
			data = open(os.path.join(self.dataset_filepath, file)).readlines()
			cur_tot = 0
			for line in data[5:65]:
				cur_tot += float(line.split("|")[4].strip())
			self.usage_totals[file_num] = cur_tot
			file_num += 1
		
		# Load all data source files needed on init so we don't have to keep opening/closing them
		self.item_encoding = json.load(open(os.path.join(PATH, "Pokedex", "itemEncoding.json")))
		self.ability_encoding = json.load(open(os.path.join(PATH, "Pokedex", "abilityEncoding.json")))
		self.move_encoding = json.load(open(os.path.join(PATH, "Pokedex", "moveEncoding.json")))
		self.type_encoding = json.load(open(os.path.join(PATH, "Pokedex", "typeEncoding.json")))
		self.pokedex = json.load(open(os.path.join(PATH, "Pokedex", "pokedex.json")))

	def __len__(self):
		# # of input files * # of pokemon used in each file (60) / batch size
		return self.input_count * 60 // self.batch_size # Floor division ensures we always have enough data for batch

	def __getitem__(self, index):
		# index is the index of the batch to be retrieved

		line_index = index % (60 // self.batch_size)
		file_index = index // (60 // self.batch_size)

		batch_file = open(os.path.join(self.dataset_filepath, self.input_files[file_index]), mode="r")
		data = batch_file.readlines()
		pokemon = []
		y = []
		for line in data[line_index + 5 : line_index + 5 + self.batch_size]: # Shave off first 5 common lines and ensure only include the top 60 pokemon
			pokemon.append(line.split("|")[2].strip())
			y.append(float(line.split("|")[4].strip()) / self.usage_totals[file_index]) # Normalize usage to range 0-1 using total usage in file

		x = []
		for mon in pokemon:
			# Grab the pokemon's stats from the file (255 is the max size for any stat)
			stats = [self.pokedex[mon]['hp']/255, 
					 self.pokedex[mon]['atk']/255, 
					 self.pokedex[mon]['def']/255, 
					 self.pokedex[mon]['spa']/255, 
					 self.pokedex[mon]['spd']/255, 
					 self.pokedex[mon]['spe']/255]
			
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

			info = np.concatenate((moves, ability, item, types))
			dim_reduced_sparse = self.encoder.predict(tf.reshape(np.array(info), (1,569))) # Only encode sparse areas
			xline = np.concatenate((stats, tf.reshape(dim_reduced_sparse, (35))))
			x.append(xline)
		return np.array(x), np.array(y)