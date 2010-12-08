import cPickle as pickle
import numpy as np
import copy
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
definitely = 1.0
probably = 0.8
guessing = 0.1


class AvianAsker:
    def __init__(self):
        self.database = initialize()
        self.reset()
        
    def reset(self):
        self.unkbird = [None for i in range(nattributes)]
        self.unkbird_certainty = [0 for i in range(nattributes)]
        self.denied_bird_list = []
        self.Qasked = []
        self.questions_remaining = [i for i in range(nattributes)]
        self.ask = True
        
    def myAvianAsker(self, img_id, QAs):
        if 1:
            ans = self.image_error_halving_method(img_id, QAs)
            return ans
            
    def image_error_halving_method(self, img_id, QAs):
        # if it's a new bird.. start with a fresh matrix
        if len(QAs) == 0:
            self.reset()
                        
        Q = None
        if len(QAs) > 0:
            Q = int(QAs[-1][0])
            A = QAs[-1][1]
            V = int(A[0])
            
            # guessed bird
            if Q >= nattributes:
                bird_guess = Q-nattributes+1
                #if V == 1:
                    #print 'yay!'
                if V == 0:
                    #print 'wrong guess!!'
                    self.denied_bird_list.append(bird_guess)

            # guessed attribute            
            else:
                try:
                    print 'questions asked: ', Q, V, int(A[1])
                except:
                    print 'questions asked: ', Q, V
                if V == 0:
                    v = 0
                elif V == 1:
                    v = 1.
                elif V == 2:
                    v = None
                    
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
                self.unkbird_certainty[Q] = c
                self.Qasked.append(Q)
                self.questions_remaining.remove(Q)
                
        ##############  MEAT of ALGORITHM  ###################
        
        calc_errors(self.database, self.unkbird, self.unkbird_certainty, self.denied_bird_list)
        likely_birds = calc_likely_birds(self.database)
        order = calc_bird_order(self.database)
        print 'order: '
        modes_sorted, modes = calc_mode_bird_order(self.database, threshold=0.2)
        print self.database.birds[order[0]].bird_id, self.database.birds[order[1]].bird_id, self.database.birds[order[2]].bird_id, self.database.birds[order[3]].bird_id, self.database.birds[order[4]].bird_id, self.database.birds[order[5]].bird_id, self.database.birds[order[6]].bird_id, self.database.birds[order[70]].bird_id, self.database.birds[order[8]].bird_id, self.database.birds[order[9]].bird_id, self.database.birds[order[10]].bird_id
        print 'mode order: '        
        print modes_sorted
        print 'modes: '
        print modes
        best_bird = modes[0]
                
        
        best_qs = self.questions_remaining
        
        # just to know what bird we're dealing with
        if self.ask is True:
            self.ask = False
            return self.database.birds[best_bird].bird_id + nattributes -1
            
        
        #print self.Qasked
        else:
            try:
                n = np.random.randint(0,len(self.questions_remaining))
                q = self.questions_remaining[n]
                print 'asking question: ', q, len(self.Qasked)
                return q
            except:
                # last resort: start guessing birds!
                print 'guessing bird: ', best_bird
                return best_bird + nattributes -1
        
        

#########################################################################################

def initialize():
    try:
        database = load('picklefile')
        load_image_ids(database, 'student_image.txt')
        #print 'database loaded from picklefile!'
    except:
        print 'need to generate database'
        database = load_images('student_dataset.txt')
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
    database.load_info()
    prep_data(database)
    return database
    
def load_workers(filename):
    database = Database()
    database.load_worker_data(filename)
    database.load_info()
    
    print 'prepping data...'
    prep_worker_data(database)
    prep_avg_image_data(database)
    fill_empty_worker_data(database)
    save_unique_worker_data(database)
    delete_unnecessary_data(database)
    calc_bird_dictionary(database)
    
    return database
    
def load_birds(filename):
    database = Database()
    load_image_ids(database, 'student_image.txt')
    database.load_birds(filename)
    prep_attributes(database)
    return database
    
def load_images(filename):
    database = Database()
    load_image_ids(database, 'student_image.txt')
    database.load_images(filename)
    #prep_attributes(database)
    return database
    
def save(database, filename):
    print 'saving data to file: ', filename
    fname = (filename)  
    fd = open( fname, mode='w' )
    pickle.dump(database, fd)
    return 1
    
                
def prep_attributes(database):
    
    for b, bird in enumerate(database.birds):
        if bird is not None:
            
            for a, attribute in enumerate(bird.attributes):
                
                #nanswers = float(len(attribute.true_certainties) + len(attribute.false_certainties))
            
                if len(attribute.true_certainties) > 0:
                    attribute.true = np.mean(attribute.true_certainties) / np.exp(1/float(len(attribute.true_certainties)))
                else:
                    attribute.true = 0
                
                if len(attribute.false_certainties) > 0:
                    attribute.false = np.mean(attribute.false_certainties) / np.exp(1/float(len(attribute.false_certainties)))
                else:
                    attribute.false = 0

