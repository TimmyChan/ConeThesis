from sage.all import *
from sage.misc import *
import numpy as np

#=============================#
# OUTPUT FUNCTION DEFINITIONS #
#=============================#
SIGFIG = 2



# FORMATTING FUNCTION
def printseparator(FILE): 
    print("================================================================")
    FILE.write("================================================================")
    

# TAKES AN INTEGER ARRAY AND RETURNS A FREQUENCY TABLE (MEANT FOR PLOTTING DATA)
def frequencyArray(List):
    maximum = max(List)
    return [List.count(i) for i in range(maximum+1)]
        
        
def printCD(C,D,FILE):
    print("Inner Cone: \n{}\nOuterCone:\n{}".format(C.rays_list(),D.rays_list()))
    FILE.write("Inner Cone: \n{}\nOuterCone:\n{}".format(C.rays_list(),D.rays_list()))
    
# DISPLAY STATISTICS OF A LIST RAWDATA, WHERE EACH ENTRY IN THE LIST IS A TUPLE (# of steps, Cone, Vector)
def printStats(RawData,FILE, Final=False): 
    Data = [RawData[i][0] for i in range(len(RawData))]
    #print Data
    if Final:
        printseparator(FILE)
        print("DATA SUMMARY:")
        FILE.write("DATA SUMMARY:")
        
    else:
        print("TRIAL STATS:")
        FILE.write("TRIAL STATS:")
    print("\tMean: {}\tMedian: {}\tMode: {}\n\tMin: {}\tMax: {} \n\tStandard Deviation: {}".format(round(mean(Data),SIGFIG),  round(median(Data),SIGFIG), max(Data), min(Data), np.max(Data), round(std(Data),SIGFIG)))
    FILE.write("\tMean: {}\tMedian: {}\tMode: {}\n\tMin: {}\tMax: {} \n\tStandard Deviation: {}".format(round(mean(Data),SIGFIG),  round(median(Data),SIGFIG), max(Data), min(Data), np.max(Data), round(std(Data),SIGFIG)))
    
    if Final:
        index_min = min(xrange(len(Data)), key=Data.__getitem__) # GET THE INDEX OF THE MIN STEP
        minC = RawData[index_min][1]
        minD = RawData[index_min][2]
        #print("DEBUG: The index of the minimum value: {}, Minimum Value: {}".format(index_min, Data[index_min]))
        print("An initial condition that gave us the minimum number of steps ({}):".format(RawData[index_min][0]))
        
        FILE.write("An initial condition that gave us the minimum number of steps ({}):".format(RawData[index_min][0]))
        printCD(minC,minD,FILE)

        index_max = max(xrange(len(Data)), key=Data.__getitem__) # GET THE INDEX OF THE MAX STEP        
        maxC = RawData[index_max][1]
        maxD = RawData[index_max][2]
        #print("DEBUG: The index of the maximum value: {}, Minimum Value: {}".format(index_max, Data[index_max]))
        print("An initial condition that gave us the maximum number of steps ({}):".format(RawData[index_max][0]))
        FILE.write("An initial condition that gave us the maximum number of steps ({}):".format(RawData[index_max][0]))
        
        printCD(maxC,maxD,FILE)
        
        
        frequencyTable = frequencyArray(Data)

        from pylab import boxplot,savefig
        import datetime 

        c=plot(bar_chart(frequencyTable))
        b=boxplot(Data)
        imagefile = FILE.name[:-3] + ".png" 
        savefig(imagefile)

