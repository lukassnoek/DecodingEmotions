# SharedStates

This repository contains the scripts and notebooks of the SharedStates project, corresponding to the submitted article:
Oosterwijk, Snoek, Rotteveel, Barrett, & Scholte. (in prep). Shared states: Using MVPA to test neural overlap between self-focused emotion imagery and other-focused emotion understanding.
***

## Dependencies
Most of the analyses documented in the repository depend on the *scikit-learn* package (http://scikit-learn.org/) and the *skbold* package (https://github.com/lukassnoek/skbold). The latter package is being developed alongside my PhD-project and includes some tools to make the construction of machine learning pipelines easier. Since submitting the paper for the first time, much of the code in the *skbold* package has changed. Therefore, the main (original) analyses depend on and older version of *skbold*, which has been branched off under the name 'SharedStates'. To install this 'version' of the package, you can use *pip*:
```
$ pip install git+https://github.com/lukassnoek/skbold.git@SharedStates
```
In response to several reviews, we have included additional analyses which depend on a more recent version of the *skbold* package, which can be installed as follows:
```
$ pip install git+https://github.com/lukassnoek/skbold.git@master
```

## Repo structure/contents:
* *ANALYSES*. This folder contains all scripts for the project.
* *MATERIALS_PROCEDURES_DESIGN*. This folder contains the Presentation (Neurobs) scripts used for stimulus presentation (Self-focused task and Other-focused task) and the stimulus materials.

***

## Docker image

To make the analyses from this study fully reproducible, I'm working on a Dockerfile to create a Linux environment with the appropriate software (FSL, Python packages, etc.), data (fMRI-data & metadata), and analysis-scripts (from the current repository). The image can be pulled as follows (warning: about 4 GB in size!):

```
$ docker pull lukassnoek/nibase
```

^ NOT YET FUNCTIONAL!
