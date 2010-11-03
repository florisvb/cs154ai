import AvianAsker as AA
import numpy as np

# NOTE: good idea to remove 'picklefile' if this is the first time running this script (or using updated AvianAsker code)

database = AA.initialize()


# make an unknown bird
unkbird = np.ones(database.num_attributes)*0.5

# set some random parameters:
data = [[1,1]]

for datum in data:
    unkbird[datum[0]] = datum[1]
    
# fill out related attributes:
unkbird = AA.fillout_related_attributes(database, unkbird)

# remove impossible birds:
AA.remove_impossible_birds(database, unkbird)

# print number of remaining birds:
print 'remaining possible birds: ', AA.count_permissible_birds(database)

# calculate probabilities for unknown attributes:
p = AA.calc_attribute_probabilities(database, unkbird)
print 'best guess at unkbird attributes: '
print p

# update unkbird to reflect these new info:
unkbird = p

# calculate bird probabilities:
AA.calc_bird_probabilities(database, unkbird)

# print the bird probabilities for all the birds:
print 'probabilities'
AA.print_probabilities(database)



