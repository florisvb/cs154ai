import cPickle as pickle
import numpy as np
import random

# TODO:

# these are the variables that need tuning:
'''
definitely, probably, guessing
weight_diff, weight_uncertainty
probability and number of bird thresholds in finding the set of likely birds
'''

nspecies = 200
nattributes = 288

# probability scores... these values will require training or guess and check or something..
definitely = 0.9
probably = 0.6
guessing = 0.2

#########################################################################################

class AvianAsker:
    def __init__(self):
        self.database = initialize()
        self.unkbird = np.zeros(nattributes, dtype=float)
        self.unkbirdunc = np.zeros(nattributes, dtype=float)
        self.Qasked = []
    def myAvianAsker(self, img_id, QAs):
        if 1:
            ans = self.probability_halving_method(img_id, QAs)
            return ans
            
    def probability_halving_method(self, img_id, QAs):
        # if it's a new bird.. start with a fresh matrix
        if len(QAs) == 0:
            self.unkbird = np.zeros(nattributes, dtype=float)
            self.unkbirdunc = np.zeros(nattributes, dtype=float)
            reset(self.database)        
            self.Qasked = []
        # delete all birds that fail the question
        Q = None
        if len(QAs) > 0:
            Q = int(QAs[-1][0])
            A = QAs[-1][1]
            V = int(A[0])
            
            # guessed bird
            if Q >= nattributes:
                bird_guess = Q-nattributes+1
                if V == 1:
                    print 'yay!'
                if V == 0:
                    print 'wrong guess!!'
                    self.database.birds[bird_guess].permissible = False

            # guessed attribute            
            else:
                if V == 0:
                    v = -1.
                elif V == 1:
                    v = 1.
                elif V == 2:
                    v = 0.
                    
                if V != 2:
                    C = int(A[1])
                    if C == 0:
                        c = definitely
                    if C == 1:
                        c = probably
                    if C == 2:
                        c = guessing
                else:
                    c = 0
                
                self.unkbird[Q] = v
                self.unkbirdunc[Q] = c
                self.Qasked.append(Q)
                
        # calculate bird probabilities
        calc_bird_probabilities(self.database, self.unkbird, self.unkbirdunc)
        
        
            
        ##################  now ask questions  #######################
         # recalculate bird probabilities:
        #calc_bird_probabilities(self.database, likelybird, nonzero_only=False)
        
        
        
        
        '''
        #calc_bird_probabilities(self.database, likelybird, nonzero_only=False)
        most_probable_bird, p = get_most_probable_bird(self.database)
        
        calc_likely_birds(self.database, 0.8)
        n = count_likely_birds(self.database)
        if n < 4 and n > 0:
            # ask the question!
            # find the bird with the highest probability:
            print 'guessing bird: ', most_probable_bird, p
            return most_probable_bird + nattributes -1
        '''
        # calculate probabilities for unknown attributes:
        n = 0
        p = 1.0
        while n < 6:
            p -= 0.02
            calc_likely_birds(self.database, p)
            n = count_likely_birds(self.database)
            
        print 'n likely birds: ', n, p
        if n > 0 and n < 10:
            most_probable_bird, p = get_most_probable_bird(self.database)
            print 'guessing bird: ', most_probable_bird, p
            return most_probable_bird + nattributes -1
            
        likelybird = calc_likelybird(self.database)
        diff = np.abs(likelybird - np.zeros_like(likelybird))   
        
        # perhaps work in choosing the attributes that have higher certainty for the likely birds?
        avg_uncertainty = calc_avg_uncertainty_for_likely_birds(self.database)
        
        weight_diff = 1 # diff of 0 is desireable
        weight_uncertainty = 1 # uncertainty of 0 is desireable
        
        information = weight_diff*diff + weight_uncertainty*avg_uncertainty
        
        best_qs = np.argsort(information)
        print self.Qasked
        i = 0
        for i in range(len(best_qs)):
            if best_qs[i] in self.Qasked:
                continue
            else:
                print best_qs[i]
                return best_qs[i]
                
        # last resort: start guessing birds!
        most_probable_bird, p = get_most_probable_bird(self.database)
        print 'guessing bird: ', most_probable_bird, p
        return most_probable_bird + nattributes -1   
                


        
