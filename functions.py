import numpy as np
import datastructure
import cPickle as pickle

def load(filename):
    fname = (filename)
    fd = open( fname, mode='r')
    print 'loading data... '
    database = pickle.load(fd)
    return database
    
def load_raw(filename):
    database = datastructure.Database()
    database.load_data(filename)
    return database
    
def save(database, filename):
    print 'saving data to file: ', filename
    fname = (filename)  
    fd = open( fname, mode='w' )
    pickle.dump(database, fd)
    return 1
    
#############################################################################

def count_permissible_birds(database):
    n = 0
    for k,v in database.birds.items():
        if database.birds[k].permissible is True:
            n += 1
    return n
