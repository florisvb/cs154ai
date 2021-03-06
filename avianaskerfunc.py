import cPickle as pickle
import numpy as np

def self_containedfunction(questionlist):

    SAVE_DATA = True

    try:
        database = load('picklefile')
        print 'database loaded from picklefile!'
    except:
        print 'need to generate database'
        database = load_raw('dataset.txt')
        database.mat = generate_attribute_matrix(database, dtype='numpy', append_bird_ids=True, remove_empty_row=True)
        save(database, 'picklefile')
    ## you now have a raw database to work with
    
    mat = database.mat
    
    # insert code here	
    
    
    
    # optional: 
    if SAVE_DATA is True:
        database.mat = mat
        save(database, 'picklefile')
        
#########################################################################################

def load(filename):
    fname = (filename)
    fd = open( fname, mode='r')
    print 'loading data... '
    database = pickle.load(fd)
    fd.close()
    return database
    
def load_raw(filename):
    database = Database()
    database.load_data(filename)
    return database
    
def save(database, filename):
    print 'saving data to file: ', filename
    fname = (filename)  
    fd = open( fname, mode='w' )
    pickle.dump(database, fd)
    fd.close()
    return 1
    
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
        self.load_image_ids('milestone1/specie_names.txt') 
        
        # look up attribute id number and text pair
        self.load_attribute_ids('milestone1/attributes.txt')
        
    def load_data(self, filename='milestone1/dataset.txt'):
        print 'loading data... this may take some time'
        raw_data = []
        infile = open(filename,"r")
        line_number = 0
        
        for line in infile.readlines():
            line_number += 1
            percent_read = float(line_number) / 57600.
            print 'reading line: ', line_number, ' = ', percent_read*100, '%'
            
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
    

        
    
    
