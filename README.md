# DecodingEmotions

All analyses scripts for the Decoding Emotions study, which will be submitted as:
Oosterwijk, Snoek, Rotteveel, Barrett, & Scholte. (in prep). Shared states: Using MVPA to test neural overlap between self-focused emotion imagery and other-focused emotion understanding.

***

Note that this repository only contains scripts. The underlying algorithms, preprocessing functions, and other necessities for the machine learning pipeline come mostly from the *scikit-learn* package (http://scikit-learn.org/) and the *skbold* package (https://github.com/lukassnoek/skbold). The latter package is being developed alongside my PhD-project and includes some tools to make the construction of machine learning pipelines easier.

Folder structure/contents:
* *Analyses*. This folder contains all scripts for the project.
* *Behavioral_data*. This folder contains csv-files with behavioral and demographic data.
* *Stimulus_delivery*. This folder contains the Presentation (Neurobs) scripts used for stimulus presentation (Self-focused task and Other-focused task).

N.B.: The folder *statistics* contain Jupyter Notebooks that document how statistics have been calculated, how plots have been constructed, and other things that accompany the submitted manuscript.

***

## Docker image

To make the analyses from this study fully reproducible, I'm working on a Dockerfile to create a Linux environment with the appropriate software (FSL, Python packages, etc.), data (fMRI-data & metadata), and analysis-scripts (from the current repository). The image can be pulled as follows (warning: about 4 GB in size!):

```
docker pull lukassnoek/nibase
```

^ NOT YET FUNCTIONAL!
