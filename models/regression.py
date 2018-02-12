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
    
    Note that the same table and column names are used for both estimation and prediction,
    although the dependent variable may be different if needed. This is in alignment with
    the existing UrbanSim codebase.
    
    Parameters
    ----------
    model_expression : str
        Passed to urbansim.models.RegressionModel().
    tables : str or list of str
        Name(s) of Orca tables to draw data from. The first table is the primary one.
        Any additional tables need to have merge relationships ("broadcasts") specified
        so that they can be merged unambiguously onto the first table. 
    fit_filters : list of str, optional
        For estimation. Passed to urbansim.models.RegressionModel().
    out_fname : str, optional
        For prediction. Name of column to write fitted values to (in the primary table),
        if different from the dependent variable used for estimation.
    predict_filters : list of str, optional
        For prediction. Passed to urbansim.models.RegressionModel().
    ytransform : callable, optional
        For prediction. Passed to urbansim.models.RegressionModel().
    name : str, optional
        For ModelManager.
    tags : list of str, optional
        For ModelManager.
    
    """
    def __init__(self, model_expression, tables, fit_filters=None, out_fname=None,    
            predict_filters=None, ytransform=None, name=None, tags=[]):
        
        # Parameters needed outside the constructor
        self.tables = tables
        self.out_fname = out_fname
        self.type = 'RegressionStep'
        self.name = name
        self.tags = tags
        
        # Generate a name if none provided
        if (self.name == None):
            self.name = self.type + '-' + dt.now().strftime('%Y%m%d-%H%M%S')
    
        # TO DO: 
        # - Figure out what we can infer about requirements for the underlying data, and
        #   write an 'orca_test' assertion to confirm compliance.

        self.model = RegressionModel(model_expression=model_expression,
                fit_filters=fit_filters, predict_filters=predict_filters,
                ytransform=ytransform, name=name)

    
    def get_data(self):
        """
        Generate a DataFrame from Orca table and column names. The results should not be
        stored, in case the data in Orca changes between when the class is initialized 
        and when fit() or run() is invoked.
        
        """
        # TO DO: handle single table as well as list
        tables = self.tables
        columns = self.model.columns_used()
        df = orca.merge_tables(target=tables[0], tables=tables, columns=columns)
        return df
    
    
    def fit(self):
        """
        Estimate the model and report results.
        
        """
        results = self.model.fit(self.get_data())
        print(results.summary())
        
        
    def run(self):
        """
        Run the model step: calculate predicted values and use them to update a column.
        
        """
        # TO DO: 
        # - Figure out what we can infer about requirements for the underlying data, and
        #   write an 'orca_test' assertion to confirm compliance.
        # - If no destination column was specified, use name of dependent variable

        values = self.model.predict(self.get_data())
        print(len(values))
        
        dfw = orca.get_table(self.tables[0])
        dfw.update_col_from_series(self.out_fname, values, cast=True)
        
    
    def register(self):
        """
        Register the model step with Orca and the ModelManager. This includes saving it
        to disk so it will be automatically loaded in the future. 
        
        """
        None