def initialize():
    try:
        database = load('picklefile')
        #print 'database loaded from picklefile!'
    except:
        print 'need to generate database'
        database = load_raw('student_dataset.txt')
        save(database, 'picklefile')
    return database

def load(filename):
    fname = (filename)
    fd = open( fname, mode='r')
    print 'loading data... '
    database = pickle.load(fd)
    return database
    
def load_raw(filename):
    database = Database()
    database.load_data(filename)
    database.calc_probabilistic_data()
    return database
    
def save(database, filename):
    print 'saving data to file: ', filename
    fname = (filename)  
    fd = open( fname, mode='w' )
    pickle.dump(database, fd)
    return 1
    
    #########################################################################################
    
    

def count_permissible_birds(database):
    n = 0
    for bird in database.birds:
        if bird is not None:
            if bird.permissible is True:
                n += 1
    return n
    
def count_likely_birds(database):
    n = 0.
    for bird in database.birds:
        if bird is not None:
            if bird.likely is True:
                n+=1
    return n
    
def get_most_probable_bird(database):
    best_prob = 0
    best_bird = None
    for i in range(len(database.birds)):
        bird = database.birds[i]
        if bird is None or bird.permissible is False:
            continue
        if bird.probability > best_prob:
            best_prob = bird.probability
            best_bird = i
    return best_bird, best_prob
    
def calc_likelybird(database):
    mat = None
    probsum = 0.
    for bird in database.birds:
        if bird is None:
            continue
        if bird.likely is True:
            
            new_bird_attr = bird.attributes_probabilistic*bird.probability
            probsum += bird.probability
        
            if mat is None:
                mat = np.array(new_bird_attr)
            else:
                mat = np.vstack((mat, new_bird_attr))
    if mat is not None:
        likelybird = np.sum(mat, axis=0) / probsum
    else:
        likelybird = np.zeros(nattributes, dtype=float)
    return likelybird
    
def calc_avg_uncertainty_for_likely_birds(database):
    
    sum_certainty = np.zeros(nattributes, dtype=float)
    n = 0
    for i, bird in enumerate(database.birds):
        if bird is not None:
            if bird.likely is True:
                n += 1
                sum_certainty += bird.attributes_certainty
    
    avg_certainty = sum_certainty / n
    
    # high avg_certainty == good, convert to uncertainty, where low is good:
    avg_uncertainty = np.abs(1-avg_certainty)
    
    return avg_uncertainty  
        
# this is the best model we have for the unknown bird
def calc_attribute_probabilities(database, unkbird):
    # get matrix of permissible bird attributes:
    mat = generate_attribute_matrix(database, dtype='numpy', append_bird_ids=False, remove_empty_row=True, permissible_only=True)
    probability_array = np.sum(mat, axis=0) / float(mat.shape[0])
    return probability_array
    
def calc_bird_probabilities(database, unkbird, unkbirdunc):

    for i,bird in enumerate(database.birds):
        if bird is None:
            continue
            
        binary_err = np.abs(bird.attributes_binary - unkbird)
        uncertainties = bird.attributes_certainty*unkbirdunc
        
        database.birds[i].err = sum( binary_err*uncertainties ) / 2.
        
        if unkbirdunc.sum() > 0:
            database.birds[i].probability = (unkbirdunc.sum() - database.birds[i].err) / unkbirdunc.sum()
        else:
            database.birds[i].probability = 0.5
    return database
    
def calc_likely_birds(database, p):
    for i in range(len(database.birds)):
        if i == 0:
            continue
        if database.birds[i].probability >= p and database.birds[i].permissible is True:
            database.birds[i].likely = True
        else:
            database.birds[i].likely = False 
    
def reliable_attributes(database):
    reliability = np.zeros(nattributes, dtype=float)
    for bird in database.birds:
        if bird is not None:
            reliability += np.abs(bird.attributes_probabilistic)
    reliability /= float(nspecies)    
    return reliability
    
        
def print_errors(database):
    for bird in database.birds:
        if bird is not None:
            print bird.err
            
def print_probabilities(database):
    for bird in database.birds:
        if bird is not None:
            print bird.probability
            
def print_birds(database):
    for i,bird in enumerate(database.birds):
        if bird is not None:
            print i
            
