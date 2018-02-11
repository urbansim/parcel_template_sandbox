import numpy as np
import pandas as pd
from datetime import datetime as dt

import orca
from urbansim.models import RegressionModel


class RegressionStep(object):
    """
    A class for building regression model steps. This wraps urbansim.models.
    RegressionModel() and adds a number of features:
    
    1. Allows passing all parameters needed for the model step at once.
    2. Allows direct registration of the model step with Orca and the ModelManager.
    3. Adds ModelManager metadata: type, name, tags.
    
    TO DO:
    - how to handle prediction data?
    
    Parameters
    ----------
    model_expression : str
        Passed to urbansim.models.RegressionModel().
    data : str or list of str
        Name(s) of Orca tables to draw estimation data from. The tables need to have 
        merge relationships ("broadcasts") registered so that 
    fit_filters : list of str, optional
        Passed to urbansim.models.RegressionModel().
    predict_filters : list of str, optional
        Passed to urbansim.models.RegressionModel().
    ytransform : callable, optional
        Passed to urbansim.models.RegressionModel().
    name : str, optional
    tags : list of str, optional
    
    """
    def __init__(self, model_expression, data, fit_filters=None, predict_filters=None,
                 ytransform=None, name=None, tags=[]):
        
        self.type = 'RegressionStep'
        self.name = name
        self.tags = tags
        
        # Generate a name if needed
        if (self.name == None):
            self.name = self.type + '-' + dt.now().strftime('%Y%m%d-%H%M%S')
    
        self.model = RegressionModel(model_expression=model_expression,
                fit_filters=fit_filters, predict_filters=predict_filters,
                ytransform=ytransform, name=name)
        
        tables = data  # TO DO: handle single table as well as list
        columns = self.model.columns_used()        
        self.df = orca.merge_tables(target=tables[0], tables=tables, columns=columns)

    
    def fit(self):
        """
        Estimate the model and report results.
        
        """
        self.model.fit(self.df)
        self.model.report_fit()
        
        
    def register(self):
        """
        Register the model step with Orca and the ModelManager. This includes saving it
        to disk so it will be automatically loaded in the future. 
        
        """
        None