#Creating an XOR Gate with NEAT(Neuroevolution of Augmenting Topologies)
#Created By:
#813 Brayden R
#Assisted By:
#817 Christopher Tan

#Current Date
#4/19/18

#====================================================================================================================================================

#Imports
from operator import itemgetter
from turtle import *
from random import *
from math import *

#====================================================================================================================================================

#Setup
inputs = [0, 1] # Current Goal: Nerual net to  make XOR gate
outputs = 1 #Number of output nodes
population = 10 #The number of genomes
innovation = 0 #Global innovation number
c1=1 #delta excess   
c2 = 1 #delta disjoint 
c3 = 0.4 #deltaweights
dthresh = 2 #The threshold for how similar genomes have to be in order to be considered the same species
stalespecies = 15 #How many generations it takes for an unchanging species to die
expected = [0,1,1,1] #Desired Output


mutateConnectionsChance = .80 #Chance connections will mutate
perturbChance = .90 #Chance that new weight will be perturbed instead of randomized when mutated
mutateDisableChance = .4 #Chance that a gene will be disabled when mutated
mutateEnableChance  = .2 #Chance that a gene will be enabled when mutated
crossoverChance = .75 #Chance of 2 genes from 2 genomes crossing (The rest of pop produced through mutation)
mutateNodeChance =0.03 #Chance of node being mutated(split)
mutateConnectionChance= 0.05 #Chance of a connection being created

doCompleteProgram = True

#====================================================================================================================================================

def poly(size,sides,col):
    startPos = pos()
    color(col)
    pu()
    goto(startPos[0] -size/2, startPos[1])
    pd()
    begin_fill()
    for i in range(sides):
        fd(size); lt(360/sides)
    end_fill()
    color('black')

def draw(genome,origin):
    ptlist = []
    pu(); goto(-100+ origin[0],origin[1]); pd()
    poly(40,4,'green')
    ptlist.append(pos())
    pu(); goto(origin); pd()
    circle(20)
    ptlist.append(pos())

    pu(); goto(100 + origin[0],origin[1]); pd()
    circle(20)
    ptlist.append(pos())
    
    pu(); goto(50+ origin[0],200+origin[1]); pd()
    circle(20)
    ptlist.append(pos())
    dx = 0
    try :
        for i in range(3,genome['numnodes']):
            pu()
            goto(-50 +dx+origin[0], 100+origin[1])
            pd(); circle(10)
            dx+= 50
            ptlist.append(pos())

            
    except:
        pass
    print('ptlist = ',ptlist)
    for g in genome['genes']:
        if g['enabled']:
            color('black')
        else:
            color('red')
        
        pu()
        goto(ptlist[g['outof']])
        pd()
        goto(ptlist[g['into']])
            
                       
                   
    


def findgene(genome,inno):
    for i in genome['genes']:
        if i['innovation'] == inno:
            return i
    return 0

def inno(i):
    global innovation
    try:
        for gene in pool['genes']:
            if i['into']==gene['into'] and i['outof']==gene['outof']:
                i['innovation']= gene['innovation']
    except:
        pass
    pool['genes'].append(i)
    if i['innovation'] == 0:
        innovation += 1
        i['innovation']= innovation
        
def sigmoid(x):
    return 2/(1+e**(-4.9*x))-1

def comp(genome1, genome2):
    maxino1 = 0
    for g in genome1['genes']:
        if g['innovation'] > maxino1:
            maxino1 = g['innovation']
    maxino2 = 0
    for g in genome2['genes']:
        if g['innovation'] > maxino2:
            maxino2 = g['innovation']
    if maxino2 < maxino1:
        maxino2, maxino1 = maxino1, maxino2
    e=0
    for i in range(maxino2-maxino1):
        e += 1
    wtot = 0
    numw = 0
    d = 0
    for i in genome2['genes']:
        for j in genome1['genes']:
            if i['innovation'] == j['innovation']:
                numw += 1
                wtot += abs(i['weight'] - j['weight'])
                break
    for i in range(1,maxino2+1):
        if findgene(genome1, i) == 0:
            if findgene(genome2,i) != 0:
                d+=1
        if findgene(genome2,i) == 0:
            if findgene(genome1,i) != 0:
                d+=1
            
    
        
        
    w = wtot/numw
    n= len(genome2)
    #print('e = ',e)
    #print('d = ',d)
    #print('w = ',w)
    #print('n = ',n)
    return (c1 * e)/n + (c2*d)/n + c3 *w

