import random

nspecies = 200
nattributes = 287


#Example of a bad asker
#Replace this part by your own function
def myAvianAsker(QAs):
	#First five questions are on attributes 
        if len(QAs) < 5:
                Q=random.randint(nspecies+1,nspecies+nattributes)
	#All others guess the species
	else:
                Q=random.randint(1,nspecies)
	return Q

#Open random bird
infile = open("specie_names.txt","r")
train = infile.readlines()
spec_dict={}
for lines in train:
        entry=lines.split()
        spec_dict[entry[0]]= [entry[1],entry[2],entry[3]]
rndbrd = random.randint(1,len(train))

#Open train data
infile = open("dataset.txt","r")
id_dict={}
attr_dict={}
for lines in infile.readlines():
        entry = lines.split();
        attr_dict[entry[1]]=entry[2]
        id_dict[entry[0]]=attr_dict

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
while True:
        Q = myAvianAsker(QAs)
	if Q == rndbrd:
                print("Is it "+" ".join(spec_dict[str(Q)][1].split('_'))+"?")
                print("You have guessed correctly, the bird is "+" ".join(spec_dict[str(rndbrd)][1].split('_'))+"\n")
                break
        elif Q <= nspecies and Q != rndbrd:
                print("Is it "+" ".join(spec_dict[str(Q)][1].split('_'))+"?")
                print("Sorry, you are wrong!\n")
                A = "4" #incorrect guess
        else:                
                print("It"+ Ques_dict[str(Q-nspecies)] +"?")
                A = id_dict[spec_dict[str(rndbrd)][0]][str(Q-nspecies)];                       
                if A == '0':
                        print("Yes!\n")
                else:
                        print("No!\n")
	QAs.append([Q, A])
