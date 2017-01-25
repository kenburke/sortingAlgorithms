# You can do all of this in the `__main__.py` file, but this file exists
# to shows how to do relative import functions from another python file in
# the same directory as this one.

import numpy as np
import sys
import matplotlib.pyplot as plt
from .algs import quicksort, bubblesort

def basic_test():
    """
    This function is called in `__main__.py`
    Tests the sorting algorithms on small datasets for visual inspection of results.
    """
    print("This is `run()` from ", __file__)

    unsorted = np.random.rand(10)
    print("\n\tUnsorted input: ", unsorted)
    
    bsSorted = unsorted
    bubblesort(bsSorted)
    print("\n\tBubblesort output: ", bsSorted)
    
    qsSorted = unsorted
    quicksort(qsSorted)
    print("\n\tQuicksort output: ", qsSorted)
    
    print("\n\tBubblesort output == Quicksort output?  ", np.array_equal(bsSorted, qsSorted))
      
def complexity_experiment():
    """
    Tests complexity (as defined by time, assignments and conditionals) of
    the sorting algorithms as a function of input data size.
    """
    
    inputDataSizes = [100,200,300,400,500,600]#,700,800,900,1000]
    repsPerInputSize = 100
    
    assignments = np.zeros((2,len(inputDataSizes),repsPerInputSize))
    conditionals = np.zeros((2,len(inputDataSizes),repsPerInputSize))
    time = np.zeros((2,len(inputDataSizes),repsPerInputSize))
    
    progress = 0
    checkpoints = {'0':4,'1':8,'2':16,'3':24,'4':36,'5':48,'6':60,'7':72,'8':84,'9':100}

    print("\n------------------------------------------------\n")        
    print("\tTesting Bubblesort Complexity:")
    print("\tinputDataSizes = ", inputDataSizes)
    print("\trepsPerInputSize = ", repsPerInputSize,"\n")

    for i in range(0,len(inputDataSizes)):

        #run bubblesort many times for each input size
        for j in range(0,repsPerInputSize):
            data = np.random.rand(inputDataSizes[i])
            c, a, t = bubblesort(data)
            conditionals[0,i,j] = c
            assignments[0,i,j,] = a
            time[0,i,j] = t
            
        progress = checkpoints[str(i)]
        if str(i) in checkpoints.keys():
            update_progress(progress)
    
    print("\n------------------------------------------------\n")        
    print("\tTesting Quicksort Complexity:")
    print("\tinputDataSizes = ", inputDataSizes)
    print("\trepsPerInputSize = ", repsPerInputSize,"\n")
    progress = 0

    for i in range(0,len(inputDataSizes)):
    
        #run quicksort many times for each input size
        for j in range(0,repsPerInputSize):
            data = np.random.rand(inputDataSizes[i])
            c, a, t = quicksort(data)
            conditionals[1,i,j] = c
            assignments[1,i,j] = a
            time[1,i,j] = t

        progress = checkpoints[str(i)]    
        if str(i) in checkpoints.keys():
            update_progress(progress)
    
    print("\n------------------------------------------------\n")        
    
    complexity = {'assign':assignments,'cond':conditionals,'time':time}
    inputData = {'sizes':inputDataSizes,'reps':repsPerInputSize}
    
    return complexity, inputData

