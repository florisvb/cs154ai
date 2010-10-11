import datastructure
import functions


# this is to load the raw data... this takes a very long time
if 0:
    database = datastructure.load_raw(FILENAME)
    
# this is to load a pickled database... much faster 
if 1:
    database = datastructure.load(FILENAME)
    

# some examples of how to use the database:

# find all bird species that have pink eyes... that means look for all birds that have a value of True for attribute 287:
if 1:
    for k,v in database.birds.items():
        if database.birds[k].has_attribute(287):
            print k 
        # alternatively:
        if 0:
            if v.has_attribute(287):
                print k 
        
    
# eliminate all birds with pink eyes [287], and irridescent wings [275] from the database... it's best not to remove them entirely, so let's tag them with a variable
if 0:
    for k,v in database.birds.items():
        if database.birds[k].has_attribute(287):
            database.birds[k].permissible = False
        if database.birds[k].has_attribute(275):
            database.birds[k].permissible = False            
            
    # now next time we can just look for the 'permissible' birds:
    print 'number permissible birds left: ', functions.count_permissible_birds(database)
    