def thresh(n, t):
    if n > t:
        return 1
    else:
        return 0
    
        
#########################################################################################

def calc_errors(database, unkbird, unkbird_certainty, denied_list=None):
    # unkbird is a vector array
    threshold = 0.3
    
    
    for bird in database.birds:
        if bird is not None:
            
            errors = 0
            n = 0.
            for i, val in enumerate(unkbird):
                if val is None: 
                    continue
                if val == 0:
                    err = 1-((1-np.abs(thresh(bird.attributes[i].false,threshold) - 1))*unkbird_certainty[i]*bird.attributes[i].false)
                if val == 1:
                    err = 1-((1-np.abs(thresh(bird.attributes[i].true,threshold) - 1))*unkbird_certainty[i]*bird.attributes[i].true)
                errors += err
                n += 1.
            try:
                bird.error = errors / n
            except:
                bird.error = 0.
            if denied_list is not None:
                if bird.bird_id in denied_list:
                    bird.error = 1000.
        
def calc_bird_order(database, bird_ids=None):

    if bird_ids is None:
        birds = database.birds[1:]
    else:
        if type(bird_ids) is not list:
            bird_ids = [bird_ids]
        birds = [database.birds[i] for i in bird_ids]

    bird_errors = [bird.error for bird in birds]
    order = np.argsort(bird_errors)
    return order
    
def print_errors(database):
    for bird in database.birds:
        if bird is not None:
            print bird.bird_id, bird.error
    
def calc_likely_birds(database, threshold=0.46):
    likely_birds = []
    for bird in database.birds:
        if bird is not None:
            if bird.error <= threshold:
                likely_birds.append(bird.bird_id)
    return likely_birds
                
def print_attributes(database, bird_ids, attributes=None):

    if type(bird_ids) is not list:
        bird_ids = [bird_ids]
    birds = [database.birds[bird_id] for bird_id in bird_ids]  
    
    if attributes is None:
        attributes = [i for i in range(nattributes)]
    
    for bird in birds:    
        if bird is not None:
            for a in attributes:    
                print a, bird.attributes[a].true, bird.attributes[a].false

    
def calc_information_values(database, likely_images):

    avg_likely_image = None
    avg_likely_image_certainties = None
    
    for k in likely_images:
        image = database.images[k]
        
        if avg_likely_image is None:
            avg_likely_image = image.attributes
            avg_likely_image_certainties = image.certainties
        else:
            avg_likely_image += image.attributes
            avg_likely_image_certainties += image.certainties
            
            
    avg_likely_image /= float(len(likely_images))
    avg_likely_image_abs = np.abs(avg_likely_image)
    avg_likely_image_abs_pos = 1.-avg_likely_image_abs
    avg_likely_image_certainties /= float(len(likely_images))
    
    # best information content will be a combination of the attribute with a value of zero (greatest disagreement among images), and a high certainty
    
    information_values = 1. - avg_likely_image_abs_pos#*avg_likely_image_certainties # information value of 0 is good, 1 is bad (for np.argsort simplicity)
    
    return information_values
    

def mode(database, a, full_output=True):
    a = np.array(a)
    uarr = np.unique(a)
    
    if full_output is False:
        bestu = 0
        modeu = 0
        for i, u in enumerate(uarr):
            u = int(u)
            l = len(a[a==u])
            if l > modeu:
                bestu = u
                modeu = l
        return bestu, modeu
        
    else:
        modes = [0 for i in range(nspecies+1)]
        for i, u in enumerate(uarr):
            u = int(u)
            l = float(len(a[a==u]))
            print l
            modes[u] = l / float(len(database.bird_images_dict[u]))
        modes_sorted = np.argsort(modes)   
        return modes_sorted[::-1], modes
            
def calc_mode_bird_order(database, threshold=0.5):

    likely_images = calc_likely_birds(database, threshold)
    
    birds = [database.birds[i].bird_id for i in likely_images]
    
    modes_sorted, modes = mode(database, birds)
    
    return modes_sorted, modes


