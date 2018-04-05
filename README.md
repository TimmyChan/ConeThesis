# Computational Verification of the Cone Conjecture v0.1.0

Tested in Ubuntu 16.04.4 LTS (xenial) as of April 5th, 2018.

This is a computational experiment, implementing the Top Down and Bottom Up algorithms found in "The Poset of Rational Cones" (https://msp.org/pjm/2018/292-1/p05.xhtml)

## Getting Started

### Dependencies
SAGE - Make sure to compile SAGE from source so that custom packages can be used! Download the master branch from

```
https://github.com/sagemath/sage
```

Similarly, make Normaliz and PyNormaliz 


### Instructions
Install dependencies then simply run
```
sage Experiment.py DIM
```

Where DIM is the ambient dimension for the test.


### Modules

#### Experiment.py
Wrapper file, defines global variables and calls on generateInitialConditions 
	----- Variables -----
	RMIN, RMAX 
		variables that control random number generators
	numgen 
		number of generators used in generateCone()


#### Init.py 
Generates Initial Conditions for the experiment.
	----- Functions -----
	generateRandomVector(dim, RMIN, RMAX, verbose=False)
		GCD_List(args): Returns 
		GCD(a,b): Returns gcd of a and b, returns a if b = 0.
	generateCone(dim, numgen, RMIN, RMAX, verbose=False)
		Generates proper full dimensional cone.
	generateOutsideVector(dim, SAGECone, RMIN, RMAX, verbose=False)
		Takes a cone, called SAGECone, and generates a vector v outside of the cone such that v and -v are both not in SAGECone.
	generateInitialConditions(dim, gencount, RMIN, RMAX, verbose=False)
		Calls the above functions, and returns C, D, v, where C is contained in D, with D as the conical hull of C and v.


#### TopDown.py 
Implements the Top Down Algorithm as described in "The Poset of Rational Cones"
	----- Functions -----
	TopDownTrial(C,D,v, verbose=False)
		Conducts the experiment using the TopDown algorithm
	TopDownStep(C,D,v, verbose=False)
		Conducts one step of the algorithm
		Takes Hilbert Basis of D, removes shortest extremal ray of D not contained in C
		Takes conical hull of vectors remaining from previous step, return this intermediate cone.


Goal: 
BottomUp4D.py - specialized module for 4D bottom up
  -> BottomUp.py - perhaps not possible...? Maybe?
