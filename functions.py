import numpy as np

count_permissible_birds(database):
    n = 0:
    for k,v in database.birds.items():
        if database.birds[k].permissible is True:
            n += 1
    return n