def load_image_ids(database, filename):
    infile = open(filename,"r")
    database.image_dict = {}
    database.bird_images_dict = {}
    for line in infile.readlines():
        partitioned = line.partition(' ')
        img_number = int(partitioned[0])
        text = partitioned[2]
        bird_id = int(text[0:3])
        img_path = text
        species = img_path.split('/')
        if img_number not in database.image_dict.keys():
            database.image_dict.setdefault(img_number, [bird_id, img_path, species])
        
        if bird_id not in database.bird_images_dict.keys():
            database.bird_images_dict.setdefault(bird_id, [])
        if img_number not in database.bird_images_dict[bird_id]:
            database.bird_images_dict[bird_id].append(img_number)
            
        if 0:
            try:
                if img_number not in database.birds[bird_id].images:
                    database.birds[bird_id].images.append(img_number)
            except:
                database.birds[bird_id].images = [img_number]
            database.birds[bird_id].species = species[0][4:]

    
    
#########################################################################################

class Image:
    def __init__(self, image_id, worker_id=None):
        self.image_id = image_id
        self.worker_id = worker_id
        self.attributes = np.zeros(nattributes, dtype=float)
        self.nobs = np.zeros(nattributes, dtype=float)
        self.certainties = np.zeros(nattributes, dtype=float)
        self.error = 0.0
        self.histogram = None

class ImageGroup:
    def __init__(self, image_id):
        self.image_id = image_id
        self.workers = {} # dictionary of individual instances of this image -- corresponding to unique workers
        self.avg = Image(self.image_id)
        
class Attribute:
    def __init__(self, attribute_id):
        self.attribute_id = attribute_id
        self.true_certainties = []
        self.false_certainties = []
        self.false = 0
        self.true = 0
        
class Bird:
    def __init__(self, bird_id):
        self.bird_id = bird_id
        self.attributes = [Attribute(i) for i in range(nattributes)]
        self.images = []
        
        # each element in self.attributes is a list of possible answers and their certainties
        
    
    
# to generate the table, just vstack all the arrays for all the images in all the workers, append the bird_id (get from image_id)

#########################################################################################

        
class Database:
    def __init__(self):
        print 'initializing'
        self.images = {}
        self.image_groups = {}
        self.birds = [None for i in range(nspecies+1)]
        self.images = {}
        
    def load_info(self):
        self.load_image_ids('student_image.txt') 
        self.load_attribute_ids('attributes.txt')
        
    def load_birds(self, filename):
        print 'loading data... this may take some time'
        infile = open(filename,"r")
        line_number = 0
        
        for line in infile.readlines():
            line_number += 1
            percent_read = float(line_number) / 7111751.
            
            entry = map(int, line.split())
            # rawdata: 
            # <image_id> <attribute_id> <is_present> <certainty_id> <worker_id>
            
            image_id = entry[0]
            attribute_id = entry[1]
            is_present = entry[2]*2 -1
            certainty_id = entry[3]
            worker_id = entry[4]
            
            bird_id = self.image_dict[image_id][0]
            
            # convert certainties to something meaningful:
            if certainty_id == 0: # definitely
                certainty = 1.0
            elif certainty_id == 1: # probably
                certainty = 0.8
            elif certainty_id == 2: # guessing
                certainty = 0.1
            
            
            def save_entry(bird):
                if is_present > 0:
                    bird.attributes[attribute_id].true_certainties.append(certainty)
                if is_present < 0:
                    bird.attributes[attribute_id].false_certainties.append(certainty)
                    
            if self.birds[bird_id] is None:
                print 'reading line: ', line_number, ' = ', percent_read*100, '%'                
                self.birds[bird_id] = Bird(bird_id)
            save_entry(self.birds[bird_id])
                
                
    def load_images(self, filename):
        print 'loading data... this may take some time'
        infile = open(filename,"r")
        line_number = 0
        
        for line in infile.readlines():
            line_number += 1
            percent_read = float(line_number) / 7111751.
            
            entry = map(int, line.split())
            # rawdata: 
            # <image_id> <attribute_id> <is_present> <certainty_id> <worker_id>
            
            image_id = entry[0]
            attribute_id = entry[1]
            is_present = entry[2]*2 -1
            certainty_id = entry[3]
            worker_id = entry[4]
            
            bird_id = self.image_dict[image_id][0]
            
            # convert certainties to something meaningful:
            if certainty_id == 0: # definitely
                certainty = 1.0
            elif certainty_id == 1: # probably
                certainty = 0.8
            elif certainty_id == 2: # guessing
                certainty = 0.1
            
            
            def save_entry(image):
                if is_present > 0:
                    image.attributes[attribute_id].true_certainties.append(certainty)
                if is_present < 0:
                    image.attributes[attribute_id].false_certainties.append(certainty)
                    
            if image_id not in self.images.keys():
                print 'reading line: ', line_number, ' = ', percent_read*100, '%'                
                self.images.setdefault(image_id, Bird(bird_id))
            save_entry(self.images[image_id])                
                
        self.birds = []
        for i, image in self.images.items():
            self.birds.append(image)
            
    
            
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
            
            
            
            
            
            
            
            
            
            
