"""Trains a network on data simulated by ReLERNN_SIMULATE.py"""

import os,sys
relernnBase = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),"scripts")
sys.path.insert(1, relernnBase)

from Imports import *
from Simulator import *
from Helpers import *
from SequenceBatchGenerator import *
from Networks import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--projectDir',dest='outDir',help='Directory for all project output. NOTE: the same projectDir must be used for all functions of ReLERNN')
    parser.add_argument('--nEpoch',dest='nEpoch',help='Number of epochs to train over', type=int, default=250)
    parser.add_argument('--gpuID',dest='gpuID',help='Identifier specifying which GPU to use', type=int, default=0)
    args = parser.parse_args()


    ## Set up the directory structure to store the simulations data.
    DataDir = args.outDir
    trainDir = os.path.join(DataDir,"train")
    valiDir = os.path.join(DataDir,"vali")
    testDir = os.path.join(DataDir,"test")
    networkDir = os.path.join(DataDir,"networks")
    vcfDir = os.path.join(DataDir,"splitVCFs")


    ## Read in the window sizes
    wins=[]
    winFILE=os.path.join(networkDir,"windowSizes.txt")
    with open(winFILE, "r") as fIN:
        for line in fIN:
            ar=line.split()
            wins.append([ar[0],int(ar[1]),int(ar[2]),int(ar[3]),int(ar[4]),int(ar[5])])
    nSam=[]
    maxMean=0
    maxLen=0
    maxMax=0
    for i in range(len(wins)):
        maxMax=max([maxMax,wins[i][5]])
        maxMean=max([maxMean,wins[i][4]])
        maxLen=max([maxLen,wins[i][2]])
        nSam.append(wins[i][1])


    ## Define output files
    test_resultFile = os.path.join(networkDir,"testResults.p")
    test_resultFig = os.path.join(networkDir,"testResults.pdf")
    modelSave = os.path.join(networkDir,"model.json")
    weightsSave = os.path.join(networkDir,"weights.h5")


    ## Identify padding required
    maxSegSites = 0
    for ds in [trainDir,valiDir,testDir]:
        DsInfoDir = pickle.load(open(os.path.join(ds,"info.p"),"rb"))
        segSitesInDs = max(DsInfoDir["segSites"])
        maxSegSites = max(maxSegSites,segSitesInDs)
    maxSegSites = max(maxSegSites, maxMax)


    ## Set network parameters
    bds_train_params = {
        'treesDirectory':trainDir,
        'targetNormalization':"zscore",
        'batchSize': 64,
        'maxLen': maxSegSites,
        'frameWidth': 5,
        'shuffleInds':True,
        'sortInds':False,
        'center':False,
        'ancVal':-1,
        'padVal':0,
        'derVal':1,
        'realLinePos':True,
        'posPadVal':0,
              }


    ## Dump batch pars for bootstrap
    batchParsFILE=os.path.join(networkDir,"batchPars.p")
    with open(batchParsFILE, "wb") as fOUT:
        pickle.dump(bds_train_params,fOUT)


    bds_vali_params = copy.deepcopy(bds_train_params)
    bds_vali_params['treesDirectory'] = valiDir
    bds_vali_params['batchSize'] = 64

    bds_test_params = copy.deepcopy(bds_train_params)
    bds_test_params['treesDirectory'] = testDir
    DsInfoDir = pickle.load(open(os.path.join(testDir,"info.p"),"rb"))
    bds_test_params['batchSize'] = DsInfoDir["numReps"]
    bds_test_params['shuffleExamples'] = False


    ## Define sequence batch generator
    train_sequence = SequenceBatchGenerator(**bds_train_params)
    vali_sequence = SequenceBatchGenerator(**bds_vali_params)
    test_sequence = SequenceBatchGenerator(**bds_test_params)


    ## Train network
    runModels(ModelFuncPointer=GRU_TUNED84,
            ModelName="GRU_TUNED84",
            TrainDir=trainDir,
            TrainGenerator=train_sequence,
            ValidationGenerator=vali_sequence,
            TestGenerator=test_sequence,
            resultsFile=test_resultFile,
            outputNetwork=[modelSave,weightsSave],
            numEpochs=args.nEpoch,
            validationSteps=20,
            gpuID=args.gpuID)

    ## Plot results of predictions on test set
    plotResults(resultsFile=test_resultFile,saveas=test_resultFig)

    print("\n***ReLERNN_TRAIN.py FINISHED!***\n")

if __name__ == "__main__":
	main()