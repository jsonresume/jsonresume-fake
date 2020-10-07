from textgenrnn import textgenrnn

# Load the names model
textgen = textgenrnn(weights_path='./models/names/textgenrnn_weights.hdf5',
                       vocab_path='./models/names/textgenrnn_vocab.json',
                       config_path='./models/names/textgenrnn_config.json')

# n - How many sample outputs should you generate
# temperature - A value between 0-1, where 1 is more creative and 0 tries to be boring
names = textgen.generate(n=3, temperature=0.7, return_as_list=True)
print(names)
