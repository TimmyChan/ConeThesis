# NOTE:  InnerCone = Initial cone using random generator, C in paper                     
#        OutsideVector = Vector Outside cone C, v
#        OuterCone = Conical Hull of C union v, D


#from PyNormaliz import *
from sage.all import *


#==================#
# GLOBAL VARIABLES #
#==================# 

NUMOFTRIALS = 10
NUMOFTESTS = 100

# The number of generators used for the cone (useful for 3d and up)
NUMGEN = 10

# Internal Variable Definitions. Changes based on dimension.
x1,x2,x3 = var('x1,x2,x3')

# RESTRICTIONS ON RANDOM NUMBER GENERATOR. 
RMAX = 10
RMIN = -RMAX
INFINITYCORK = RMAX^2



# The number of significant digits used for floating point numbers 
# (display only does not affect accuracy)       
SIGFIG = 5
#=============================#
# OUTPUT FUNCTION DEFINITIONS #
#=============================#


# FORMATTING FUNCTION
def printseparator(): 
    print("================================================================")



# TAKES AN INTEGER ARRAY AND RETURNS A FREQUENCY TABLE (MEANT FOR PLOTTING DATA)
def frequencyArray(List):
    maximum = max(List)
    return [List.count(i) for i in range(maximum+1)]
        
        
        
# DISPLAY STATISTICS OF A LIST RAWDATA, WHERE EACH ENTRY IN THE LIST IS A TUPLE (# of steps, Cone, Vector)
def printStats(RawData, Final=False): 
    Data = [RawData[i][0] for i in range(len(RawData))]
    #print Data
    if Final:
        printseparator()
        print("DATA SUMMARY:")
        
    else:
        print("TRIAL STATS:")
    print("\tMean: {}\tMedian: {}\tMode: {}\n\tMin: {}\tMax: {} \n\tStandard Deviation: {}".format(N(mean(Data),digits=SIGFIG),  N(median(Data),digits=SIGFIG), mode(Data), min(Data), max(Data), N(std(Data),digits=SIGFIG)))
    if Final:
        index_min = min(xrange(len(Data)), key=Data.__getitem__) # GET THE INDEX OF THE MIN STEP
        minC = RawData[index_min][1]
        minD = RawData[index_min][2]
        #print("DEBUG: The index of the minimum value: {}, Minimum Value: {}".format(index_min, Data[index_min]))
        print("An initial condition that gave us the minimum number of steps:")
        printCD(minC,minD)

        index_max = max(xrange(len(Data)), key=Data.__getitem__) # GET THE INDEX OF THE MAX STEP        
        maxC = RawData[index_max][1]
        maxD = RawData[index_max][2]
        #print("DEBUG: The index of the maximum value: {}, Minimum Value: {}".format(index_max, Data[index_max]))
        print("An initial condition that gave us the maximum number of steps:")
        printCD(maxC,maxD)
        
        
        frequencyTable = frequencyArray(Data)
        plot(bar_chart(frequencyTable)).show()
        from pylab import boxplot,savefig
        b=boxplot(Data)
        savefig("sage1.png")
        
        
        
#=============================#
# GENERATE INITIAL CONDITIONS #
#=============================#

# Temporary Function
# Input: Number of extremeal generators (numgen) in the cone
# Description: Generates (numgen) many vectors in the halfspace z>0
#              and takes conical hull
# Returns: Cone
def generateCone(numgen):
    vects = [(0,0,0) for i in range(numgen)] # Empty list of vectors
    for i in range(numgen):
        vects[i] = (randint(RMIN,RMAX),randint(RMIN,RMAX),randint(1,RMAX))
        #print("Random Vector {} = {}".format(i,vects[i]))
    Temp = Cone(vects)
    #print Temp.rays()
    return Temp


# Function to generate a primitive rational vector
def GCD(a,b):
    return abs(a) if b==0 else GCD(b, a%b)
def GCD_List(*args):
    return reduce(GCD, args)
def generateRandomVector():
    a = randint(RMIN, RMAX)
    b = randint(RMIN, RMAX)
    c = 0
    d = GCD_List(a,b,c)
    return vector([a/d,b/d,c/d])

def generateOutsideVector(someCone):
    temp = generateRandomVector()                                             # Generate Some Random Vector
    #print("Generating Random Vector: {}".format(temp))                        
    while(someCone.contains(temp) or someCone.contains(-temp)):               # Loop to verify v not in C and -v not in C
        #if someCone.contains(temp):
            #print("{} is in the Cone.".format(temp))
        #else:
            #print("{} is in the Cone.".format(-temp,someCone.contains(-temp)))
        temp = generateRandomVector()
        #print("Generating Random Vector: {}".format(temp))     

    #print("All is well, returning: {}".format(temp))
    
    return temp