def sh(genome1, genome2):
    if comp(genome1,genome2) > dthresh:
        return 0
    else:
        return 1

def adjustedFit(genome):
    global pool
    tot = 0
    for i in pool['genomes']:
        tot += sh(genome, i)
    return fitness(genome,expected)/tot
        


#====================================================================================================================================================

def newPool():
    pool = {}
    pool['genes'] = []
    pool['genomes'] = []
    return pool

pool = newPool()

def newGene():
    gene = {}
    gene['into'] = 0
    gene['outof'] = 0
    gene['weight'] = 0.0
    gene['enabled'] = True
    gene['innovation'] = 0

    return gene
def copyGene(gene):
    gene2 = newGene()
    gene2['into'] = gene['into']
    gene2['outof'] = gene['outof']
    gene2['weight'] = gene['weight']
    gene2['enabled'] = gene['enabled']
    gene2['innovation'] = gene['innovation']

    return gene2
    
def newGenome():
    global pool
    genome = {}
    genome['genes'] = []
    genome['numnodes'] = 0
    genome['fitness'] = 0
    return genome
def newSpecies():
    species = {}
    species['topfit'] = 0
    species['staleness'] = 0
    species['genomes'] = {}
    species['averagefit'] = 0
    return species

##def newNode():
##    node = {}
##    node['incoming'] = {}
##    node['value'] = 0
##    return node
##        
def basicGenome():
    genome = newGenome()
    global innovation
    global pool
    for i in range(1,len(inputs)+1):
        g = newGene()
        genome['genes'].append(g)        
        g['into'] = len(inputs)+1
        g['outof'] = i
        g['weight'] = 2*random() -1
        inno(g)         
    genome['numnodes'] += len(inputs)+1
    pool['genomes'].append(genome)
    return genome       

def fitness(genome,expectedoutput):
    total = 0
    x=0
    for i in inputs:
        for j in inputs:
            total += abs((output(genome,i,j)- expectedoutput[x]))
            x+=1
    genome['fitness'] = abs(total)*-1 + 4
    return genome['fitness']

def output(genome, input1, input2):
    nodes = genome['numnodes']
    node_l = []
    tempNodeList = []
    for i in genome['genes']:
        tempNodeList.append(i['outof'])
        tempNodeList.append(i['into'])
    maxNodeNum = max(tempNodeList)
    for i in range(maxNodeNum+1):
        node_l.append(0)
    node_l[0] = 1
    node_l[1] = input1
    node_l[2] = input2
    for n in range(len(node_l)):
        total = 0
        for g in genome['genes']:
            if g['enabled']:
                if g['into'] == n:
                    try: total += node_l[g['outof']]* g['weight']
                    except: print('ERROR at: ',g['outof'], node_l)
        if total != 0:           
            node_l[n] = sigmoid(total)
    return node_l[len(node_l)-1]

def mutate_node(genome,gene):
    global innovation
    for i in genome['genes']:
        if i['innovation'] == gene:
            g = i
    g['enabled'] = False
    x = newGene()
    y = newGene()
    newnode = genome['numnodes']
    x['into']= g['into']
    x['outof']= newnode
    x['weight'] = g['weight']
    y['into'] = newnode
    y['outof'] = g['outof']
    y['weight'] = random()
    inno(x)
    inno(y)

    genome['genes'].append(x)
    genome['genes'].append(y)
    genome['numnodes'] += 1
def mutate_connection(genome):
    nodes = genome['numnodes']
    while True:
        node1 = round(random()*(nodes-1))
        node2 = round(random()*(nodes-1))
        if (node1 == 0 or node1 == 1) and (node2 == 0 or node2 == 1):
            pass
        else:
            x = True
            for g in genome['genes']:
                if (g['into'] == node2 and g['outof'] == node1) or (g['outof'] == node2 and g['into'] == node1):
                    x= False
            if x == True:
                break
    x = newGene()
    
    x['into'] = node2
    x['outof']= node1
    inno(x)
    genome['genes'].append(x)

def crossover(g1,g2):
    child = newGenome()
    innol = []
    if g1['fitness'] < g2['fitness']:
        g1,g2 = g2,g1
