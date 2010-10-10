in an interactive python environment, like ipython, use the datastructure like so:

import datastructure

# for raw data: (this takes a while)
data.load_data(FILENAME)
data = datastructure.Database()

# for a pickled file: (ie. someone has already run the database and provided a pickle file):
data = datastructure.load(FILENAME.PICKLE)

# acccessing the data:
for k, v in data.birds.items():
    # k is the species name
    # to access the attributes:
    data.birds[k].attributes
    # the attributes are in a matrix form, where 0: false, 1: true
    # the attribute index number corresponds to the attribute in the attributes.txt file
