# *ReLERNN*
## *Recombination Landscape Estimation using Recurrent Neural Networks*
====================================================================

ReLERNN uses deep learning to infer the genome-wide landscape of recombination from as few as two diploid samples.
This repository contains the code and instructions required to run ReLERNN, and includes example files to ensure everything is working properly.   

## Recommended installation on linux
Install `tensorflow-gpu` on your system. Directions can be found [here](https://www.tensorflow.org/install/gpu). We recommend using tensorflow version 1.13.1. You will need to install the CUDA toolkit and CuDNN as well as mentioned in the docs above.

Further dependencies for ReLERNN can be installed with pip.
This is done with the following command:

```
$ pip install ReLERNN
```

Alternatively, you can clone directly from github and install via setup.py using the following commands: 

```
$ git clone https://github.com/kern-lab/ReLERNN.git
$ cd ReLERNN
$ python setup.py install
```

It should be as simple as that.

## Testing ReLERNN
An example VCF file (10 haploid samples) and a shell script for running ReLERNN's four modules is located in $/ReLERNN/examples.
To test the functionality of ReLERNN simply use the following commands:

```
$ cd examples
$ ./example_pipeline.sh
```

Provided everything worked as planned, $ReLERNN/examples/example_output/ should be populated with a few directories along with the files: example.PREDICT.txt and example.PREDICT.BSCORRECT.txt.
The latter is the finalized output file with your recombination rate predictions and estimates of uncertainty.

The above example took 57 seconds to complete on a Xeon machine using four CPUs and one NVIDIA 2070 GPU.
Note that the parameters used for this example were designed only to test the success of the installation, not to make accurate predictions.
Please use the guidelines below for the best results when analyzing real data.
While it is possible to run ReLERNN without a dedicated GPU, if you do try this, you are going to have a bad time.

## Estimating a recombination landscape using ReLERNN
[Method flow](./methodFlow.png)
