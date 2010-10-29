import numpy as np
import cPickle as pickle
import random

nspecies = 200
nattributes = 288

#########################################################################################
#  myAvianAsker
#########################################################################################

def answerQuestion(Q, truth_value, matrix):
    
    if Q >= nattributes:
        bird_guess = Q-nattributes+1
        index = np.where(matrix==bird_guess)[0][0]
        if int(truth_value) == 0:
            matrix = np.delete(matrix, np.s_[index], axis=0)
        return matrix
    else:
        attrnum = Q+1
        
    num_species = matrix.shape[0]
    for i in range(1,num_species+1):
        index = num_species - i
        if (int(matrix[index,attrnum]) != int(truth_value)):
            matrix = np.delete(matrix, np.s_[index], axis=0)
    return matrix


#Generate a question
def myAvianAsker(QAs, printvals=False, database=None):
    SAVE_DATA = True

    if database is None:
        cheat = False
        database = initialize()
    else:
        cheat = True
        # database is given
    
    # if it's a new bird.. start with a fresh matrix
    ## TODO:
    # This might be wrong? Need a 'is new bird' algorithm based on QAs
    if len(QAs) == 0:
        database.mat = generate_attribute_matrix(database, dtype='numpy', append_bird_ids=True, remove_empty_row=True)
    mat = database.mat
    
    # delete all birds that fail the question
    if len(QAs) > 0:
        Q = QAs[-1][0]
        A = QAs[-1][1]
        mat = answerQuestion(Q, A, mat)
                    
    #Save the trunkated matrix into a pickle: 
    database.mat = mat
    if SAVE_DATA is True and cheat is False:
        save(database, 'picklefile')

    # if we've found the bird, ask about its name
    if (mat.shape[0] <= 3):
        if printvals:
	        print mat[0,0]
	        
        possible_birds = [i for i in mat[:,0]]
        bird_guess = possible_birds[ random.randint(1,len(possible_birds))-1 ]
        
        if cheat is False:
            return bird_guess + nattributes -1 
        elif cheat is True:
            return bird_guess + nattributes -1 , database

    # otherwise generate a question about one of the attributes
    min_value = 10000
    min_index = -1
    for i in range(1,mat.shape[1]):
        num = abs(float(sum(mat[:,i]))/mat.shape[0] - 0.5)
        if (num < min_value):
            min_value = num
            min_index = i
            
    if cheat is False:
        return min_index-1
    elif cheat is True:
        return min_index-1, database
        
#########################################################################################
#  Help Functions
#########################################################################################

def load(filename):
    fname = (filename)
    fd = open( fname, mode='r')
    #print 'loading data... '
    database = pickle.load(fd)
    fd.close()
    return database
    
def load_raw(filename):
    database = Database()
    database.load_data(filename)
    return database
    
def save(database, filename):
    #print 'saving data to file: ', filename
    fname = (filename)  
    fd = open( fname, mode='w' )
    pickle.dump(database, fd)
    fd.close()
    return 1
    
def initialize():
    try:
        database = load('picklefile')
        #print 'database loaded from picklefile!'
    except:
        print 'need to generate database'
        database = load_raw('dataset.txt')
        database.mat = generate_attribute_matrix(database, dtype='numpy', append_bird_ids=True, remove_empty_row=True)
        save(database, 'picklefile')
    return database
#########################################################################################

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

#########################################################################################

class Bird:
    def __init__(self, species, num_attributes=284):
        self.species = species
        self.permissible = True
        
        # numpy array: there are 288 attributes
        
        #self.attributes = [0 for i in range(n_attributes)]
        self.attributes_binary = [0 for i in range(num_attributes)]
        
    def has_attribute(self, attribute, method='binary'):
        answer = None
        
        if method == 'binary':
            if self.attributes_binary[attribute] == 0:
                answer = False
            else:
                answer = True
                
        return answer
        
#########################################################################################        
        
class Database:
    def __init__(self, num_species=201, num_attributes=288):
        print 'initializing'
        
        self.num_species = num_species
        self.num_attributes = num_attributes
        
        # dictionary of bird species:
        self.birds = [None for i in range(num_species)]
        self.bird_names = {}
        
        # look up image_id to get species name:
        self.load_image_ids('specie_names.txt') 
        
        # look up attribute id number and text pair
        self.load_attribute_ids('attributes.txt')
        
    def load_data(self, filename='dataset.txt'):
        print 'loading data... this may take some time'
        raw_data = []
        infile = open(filename,"r")
        line_number = 0
        
        for line in infile.readlines():
            line_number += 1
            percent_read = float(line_number) / 57600.
            
            entry = map(int, line.split())
            #entry: img_number, attribute_number, true/false
            
            img_number = entry[0]
            attribute_number = entry[1]
            attribute_value = entry[2]
            
            species_number = self.img_ids[str(img_number)][0]
            species_name = self.img_ids[str(img_number)][1]
            self.bird_names.setdefault(species_name, species_number)
            if self.birds[species_number] is None:
                self.birds[species_number] = Bird(species_name, num_attributes=self.num_attributes)
                print 'reading line: ', line_number, ' = ', percent_read*100, '%', 'bird: ', species_name
                
            # save all the data into an array of attributes:
            self.birds[species_number].attributes_binary[attribute_number] = attribute_value
            
        infile.close()
            
            
    def load_image_ids(self, filename):
        self.img_ids = {}
        infile = open(filename,"r")
        for line in infile.readlines():
            partitioned = line.split()
            img_number = int(partitioned[1])
            specie_number = int(partitioned[0])
            specie_name = partitioned[2]
            img_filename = partitioned[3]
            
            img_info = [specie_number, specie_name, img_filename]
            self.img_ids.setdefault(str(img_number), img_info)
            
        infile.close()
            
            
    def load_attribute_ids(self, filename):
        self.attribute_ids = [None for i in range(self.num_attributes)]
        infile = open(filename,"r")
        for line in infile.readlines():
            line = line.rstrip()
            partitioned_1 = line.partition(' ')
            attribute_number = int(partitioned_1[0])
            partitioned_2 = partitioned_1[2].partition('::')
            attribute_name = partitioned_2[0]
            attribute_value = partitioned_2[2]
            attribute = (attribute_name, attribute_value)
            print attribute_number
            self.attribute_ids[attribute_number] = attribute
            
        infile.close()
    
#########################################################################################
    

