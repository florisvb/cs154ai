import random
import AvianAsker
import numpy as np

myAvianAsker = AvianAsker.myAvianAsker

nspecies = 200
nattributes = 288

def playgame(printvals=True):
    gameplay = GamePlay(cheat=False)
    gameplay.playgame(printvals=True)

def check_all_birds(cheat=True):
    gameplay = GamePlay(cheat=True)
    ans = gameplay.check_all_birds()
    return ans
    
class GamePlay:
    def __init__(self, cheat=False):
        self.cheat = cheat
        if cheat is True:
            self.database = AvianAsker.initialize()
        else:
            self.database = None
            
        self.initialize()
            
    #Example of a bad asker
    #Replace this part by your own function
    def myAvianAskerRandom(self,QAs):
        #First five questions are on attributes 
        if len(QAs) < 5:
            Q=random.randint(0,nattributes-1)
        #All others guess the species
        else:
            Q=random.randint(nattributes,nattributes+nspecies)
        return Q
        
    def check_all_birds(self):
        birdnum = 1
        results = [None]
        numQs = []
        while birdnum < nspecies:
            
            QAs = self.playgame(birdnum)
            results.append(QAs)
            numQs.append(len(QAs))
            birdnum += 1
            
        mean_numQs = np.mean(numQs)
        std_numQs = np.std(numQs)
        
        return mean_numQs, std_numQs, results
        
    def initialize(self):
        infile = open("specie_names.txt","r")
        self.train = infile.readlines()
        self.spec_dict={}
        for lines in self.train:
                entry=lines.split()
                self.spec_dict[entry[0]]= [entry[1],entry[2],entry[3]]
        infile.close()
                
        #Open self.train data
        infile = open("dataset.txt","r")
        self.id_dict={}
        self.attr_dict={}
        prev_entry = ""
        for lines in infile.readlines():
                entry = lines.split()
                if entry[0] != prev_entry:
                        self.attr_dict = {}
                self.attr_dict[entry[1]]=entry[2]
                self.id_dict[entry[0]]=self.attr_dict
                prev_entry = entry[0]
        infile.close()
        
        #Open attribute data
        infile = open("attributes.txt","r")
        self.Ques_dict = {}
        for lines in infile.readlines():
                entry = lines.split()
                attr = entry[1].split("::")
                name = attr[0].split('_')
                self.Ques_dict[entry[0]] = " ".join(name) + " of " + attr[1]
        infile.close()
        
    def playgame(self,bird=None, printvals=False):
        
        if bird == None:
            #Open random bird
            rndbrd = random.randint(1,len(self.train))
        else:
            rndbrd = bird
        
        print 'playing game with bird id: ', rndbrd

        #Begin new game
        QAs = []
        Q = None
        while Q is not -1:
            if self.cheat is False:
                Q = myAvianAsker(QAs)
            elif self.cheat is True:
                ans = myAvianAsker(QAs, database=self.database)
                Q = ans[0]
                self.database = ans[1]
            if Q-nattributes+1 == rndbrd:
                if printvals:
                    print("Is it "+" ".join(self.spec_dict[str(Q-nattributes+1)][1].split('_'))+"?")
                print("You have guessed correctly, the bird is "+" ".join(self.spec_dict[str(rndbrd)][1].split('_'))+"\n")
                break
            elif Q >= nattributes + nspecies:
                if printvals:
                    print("The question is out of range")
                continue
            elif Q >= nattributes and Q != rndbrd:
                if printvals:
                    print("Is it "+" ".join(self.spec_dict[str(Q-nattributes+1)][1].split('_'))+"?")
                print("Sorry, you are wrong!\n")
                A = '0' #incorrect guess
                break
            else:            
                if printvals:    
                    print("It "+ self.Ques_dict[str(Q)] +"?")
                A = self.id_dict[self.spec_dict[str(rndbrd)][0]][str(Q)];                       
                if A == '1':
                    if printvals:
                        print("Yes!\n")
                else:
                    if printvals:
                        print("No!\n")

            QAs.append([Q, A])
        return QAs
        
    
if __name__=='__main__':
    gameplay = GamePlay(cheat=True)
    gameplay.playgame(printvals=True)
    
    