##    maxgenenum = max( len(g1['genes']), len(g2['genes'] ) )
    x= 1
    while True:
        if findgene(g1,x) == 0 and findgene(g2,x) == 0:
            break
        try: innol.append(findgene(g1,x)['innovation'])
        except: pass
        try: innol.append(findgene(g2,x)['innovation'])
        except: pass
        x+=1
    #print(innol)
    nonDupInnoL = list(set(innol))
    print('NON DUPE LIST = ',nonDupInnoL)
    y = False
    for i in nonDupInnoL:
        if findgene(g1,i) != 0 and findgene(g2,i) != 0:
                if random() < 0.5:
                    child['genes'].append( findgene(g1,i) )
                else:
                    child['genes'].append( findgene(g2,i) )
            #print('same = ',i)
        else:
            x = random()
            print('RANDOM = ',x)
            if x < 0.5:
                try:
                    if findgene(g1,i) != 0:
                           child['genes'].append(findgene(g1,i))
                           #print(i)
                    elif findgene(g2,i) != 0:
                           child['genes'].append(findgene(g2,i))
                           #print(i)
                except:
                    pass
            else:
                print('unlucky i = ',i)
    nodel = []
    for g in child['genes']:
        #print('g outof = ',g['outof'])
        try:
            nodel.index(g['outof'])
        except:
            nodel.append(g['outof'])
    try: nodel.index(2)
    except: nodel.append(2)
    #print(nodel)
    child['numnodes'] = len(nodel)                                      
    return child







    
#====================================================================================================================================================

#Testing

ht()
setup(.9,.9)

while doCompleteProgram:
    for i in range(population):
        x = basicGenome()
        adjustedFit(x )
    pool['genomes'].sort(key=itemgetter('fitness'))         #Sorting all genomes in respect to fitness
    for i in pool['genomes']:                                          #Assigning GlobalRank based on previous ordering
        i['globalrank'] = population - pool['genomes'].index(i)
    pool['genomes'].sort(key=itemgetter('globalrank'))  #Putting them in order in respect to GlobalRank
    
    

    
##    for genome in pool['genomes']:    #Testing
##        print(genome['globalrank'],genome['fitness'])
    
    
    
    doCompleteProgram = False
    print()
    print(pool['genomes'][0],pool['genomes'][1], len(pool['genomes']),sep = '\n\n')
    
##x = basicGenome()
##print(x)
##tracer(0)
##draw(x,(0,0))
##update()
##print(output(x,1,1))














##genome1 = basicGenome()
##genome2 = basicGenome()
##fitness(genome1,expected);
##print(); print()
##fitness(genome2,expected)
##mutate_node(genome1, 1)
##mutate_node(genome1, 2)
##mutate_node(genome2,1)
##mutate_connection(genome2)
####mutate_connection(genome2)
####print(comp(genome1, genome2),'\n\n')
####print(genome1,'\n')
####print(genome2,'\n')
##print(genome1,'\n\n', genome2)
##print('\n\n\n\n\n')
##child = crossover(genome1, genome2)
##print('\n\n\n\n\n')
##print('\n',child,'\n\n')
##fitness(child, expected)
##print(child)
##
##draw(genome1,(100,100))
##draw(genome2,(-200,100))
##draw(child,(-100,-200))



##print(tot,'\n')
##print(len(pool['genomes']),'\n')
##print(fitness(genome1,expected))
##print(fi(genome1))
##print(genome1,end = '\n \n')
##print(len(genome1['genes']))
##mutate_connection(genome1)
##mutate_node(genome1,1)
##print('fitness = ',fitness(genome1,[0,1,1,1]), end = '\n \n')
##print(genome1,end = '\n \n')
##print(len(genome1['genes']))
#Random ------------------------------------------------------
##bestfit = pool['genomes'][0]
##gen = 0
##x=True
##while x==True:
##    for i in range(population):
##        genome = basicGenome()
##        if fitness(genome, [0,1,1,1]) > 3.968:
##           print('\n',genome,'\n')
##           x=False
##           break
##    for genome in pool['genomes']:
##        if genome['fitness'] > bestfit['fitness']:
##            bestfit = genome
##            print(bestfit['fitness'],'generation ',gen)
##    gen+=1
##    


