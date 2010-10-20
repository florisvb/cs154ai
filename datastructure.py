import cPickle as pickle
import numpy as np


def load(filename):
    fname = (filename)
    fd = open( fname, mode='r')
    print 'loading data... '
    database = pickle.load(fd)
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
    return 1

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
            
    
            
            
            
            
            
            
            
            
            
            
            