def get_bird(database):
    for i,bird in enumerate(database.birds):
        if bird is not None:
            return bird

def reset(database):
    database.unkbird = np.zeros(nattributes, dtype=float)
    for bird in database.birds:
        if bird is not None:
            bird.permissible = True

#########################################################################################

class Bird:
    def __init__(self, species):
        self.species = species
        self.permissible = True
        self.probability = 0.5
        
        # numpy array: there are 288 attributes
        nattributes = 288
        self.image_ids = []
        self.attributes = [None for i in range(nattributes)]
        self.attributes_probabilistic = np.array([0 for i in range(nattributes)], dtype=float)
        
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
    def __init__(self):
        print 'initializing'
        
        # dictionary of bird species:
        self.birds = [None for i in range(nspecies+1)]
        
        # look up image_id to get species name:
        self.load_image_ids('student_image.txt') 
        
    def calc_probabilistic_data(self):
    
        for bird in self.birds:
            if bird is not None:
                # calculate probabilistic value for each attribute, currently assumes all users are equally 'good'
                for i in range(len(bird.attributes)):
                    attribute = bird.attributes[i]
                    if attribute is None:
                        continue
                    
                    if len(attribute.shape) == 1:
                        attribute = attribute.reshape(1,len(attribute))
                    values = np.array( attribute[:,0], dtype=float )
                    # first change the truth value so that -1 is 'do not have' and +1 is 'have'
                    values[values==0] = -1.
                    values[values==2] = 0.
                    values[values==1] = 1.
                    certainties = np.array( attribute[:,1], dtype=float )
                    certainties[certainties==0] = definitely
                    certainties[certainties==1] = probably
                    certainties[certainties==2] = guessing
                    bird.attributes_probabilistic[i] = (values*certainties).sum() / float(len(values))
                bird.attributes_binary = np.sign(bird.attributes_probabilistic)
                bird.attributes_certainty = np.abs(bird.attributes_probabilistic)
                
                
    def load_data(self, filename):
        print 'loading data... this may take some time'
        raw_data = []
        infile = open(filename,"r")
        line_number = 0
        
        for line in infile.readlines():
            line_number += 1
            percent_read = float(line_number) / 8878904.
            #print 'reading line: ', line_number, ' = ', percent_read*100, '%'
            
            entry = map(int, line.split())
            raw_data.append(entry)
            # rawdata: 
            # <image_id> <attribute_id> <is_present> <certainty_id> <worker_id>
            
            bird_id = self.img_ids[str(entry[0])][0]
            species = self.bird_ids[str(bird_id)]
            # save all the data into an array of attributes:
            attribute = entry[1]
            new_attribute_data = np.array([ entry[2], entry[3], entry[4] ])
            
            if self.birds[bird_id] is None:
                self.birds[bird_id] = Bird(species)
                
            if self.birds[bird_id].attributes[attribute] is None:
                attribute_array = new_attribute_data
                print 'loading bird: ', bird_id
            else:
                attribute_data = self.birds[bird_id].attributes[attribute]
                attribute_array = np.vstack( (attribute_data, new_attribute_data) )
            self.birds[bird_id].attributes[attribute] = attribute_array
            
            # append image ids:
            if entry[0] not in self.birds[bird_id].image_ids:
                self.birds[bird_id].image_ids.append(entry[0])
            
    def load_image_ids(self, filename):
        self.img_ids = {}
        self.bird_ids = {}
        infile = open(filename,"r")
        for line in infile.readlines():
            partitioned = line.partition(' ')
            img_number = partitioned[0]
            text = partitioned[2]
            bird_id = int(text[0:3])
            img_path = text
            self.img_ids.setdefault(img_number, [bird_id, img_path])
            name = img_path.split('/')
            self.bird_ids.setdefault(str(bird_id), name[0])
            
    def load_attribute_ids(self, filename):
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
            
    def calc_image_histograms(self):
        for bird in self.birds:
            if bird is not None:
                img_ids = bird.image_ids
                for img_id in img_ids:
                    img_file = self.img_ids[img_id][1]
                    
                    # img_file is the path/image name of the image file
                    # do image processing here
                    print img_file
                    
                    bird.histogram = 'your histogram'
            
    
            
            
            
            
            
            
            
            
            
            
            
