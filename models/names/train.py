from textgenrnn import textgenrnn
textgen = textgenrnn()

# new_model=True - it will generate in the same directory
# - textgenrnn_config.json
# - textgenrnn_vocab.json
# - textgenrnn_weights.hdf5
# word_level - True means learn off words, False means learn off letters (hard)
textgen.train_from_file('names.txt',
                        new_model=True,
                        word_level=True,
                        num_epochs=10000)
print(textgen.model.summary())
textgen.generate()
