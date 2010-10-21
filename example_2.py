import datastructure
import functions

############################################################################################################
'''
to run different sections of the script, either make a new script and copy/paste, 
or just change the if statements to the appropriate value 
'''
############################################################################################################

# you may need to change this if your path is set up differently
FILENAME = 'milestone1/dataset.txt'
FILENAME_PICKLE = 'database' 

# this is to load the raw data... this takes a somewhat long time
if 0:
    database = datastructure.load_raw(FILENAME)
    
# this is to load a pickled database... this is much faster
if 1:
    database = datastructure.load(FILENAME_PICKLE)
    

# generate a matrix where the rows are bird species and the columns are attributes:
# first column is the species number (you can omit this with flag: append_bird_ids=False)

# this is for a NUMPY array (see http://www.scipy.org/NumPy_for_Matlab_Users):
if 1:
    mat = functions.generate_attribute_matrix(database, dtype='numpy')

# this is for a regular python list:
if 0:
    mat = functions.generate_attribute_matrix(database, dtype='list')
    
# I recommend using the numpy array.. it will open more possibilities, like doing actual math
    
