# Info
**PMI: Python Modeling Interface**

Repository of Python classes to represent, score, sample 
and analyse models. It is based on the Integrative Modeling Platform 
[IMP](http://salilab.org/imp/).

**Installation:**

Clone this repository into the imp modules directory:

```
cd {imp_source}/modules
git clone https://github.com/salilab/pmi.git
```

Build IMP following the [imp instructions](http://www.integrativemodeling.org/nightly/doc/html/md_doxygen_generated_installation.html#installation).

**News February 28 2014**

The [clustering analysis](http://nbviewer.ipython.org/github/salilab/pmi/blob/master/examples/analysis/clustering_analysis.ipynb?create=1) calculates the localization densities

**News February 25 2014**

First working version of the [clustering analysis](http://nbviewer.ipython.org/github/salilab/pmi/blob/master/examples/analysis/clustering_analysis.ipynb?create=1). For the moment each cluster directory will only contain pdbs and rmfs
of the structures, but soon I'll add statistics, features and localization densities.

To have full speed install the mpi4py python library


**News February 10 2014**

Checkout the macros in macros.py

**News February 6 2014**

Added a FAQ section in the wiki. There will be ipython notebook tutorials soon.
Best IMP version so far: `ee1763c6859a29ab37415c8454d16549268d9668`
Previous versions had a bug in the RigidClosePairsFinder [bug](https://github.com/salilab/pmi/issues/19)


**News February 4 2014:**

Best IMP version so far: `b700fff93ca45ba1551c8aa9d697c805fcb126dc`
Previous versions might be considerably slow due to a [bug](https://github.com/salilab/imp/issues/724)

**News January 30 2014:**

Now the developed git branch is master and not resolution-zero.

If you want to use pmi, after you've freshly cloned it,
you don't have to checkout resolution-zero anymore:
it is the default branch that you get when you clone it.

The resolution-zero branch does not exist anymore,
it was copied into resolution-zero-old.

To see what branch you're in, run (into the pmi source code directory):

`git branch`

If you want to update the code and you still are in resolution-zero branch,
just run :

```
git checkout master
git pull
```

Note that the interface is also changing,
so you'll probably get deprecated warnings in your standard output more and more.
"grep deprecated"  to get the deprecation warnings, which might be lost in the middle of many other messages. Change your python script according to what the warnings say.
The old version of pmi (mainly used by Peter and SJ) is
still available under the tag "v0.1". To get it:

`git checkout tags/v0.1`



_Author(s)_: Riccardo Pellarin, Peter Cimermancic, Daniel Russel, Charles Greenberg, Elina Tjioe, Seung Joong Kim, Max Bonomi, Yannick Spill

_Maintainer_: Riccardo Pellarin

_License_: None

_Publications_:
- None
