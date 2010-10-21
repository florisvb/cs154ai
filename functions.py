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
    
def generate_attribute_matrix(database, dtype='numpy', append_bird_ids=True, remove_empty_row=True):
    # create a mxn matrix where m is the bird species, and n is the attribute true/false array
    num_attributes = database.num_attributes
    num_species = database.num_species
    mat = np.zeros([num_species, num_attributes], dtype=int)
    for specie in range(num_species):
        try: # try/except needed to deal with empty bird[0] case
            mat[specie, :] = database.birds[specie].attributes_binary
        except:
            pass
            
    if append_bird_ids:
        bird_ids_arr = [i for i in range(num_species)]
        bird_ids = np.array(bird_ids_arr).reshape(num_species, 1)
        mat = np.hstack( (bird_ids, mat) )
    
    if remove_empty_row:
        # remove first row: it does not correspond to a real bird
        mat = np.delete(mat, np.s_[0], axis=0)
                
    if dtype == 'numpy':
        return mat
    elif dtype == 'list':
        return mat.tolist()
    
    
    
    
    
    
    
