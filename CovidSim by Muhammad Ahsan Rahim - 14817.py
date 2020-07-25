# -*- coding: utf-8 -*-
"""


@author: Ahsan Rahim
"""
import random
import math
from numpy.random import choice
import pandas as pd
import matplotlib.pyplot as plt




pop=[[] ,[] ,[] ,[] ,[] , []]
infected=[[] ,[] ,[] ,[] ,[] , []]
recovered=[[] ,[] ,[] ,[] ,[] , []]
#stores=[(10,10) , (35,20) , (50,50) , (75,75) , (15,75) , (80,30)]
stores=[(random.randrange(1000) , random.randrange(1000)) for i in range(10)]
day=0
pop_size=2000
psize=[]
isize=[]
rsize=[]
newCases=[]




covid_prob=[4 , 450 , 1600 , 3700 , 6800]

        

def gets_Covid(age):
    #print('testing')
    x=random.randrange(6800)
    
    if(age<17 and x <covid_prob[0]):
        return 1
    if(17<age<45 and x in range(covid_prob[0] , covid_prob[1]) ):
        return 1
    if(45<age<65 and x in range(covid_prob[1] , covid_prob[2]) ):
        return 1
    if(65<age<75 and x in range(covid_prob[2] , covid_prob[3]) ):
        return 1
    if(age>75 and x in range(covid_prob[3] , covid_prob[4]) ):
        
        return 1
    #print('Negative')
    return 0;




def recovers():
    x=random.randrange(100)
    if(x<10):
        return True
    else:
        return False
    
    
def distance(co1, co2):
    #print(co1)
   # print(co2,'Hi')
    
    return math.sqrt(pow(abs(co1[0] - co2[0]), 2) + pow(abs(co1[1] - co2[1]), 2))



def BaseDistance(personPos, infectedPos):
    #print(co1)
   # print(co2,'Hi')
   #print(personPos)
   for i in range(len(infectedPos)):
       if(math.sqrt(pow(abs(personPos[0] - infectedPos[i][0]), 2) + pow(abs(personPos[1] - infectedPos[i][1]), 2)) <5):
           return True
   return False


def printGraphs():
        
        plt.ion()
        
        #Line Plot
        fig = plt.figure(figsize = (10,5))
        ax1 = fig.add_subplot(1,2,1)
        ax1.plot(psize, label = 'Susceptible')
        ax1.plot(isize , label = 'Infected')
        ax1.plot(newCases , color='red' , label='New cases')
        ax1.plot(rsize, color='green' , label='Recovered')
        ax1.legend()
        
        
        
        
        #ScatterPlot
        ax2 = fig.add_subplot(1,2,2)
        ax2.scatter(*zip(*pop[1]) , label='Susceptible')
        ax2.scatter(*zip(*infected[1]) , color='red' , label='Infected')
        ax2.scatter(*zip(*stores) , color='black' , label= 'Stores')
        if(len(recovered[1])>0):    
            ax2.scatter(*zip(*recovered[1]) , color='lime',label='Recovered')
        ax2.legend()
        plt.title('Geographical Spread Distribution on Day '+ str(day))
    

def popToInfected(i):
    infected[0].append(pop[0].pop(i))
    infected[1].append(pop[1].pop(i))
    infected[2].append(pop[2].pop(i))
    infected[3].append(pop[3].pop(i))
    infected[4].append(pop[4].pop(i))
    infected[5].append(pop[5].pop(i))




def infectedtoRecovered(i):
    recovered[0].append(infected[0].pop(i))
    recovered[1].append(infected[1].pop(i))
    recovered[2].append(infected[2].pop(i))
    recovered[3].append(infected[3].pop(i))
    recovered[4].append(infected[4].pop(i))
    recovered[5].append(infected[5].pop(i))
    
    
    
def addInfection(x):
    
    for i in range(x):
        first= random.randrange(pop_size)
        pop[5][first]=1  
        popToInfected(first)
        
    
movement=[]
covid=[]

def SimulateCovid():
    global day
    for i in range(pop_size):
        
        #age
        pop[0].append(random.randrange(100))
        #position
        pop[1].append((random.randrange(1000) , random.randrange(1000)))
    
    
    for i in range(pop_size):
        #closestStore
        pop[2].append( min(stores, key=lambda x: distance(x,pop[1][i])))
        store_weights=[0.1]*(len(stores))
        x=stores.index(pop[2][i])
        store_weights[x]=0.5
        #Movement
        pop[3].append( (random.choices(population=stores, weights=store_weights , k=1)[0] , random.randrange(24)))
        #MovementTime
        pop[4].append(random.randrange(24))
        
        #covid status
        pop[5].append(0)
     
    
    
    
    
    #Add first 2 infections to begin spread
    addInfection(2)
    
    
    
    
    
    #This while loop runs until the virus completely ends with 0 active cases
    while(len(infected[0])>1):
        
        new=0
        movement=[ (random.choices(population=stores, weights=store_weights , k=1)[0] , random.randrange(24)) for x in range(len(pop[3]))]
     
        
        pop[3]=movement
        
        
        i=0
        while(i<len(pop[0]) and len(pop[1])>0):
            
            if( pop[3][i] in infected[3]  or BaseDistance(pop[1][i], infected[1] )):
                result=gets_Covid(pop[0][i])
                if(result==1):
                    #popDF=popDF['Covid'][i]=1
                    
                    pop[5][i]=1
                    popToInfected(i)
                    new+=1
                    i-=1;
            i+=1
            
        j=0
        while(j<len(infected[0]) and len(infected[0])>0):
            if(recovers()):
                infectedtoRecovered(j)
                j-=1
                
            j+=1
            
            
            
            
        psize.append(len(pop[0]))
        isize.append(len(infected[0]))
        rsize.append(len(recovered[0]))
        newCases.append(new)
        
        printGraphs()
        #print('Day' ,j)
        day+=1            
  
    data = {'Age': pop[0],'Position':pop[1] , 'closest Store':pop[2] , 'Movement':pop[3] ,'Movement Hour': pop[4], 'Covid' : pop[5]  }
    popDF=pd.DataFrame(data)
   
    data = {'Age': infected[0],'Position':infected[1] , 'closest Store':infected[2] , 'Movement':infected[3] ,'Movement Hour': infected[4], 'Covid' : infected[5]  }
    infectedDF=pd.DataFrame(data)
    
    print(popDF)
    print(day)
    
    
    
    
#run the simulation
    
print('\nThe simulation might take upto 60 seconds before displaying graphs. \n')

print("This simulation uses the infection probabilities of according to the WHO statistics of Newyork and with recovery rate of 0.1 \n")
print("The probability function gets activated if a person gets within a 5 unit radius of an infected person or visits the same store in the same hour as an infected person \n")
print("A person randomly visits a store per day and has a higher probability to visit his nearest store \n")


SimulateCovid()


    