def generateInitialConditions(gencount, verbose=False):
    if verbose:
        def verboseprint(*args):
            for arg in args:
               print arg,
            print
    else:
        verboseprint = lambda *a: None 
    
    InnerCone = generateCone(gencount)
    OutsideVector = generateOutsideVector(InnerCone)
    
    InnerConeGenerators = InnerCone.rays()             # Collect all extremal generators of the inner cone

    OuterConeGenerators = []
    for point in InnerConeGenerators:
        OuterConeGenerators.append(point)
    OuterConeGenerators.append(OutsideVector)
    OuterCone = Cone(OuterConeGenerators)
    #print OuterCone.rays()
    return InnerCone, OuterCone, OutsideVector
    
    
    
    
# The step in the TOPDOWN algorithm after removing v
# 2.1 - Record the Hilbert basis of the outer cone
# 2.2 - Collect extremal generators that are not in fixed inner cone
# 2.3 - take the shortest extremal generator from step 2.2, remove from list in 2.1
# 2.4 - Take conical hull using list from step 2.3 
def TOPDOWNstep(Inner, Outer):
    ExtremalsNotInner = [] #To collect extremal generators not in C
    for point in Outer.rays():
        #print("Does the inner cone contain {}? {}".format(point,Inner.contains(point)))
        if(not Inner.contains(point)):
            ExtremalsNotInner.append(point) #append only when point is not in C
    '''
    if(ExtremalsNotInner == []):
        print("Extremal Generators of Outer Cone after initial step:\n{}".format(Outer.rays()))
        return    Inner
    '''
        
        #print ExtremalsNotInner
    ExtremalsLength = []
    for points in ExtremalsNotInner:
        ExtremalsLength.append(points[0]^2+points[1]^2+points[2]^2) #collect lengths of each vector
    #print ExtremalsLength
    shortestVectorIndex = ExtremalsLength.index(min(ExtremalsLength)) #getting the index of the shortest vector
    shortestVector = ExtremalsNotInner[shortestVectorIndex] #shortest extremal generator not in C
    HilbertBasis = Outer.Hilbert_basis()
    NewSet = []
    for point in HilbertBasis:
        NewSet.append(point)
    NewSet.remove(shortestVector)
    return Cone(NewSet)
    
#============================#
# BEGINNING OF TRIAL PROGRAM #
#============================#

def TOPDOWNtrial(verbose=False):
    if verbose:
        def verboseprint(*args):
            for arg in args:
               print arg,
            print
    else:
        verboseprint = lambda *a: None 
    
    C, D, v = generateInitialConditions(NUMGEN)
    
    verboseprint("Extremal Generators of the Inner Cone: \n{}".format(C.rays()))
    verboseprint("Vector Outside of Inner Cone: {}".format(v))
    verboseprint("Extremal Generators of the Outer Cone: \n{}".format(D.rays()))
    
    IntermediateCone = D
    
    # STEP 1.1: Take Hilbert Basis of Outer Cone
    HilbertBasis = IntermediateCone.Hilbert_basis()
    #print("Hilbert basis of the outer cone: \n{}".format(HilbertBasis))
    # STEP 1.2: Take Hilbert Basis and remove v (OutsideVector)
    IntermediateGenerators = [] #Container for the hilbert basis of D with v removed
    for point in HilbertBasis:
        IntermediateGenerators.append(point)
    IntermediateGenerators.remove(v)
    
    #print IntermediateGenerators
    IntermediateCone = Cone(IntermediateGenerators)
    verboseprint("Extremal Generators of Outer Cone after initial step:\n{}".format(IntermediateCone.rays()))
    
    stepcount = 1
    while(not(C.is_equivalent(IntermediateCone))):
        verboseprint("Just wrapped up step {}.\n".format(stepcount))
        IntermediateCone = TOPDOWNstep(C, IntermediateCone)
        verboseprint("Extremal Generators of Outer Cone after step {}:\n{}".format(stepcount, IntermediateCone.rays()))
        stepcount = stepcount + 1
        
    return stepcount, C, IntermediateCone
        
#==============#
# COLLECT DATA #
#==============#
AllDATA = [None]*(NUMOFTRIALS*NUMOFTESTS)
totalcounter = 0
print("Verbose Run for Accuracy Verification:")
TOPDOWNtrial(verbose=True)


print("\n\n")
print("Number of Tests: {} \nVector Coordinate Bound: (+/-){}".format((NUMOFTESTS*NUMOFTRIALS), RMAX))
printseparator()
for t in range(NUMOFTRIALS):
    
    DATA = [TOPDOWNtrial() for i in range(NUMOFTESTS)]
    print("TRIAL {}/{}: test # {} - {}".format(t+1,NUMOFTRIALS, totalcounter+1, totalcounter+NUMOFTESTS))
    printStats(DATA)
    for i in range(NUMOFTESTS):
        AllDATA[i+totalcounter] = DATA[i]
    totalcounter = totalcounter + NUMOFTESTS
    printseparator()
    
#print AllDATA
printStats(AllDATA,Final=True)