import generator
import tensorflow as tf
import numpy as np

train_gen = generator.PokemonGenerator("Training")

def pokemon_usage_model():
	# training_data_folder is the full path to a folder containing the training data
	# validation_data_folder is the full path to a folder containing the validation data

	training_generator = generator.PokemonGenerator("Training")
	validation_generator = generator.PokemonGenerator("Validation")

	model = tf.keras.Sequential([
		tf.keras.layers.Dense(units = 575, input_shape=(575,), activation = 'relu'),
		tf.keras.layers.Dense(units = 1150, activation = 'relu'),
		tf.keras.layers.Dense(units = 300, activation = 'relu'),
		tf.keras.layers.Dense(units = 100, activation = 'relu'),
		tf.keras.layers.Dense(units = 30, activation = 'relu'),
		tf.keras.layers.Dense(1, activation='relu')
	])

	model.compile(optimizer='adam',
					loss='mean_squared_error',
					metrics=['accuracy'])

	model.fit(training_generator, validation_data = validation_generator, epochs = 10, verbose=1)

	training_performance = model.evaluate(training_generator)
	validation_performance = model.evaluate(validation_generator)

	# model is a trained keras rnn model to predict which activity a sequence corresponds to
	# training_performance is the performance of the model on the training set
	# validation_performance is the performance of the model on the validation set
	return model, training_performance, validation_performance

def pokemon_usage_model_dim_reduced(encoder):
	# training_data_folder is the full path to a folder containing the training data
	# validation_data_folder is the full path to a folder containing the validation data

	training_generator = generator.PokemonGeneratorDimReduced("Training", encoder)
	validation_generator = generator.PokemonGeneratorDimReduced("Validation", encoder)

	model = tf.keras.Sequential([
		tf.keras.layers.Dense(units = 32, input_shape=(41,), activation = 'relu'),
		tf.keras.layers.Dense(units = 16, activation = 'relu'),
		tf.keras.layers.Dense(units = 2, activation = 'relu'),
		tf.keras.layers.Dense(1, activation='relu')
	])

	model.compile(optimizer='adam',
					loss='mean_squared_error',
					metrics=['accuracy'])

	model.fit(training_generator, validation_data = validation_generator, epochs = 10, verbose=1)

	training_performance = model.evaluate(training_generator)
	validation_performance = model.evaluate(validation_generator)

	# model is a trained keras rnn model to predict which activity a sequence corresponds to
	# training_performance is the performance of the model on the training set
	# validation_performance is the performance of the model on the validation set
	return model, training_performance, validation_performance

def pokemon_autoencoder():
	# training_data_folder is the full path to a folder containing the training data
	# validation_data_folder is the full path to a folder containing the validation data

	training_generator = generator.PokemonGeneratorEncoder("Training")
	validation_generator = generator.PokemonGeneratorEncoder("Validation")

	encoder_input = tf.keras.layers.Input(shape=(569))
	encoded = tf.keras.layers.Dense(300, activation='relu')(encoder_input)
	encoded = tf.keras.layers.Dense(150, activation='relu')(encoded)
	encoded = tf.keras.layers.Dense(6, activation='relu')(encoded)
	encoder = tf.keras.Model(encoder_input, encoded)

	decoder_input = tf.keras.layers.Input(shape=(6))
	decoded = tf.keras.layers.Dense(150, activation='relu')(decoder_input)
	decoded = tf.keras.layers.Dense(300, activation='relu')(decoded)
	decoded = tf.keras.layers.Dense(569, activation='relu')(decoded)
	decoder = tf.keras.Model(decoder_input, decoded)

	auto_input = tf.keras.layers.Input(shape=(569))
	encode = encoder(auto_input)
	decode = decoder(encode)
	autoencoder = tf.keras.Model(auto_input, decode)

	optimizer = tf.keras.optimizers.Adam(learning_rate=0.01)
	autoencoder.compile(loss="mean_squared_error", optimizer=optimizer, metrics=["accuracy"])

	autoencoder.fit(training_generator, validation_data = validation_generator, epochs = 15, verbose=1)

	training_performance = autoencoder.evaluate(training_generator)
	validation_performance = autoencoder.evaluate(validation_generator)

	# autoencoder is a trained autoencoder
	# training_performance is the performance of the autoencoder on the training set
	# validation_performance is the performance of the autoencoder on the validation set
	return autoencoder, training_performance, validation_performance, encoder

autoencoder, Atrain, Aval, encoder = pokemon_autoencoder()
print(Atrain)
print(Aval)

# CHUNK OF CODE TO TEST WHAT PREDICTIONS LOOK LIKE ON FINAL NET
# autoencoder, Atrain, Aval, encoder = pokemon_autoencoder()
# model, train, val = pokemon_usage_model_dim_reduced(encoder)
# x=[0.21568627450980393, 0.21568627450980393, 0.21568627450980393, 0.5294117647058824, 0.5294117647058824, 0.5294117647058824, 0.0, 0.0, 0.0, 0.0, 1.9520211219787598, 0.0, 0.0, 2.521846294403076, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.8146684169769287, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.66090726852417]
# y=0.023095524935671897
# print(y)
# print(model.predict(tf.reshape(np.array(x), (1,41))))