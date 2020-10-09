'''
Individual Conditional Expectations
'''

import pandas as pd
import numpy as np

# Learning Models
from sklearn.ensemble import RandomForestRegressor as RF
from sklearn.linear_model import LinearRegression as LM
import sklearn.metrics as m

from plotnine import *

import warnings
warnings.filterwarnings('ignore')


# %% Generate Synthetic Data -----------------------------------------

def gen_data(N=1000,seed=1234):

    # Set seed
    np.random.seed(seed)

    # Generate predictors
    x1 = np.random.normal(loc=0,scale=1, size = N)
    x2 = np.random.normal(loc=0,scale=1, size = N)
    x3 = np.random.normal(loc=0,scale=1, size = N)
    e = np.random.normal(loc=0,scale=1, size  = N)  # irreducible error

    # Generate outcome (which is a function of the predictors -- x3 intentionally left out)
    y = -2*np.cos(x1)*np.sin(x2) - x1 + x2 + -.75*x2**2 + e

    # Organize predictors
    X = np.stack([x1,x2,x3],axis=1)

    # Return the data
    return X,y


# %% -----------------------------------------

# Generate the sample of the data.
X, y = gen_data(N=250)

# Plot at the synthetic data
D= pd.DataFrame(dict(y=y,x1=X[:,0],x2=X[:,1],x3=X[:,2]))
(
    ggplot(D.melt(id_vars='y'),
           aes(x="value",y='y')) +
    geom_point(alpha=.25) +
    facet_wrap('variable') +
    theme(figure_size=(7,3))
)



# %% Build Model -----------------------------------------


# Linear model
mod_lm = LM()
mod_lm.fit(X,y)


# Random Forest model
mod_rf = RF()
mod_rf.fit(X,y)

# RF > LM
m.mean_squared_error(y,mod_lm.predict(X))
m.mean_squared_error(y,mod_rf.predict(X))

# Performance on future data.
test_X,test_y = gen_data(N=250,seed=2000)

m.mean_squared_error(test_y,mod_lm.predict(test_X))
m.mean_squared_error(test_y,mod_rf.predict(test_X))


# %% -----------------------------------------

# Same idea as the PDP, just don't average

X_tmp = X.copy()
target_var = 1
possible_values = np.arange(-3,3,.25)

ice_store = pd.DataFrame()
for val in possible_values:

    # Manipulate the value
    X_tmp[:,target_var] = val

    # Predict
    pred = mod_rf.predict(X_tmp)

    # Store the individual predictions
    vals = [val for i in range(pred.shape[0])]
    id = [i for i in range(pred.shape[0])]
    entry = pd.DataFrame(dict(id=id,val=vals,pred=pred))
    ice_store = ice_store.append(entry)

ice_store

# %% -----------------------------------------

# Visualize
(
    ggplot(data=ice_store) +
    geom_line(mapping=aes(x="val",y="pred",group="id"),alpha=.1) +
    theme_bw()
)

# %% -----------------------------------------

# PDP on top of the ICE

pdp = (ice_store
       .groupby("val").pred.mean()
       .reset_index()
       .rename(columns={"pred":'pdp'})
       .merge(ice_store,on="val",how="right")
       )


(
    ggplot(data=pdp) +
    geom_line(mapping=aes(x="val",y="pred",group="id"),alpha=.1) +
    geom_line(mapping=aes(x="val",y="pdp"),color="darkred",size=1.5) +
    theme_bw() +
    theme(figure_size = (10,5))
)