def complexity_visualize(complexity, inputData):
    
    #first get averages and stdev of assign, cond and time for each input data size for bubblesort
    meanBSAssign = np.average(complexity['assign'][0,:,:],axis=1)
    meanBSCond = np.average(complexity['cond'][0,:,:],axis=1)
    meanBSTime = np.average(complexity['time'][0,:,:],axis=1)
    stdBSAssign = np.std(complexity['assign'][0,:,:],axis=1)
    stdBSCond = np.std(complexity['cond'][0,:,:],axis=1)
    stdBSTime = np.std(complexity['time'][0,:,:],axis=1)
    
    #now quicksort
    meanQSAssign = np.average(complexity['assign'][1,:,:],axis=1)
    meanQSCond = np.average(complexity['cond'][1,:,:],axis=1)
    meanQSTime = np.average(complexity['time'][1,:,:],axis=1)
    stdQSAssign = np.std(complexity['assign'][1,:,:],axis=1)
    stdQSCond = np.std(complexity['cond'][1,:,:],axis=1)
    stdQSTime = np.std(complexity['time'][1,:,:],axis=1)
    
    
    fig = plt.figure(figsize=(20,10))
    st = fig.suptitle('Runtime, Assignments, Conditionals Comparison\nBubblesort (red) vs Quicksort (blue)\n',
        fontsize="x-large")
    
    #plot Runtime Differences (log scale)
    plt.subplot(231)
    plt.errorbar(inputData['sizes'],meanBSTime,yerr=stdBSTime,color="r")
    plt.errorbar(inputData['sizes'],meanQSTime,yerr=stdQSTime,color="b")
        
    plt.yscale('log')
    plt.ylabel('log')
    plt.title('Runtime (seconds)', fontsize=10)
    
    plt.axis([0.95*min(inputData['sizes']),1.1*max(inputData['sizes']),
        0.95*min(min(meanBSTime),min(meanQSTime)),1.3*max(max(meanBSTime),max(meanQSTime))])  
                      
    #plot Runtime Differences
    plt.subplot(234)
    plt.errorbar(inputData['sizes'],meanBSTime,yerr=stdBSTime,color="r")
    plt.errorbar(inputData['sizes'],meanQSTime,yerr=stdQSTime,color="b")
        
    plt.xlabel('Input Data Size')
    plt.ylabel('scalar')
    
    plt.axis([0.95*min(inputData['sizes']),1.1*max(inputData['sizes']),
        0.95*min(min(meanBSTime),min(meanQSTime)),1.2*max(max(meanBSTime),max(meanQSTime))])  
                  
    #plot Assign Differences (log)
    plt.subplot(232)
    plt.errorbar(inputData['sizes'],meanBSAssign,yerr=stdBSAssign,color="r")
    plt.errorbar(inputData['sizes'],meanQSAssign,yerr=stdQSAssign,color="b")
        
    plt.yscale('log')
    plt.title('Assignments', fontsize=10)
    
    plt.axis([0.95*min(inputData['sizes']),1.1*max(inputData['sizes']),
        0.95*min(min(meanBSAssign),min(meanQSAssign)),1.2*max(max(meanBSAssign),max(meanQSAssign))])  
                  
    #plot Assign Differences
    plt.subplot(235)
    plt.errorbar(inputData['sizes'],meanBSAssign,yerr=stdBSAssign,color="r")
    plt.errorbar(inputData['sizes'],meanQSAssign,yerr=stdQSAssign,color="b")
        
    plt.xlabel('Input Data Size')
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    plt.axis([0.95*min(inputData['sizes']),1.1*max(inputData['sizes']),
        0.95*min(min(meanBSAssign),min(meanQSAssign)),1.2*max(max(meanBSAssign),max(meanQSAssign))])  
        
    #plot Conditionals Differences (log)
    plt.subplot(233)
    plt.errorbar(inputData['sizes'],meanBSCond,yerr=stdBSCond, color="r")
    plt.errorbar(inputData['sizes'],meanQSCond,yerr=stdQSCond,color="b")
        
    plt.yscale('log')
    plt.title('Conditionals', fontsize=10)

    plt.axis([0.95*min(inputData['sizes']),1.1*max(inputData['sizes']),
        0.95*min(min(meanBSCond),min(meanQSCond)),1.2*max(max(meanBSCond),max(meanQSCond))])  
                  
    #plot Conditionals Differences
    plt.subplot(236)
    plt.errorbar(inputData['sizes'],meanBSCond,yerr=stdBSCond, color="r")
    plt.errorbar(inputData['sizes'],meanQSCond,yerr=stdQSCond,color="b")
        
    plt.xlabel('Input Data Size')
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    plt.axis([0.95*min(inputData['sizes']),1.1*max(inputData['sizes']),
        0.95*min(min(meanBSCond),min(meanQSCond)),1.2*max(max(meanBSCond),max(meanQSCond))])  

    #show and save                  
    plt.show()

    st.set_y(0.95)
    fig.subplots_adjust(top=0.85)
    
    fig.savefig("test.png")
    
    return

def complexity_test():

    complexity, inputData = complexity_experiment()
    
    complexity_visualize(complexity, inputData)

def update_progress(progress):
    sys.stdout.write('\r')
    sys.stdout.write('[{0}{1}] {2}%'.format('#'*(progress//2),' '*(50-progress//2),progress))    
    sys.stdout.flush()
    