import random
#from AvianAsker_A## import *
import cPickle
import AvianAsker

nspecies = 200
nattributes = 288

#TA's asker
#Replace this part by your own function in another file
AA = AvianAsker.AvianAsker()
myAvianAsker = AA.myAvianAsker

#Open attribute data
infile = open("attributes.txt","r")
Ques_dict = {}
for lines in infile.readlines():
        entry = lines.split()
        attr = entry[1].split("::")
        name = attr[0].split('_')
        Ques_dict[entry[0]] = " ".join(name) + " of " + attr[1]


image = {}
spec_dict={}
#Open image dirs
image_dir = open("student_image.txt","r")
for i in image_dir.readlines():
        entry = i.split()
        image[int(entry[0])] = entry[1]
        specy = entry[1].split(".")
        name = specy[1].split("/")
        if int(specy[0]) not in spec_dict.keys():
                spec_dict[int(specy[0])] = name[0]

#Open dataset
dataset = open("student_cPickle.txt","r")
data = cPickle.load(dataset)
dataset.close()

#Begin new game
Sum = 0
n = 1000
#AA = AvianAsker_A##()
for i in range(n):
        image_id = random.choice([k for k in image.keys()])
        rndbrd = int((image[image_id].split("."))[0])        
        #AA.init()
        #myAvianAsker = AA.myAvianAsker
        QAs = []
        while True:
                Q = myAvianAsker(image[image_id], QAs)
                if Q-nattributes+1 == rndbrd:
                        #print("Is it "+spec_dict[Q-nattributes+1]+"?")
                        #print("You have guessed correctly, the bird is "+spec_dict[rndbrd]+"\n")
                        print("Your score is "+str(len(QAs)+1))
                        Sum = Sum + len(QAs) + 1
                        break
                elif Q >= nattributes + nspecies:
                        #print("The question is out of range")
                        continue
                elif Q >= nattributes and Q != rndbrd:
                        #print("Is it "+spec_dict[Q-nattributes+1]+"?")
                        #print("Sorry, you are wrong!\n")
                        A = '0' #incorrect guess
                else:                
                        #print("It "+ Ques_dict[str(Q)] +"?")
                        if Q in data[image_id].keys():
                                A = data[image_id][Q]
                        else:
                                A = '2'
                        if 0:
                            if A == [1,0]:
                                    print("Yes! Probably.\n")
                            elif A == [1,1]:
                                    print("Yes! Definitely.\n")
                            elif A == [1,2]:
                                    print("Yes! I guess.\n")
                            elif A == [0,0]:
                                    print("No! Probably.\n")
                            elif A == [0,1]:
                                    print("No! Definitely.\n")
                            elif A == [0,2]:
                                    print("No! I guess.\n")
                            else:
                                    print("I don't know!\n")

                QAs.append([Q, A])
                f = open("QA.txt", "w")
                f.write(str(QAs))
                f.close()
        print("Num is " + str(i+1) + ", Sum is "+str(Sum)+", Score now is "+str(Sum/(i+1)))
print("Your final score is "+str(Sum/n))

