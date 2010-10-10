import pickle
import numpy as np


def load(filename):
    fname = (filename)
    fd = open( fname, mode='r')
    print 'loading data... '
    dataset = pickle.load(fd)
    return dataset
    
def save(dataset, filename):
    print 'saving data to file: ', filename
    fname = (filename)  
    fd = open( fname, mode='w' )
    pickle.dump(dataset, fd)
    return 1

#########################################################################################

class Bird:
    def __init__(self, species):
        self.species = species
        self.attribute_ids = []
        self.attribute_bool = []
        self.attribute_certainty = []
        self.worker_id = []
        
        # numpy array: there are 288 attributes
        self.attributes = np.zeros([288, 1])

#########################################################################################        
        
class Database:
    def __init__(self):
        print 'initializing'
        
        # database of bird species:
        self.birds = {}
        
        # look up image_id to get species name:
        self.load_image_ids('attributes/images.txt') 
        
    def load_data(self, filename):
        print 'loading data... this may take some time'
        self.raw_data = []
        infile = open(filename,"r")
        line_number = 0
        
        for line in infile.readlines():
            line_number += 1
            percent_read = float(line_number) / 8878904.
            print 'reading line: ', line_number, ' = ', percent_read, '%'
            
            entry = map(int, line.split())
            self.raw_data.append(entry)
            # rawdata: 
            # <image_id> <attribute_id> <is_present> <certainty_id> <worker_id>
            
            species = self.img_ids[str(entry[0])]
            
            if species not in self.birds:
                self.birds.setdefault(species, Bird(species))
                
            self.birds[species].attribute_ids.append(entry[1])
            self.birds[species].attribute_bool.append(entry[2])
            self.birds[species].attribute_certainty.append(entry[3])
            self.birds[species].worker_id.append(entry[4])
            
            # for the first round... use this.. assumes no noise in answers, and thus no need to track MTurk user numbers or certainty:
            if entry[3] is 1:
                attribute = entry[1]
                self.birds[species].attributes[attribute] = entry[2]
            
            
    def load_image_ids(self, filename):
        self.raw_img_ids = []
        self.img_ids = {}
        infile = open(filename,"r")
        for line in infile.readlines():
            partitioned = line.partition(' ')
            img_number = partitioned[0]
            img_filename = partitioned[2]
            img_filename = img_filename.strip()
            
            # strip the individual filename descriptors to get just the species name
            img_filename = img_filename.rstrip('.jpg')
            img_filename = img_filename.rstrip('xxx')
            img_filename = img_filename.rstrip('0123456789')
            img_filename = img_filename.rstrip('_')
            img_filename = img_filename.rstrip('0123456789')
            img_filename = img_filename.rstrip('_')
            
            self.img_ids.setdefault(partitioned[0], img_filename)
            
    def load_attribute_ids(self, filename):
        self.raw_attribute_ids = []
        self.attribute_ids = {}
        infile = open(filename,"r")
        for line in infile.readlines():
            line = line.rstrip()
            partitioned_1 = line.partition(' ')
            attribute_number = partitioned_1[0]
            partitioned_2 = partitioned_1[2].partition('::')
            attribute_name = partitioned_2[0]
            attribute_value = partitioned_2[2]
            attribute = (attribute_name, attribute_value)
            self.attribute_ids.setdefault(attribute_number, attribute)
            
            
            
            
            
            
            
            
            
            
            
            
            
