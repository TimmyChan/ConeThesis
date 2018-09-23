# Computational Verification of the Cone Conjecture v1.0

Written and tested in Ubuntu 16.04.4 LTS (xenial), using the development branch of SAGE also.

This is a computational experiment, implementing the Top Down and Bottom Up algorithms found in "The Poset of Rational Cones" (https://msp.org/pjm/2018/292-1/p05.xhtml)

## Getting Started

### Dependencies
SAGE - Make sure to compile SAGE from source so that custom packages can be used! Download the developer branch from git.

```
https://github.com/sagemath/sage
```

Similarly, make Normaliz and PyNormaliz. *Need to document the installation process for getting the development branch*
pyNormaliz2

Check ticket #25090
``` https://trac.sagemath.org/ticket/25090```
Once closed.

1) Update sage by navigating to the sage folder, then do the following four commands:
```
1)	git checkout develop
2)	make
3)	sage -i normaliz
4)	sage -i pynormaliz
``` 

Check when a ticket is merged in which version:
https://groups.google.com/forum/#!forum/sage-release

### Instructions
Install dependencies, save the .py files listed below to the same directory. Then run from terminal in that directory:
```
chmod +x cone_conjecture_tester.py
./cone_conjecture_tester.py
```
And have fun~

The data will be outputted into the folder "DATA/{}d/experiment_name" where {} is the dimension of the experiment, and experiment_name is what you choose in the UI. 

Main .json file will be named the same as the experiment name.
Data Summary.text - read the title.
Graphs : 
"SIZE" - the number of hilbert basis elements.
"LENGTH" - the euclidean norm of the longest element of the hilbert basis element.


### Modules

#### cone_conjecture_tester.py
Main UI for interfacing with ConeChain objects, and allows user to create, load, generate and save data.
#### cone_chain.py
Data structure to store the possible poset chains and the algorithms top_down and bottom_up. 
#### cone_chain_element.py
Data structure to hold a polyhedral cone (sage.all.Polyhedra) and holds the hilbert basis of said cone, so that the calculation needs to only be done once.
#### cone_tools.py
Holds functions that are used in the top_down and bottom_up algorithms
#### experiment_io_tools.py
Holds I/O functions that simplify coding work for cone_conjecture_tester, such as custom menus and user input functions.
