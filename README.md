# parcel_template_sandbox

This repository is a testbed for parcel template development. The main content is this notebook:

[REPM estimation.ipynb](https://github.com/urbansim/parcel_template_sandbox/blob/master/notebooks/REPM%20estimation.ipynb)

The notebook starts with a small amount of data and a couple of model steps from Paul Sohn's [urbansim_parcels](https://github.com/urbansim/urbansim_parcels) experiment. Then it goes through the workflow of buildings model steps using the new [ModelManager](https://github.com/urbansim/modelmanager) extension that treats model steps as first-class objects that can register themselves directly with Orca instead of needing to be added to a models.py file. So far, only OLS model steps are supported.

[ModelManager](https://github.com/urbansim/modelmanager) is the repository for the model step classes themselves. It's set up to be imported into other projects. 

This repository, parcel_template_sandbox, is meant to imitate what a particular UrbanSim project using a parcel template might look like. Feel free to add notebooks, or to copy/fork it for greater control. (If you add content directly to the repo, try to do it through branches and pull requests, so we can avoid merge conflicts.)