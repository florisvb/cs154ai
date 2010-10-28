import random
import AvianAsker

myAvianAsker = AvianAsker.myAvianAsker

nspecies = 200
nattributes = 288


#Example of a bad asker
#Replace this part by your own function
def myAvianAskerRandom(QAs):
    #First five questions are on attributes 
    if len(QAs) < 5:
        Q=random.randint(0,nattributes-1)
    #All others guess the species
    else:
        Q=random.randint(nattributes,nattributes+nspecies)
    return Q
    
def check_all_birds():
    birdnum = 1
    results = []
    numQs = []
    while birdnum < nspecies:
        
        QAs = playgame(birdnum)
        results.append(QAs)
        numQs.append(len(QAs))
        birdnum += 1
        
    mean_numQs = np.mean(numQs)
    std_numQs = np.std(numQs)
    
    return mean_numQs, std_numQs, results
    
    
def playgame(bird=None):

    infile = open("specie_names.txt","r")
    train = infile.readlines()
    spec_dict={}
    for lines in train:
            entry=lines.split()
            spec_dict[entry[0]]= [entry[1],entry[2],entry[3]]
    if bird == None:
        #Open random bird
        rndbrd = random.randint(1,len(train))
    else:
        rndbrd = bird

    #Open train data
    infile = open("dataset.txt","r")
    id_dict={}
    attr_dict={}
    prev_entry = ""
    for lines in infile.readlines():
            entry = lines.split()
            if entry[0] != prev_entry:
                    attr_dict = {}
            attr_dict[entry[1]]=entry[2]
            id_dict[entry[0]]=attr_dict
            prev_entry = entry[0]

    #Open attribute data
    infile = open("attributes.txt","r")
    Ques_dict = {}
    for lines in infile.readlines():
            entry = lines.split()
            attr = entry[1].split("::")
            name = attr[0].split('_')
            Ques_dict[entry[0]] = " ".join(name) + " of " + attr[1]

    #Begin new game
    QAs = []
    Q = None
    while Q is not -1:
        Q = myAvianAsker(QAs)
        if Q-nattributes+1 == rndbrd:
            print("Is it "+" ".join(spec_dict[str(Q-nattributes+1)][1].split('_'))+"?")
            print("You have guessed correctly, the bird is "+" ".join(spec_dict[str(rndbrd)][1].split('_'))+"\n")
            break
        elif Q >= nattributes + nspecies:
            print("The question is out of range")
            continue
        elif Q >= nattributes and Q != rndbrd:
            print("Is it "+" ".join(spec_dict[str(Q-nattributes+1)][1].split('_'))+"?")
            print("Sorry, you are wrong!\n")
            A = '0' #incorrect guess
            break
        else:                
            print("It "+ Ques_dict[str(Q)] +"?")
            A = id_dict[spec_dict[str(rndbrd)][0]][str(Q)];                       
            if A == '1':
                print("Yes!\n")
            else:
                print("No!\n")

        QAs.append([Q, A])
        
    return QAs
    
    
if __name__=='__main__':
    playgame()
