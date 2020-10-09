'''
Partial Dependency Plots
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
X, y = gen_data(N=1000)

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
test_X,test_y = gen_data(N=1000,seed=2000)

m.mean_squared_error(test_y,mod_lm.predict(test_X))
m.mean_squared_error(test_y,mod_rf.predict(test_X))


# %% -----------------------------------------

# The idea

X_tmp = X.copy()

# What is the average prediction with the X1 = 0?
X_tmp[:,0] = 0
pred = mod_rf.predict(X_tmp)
pred.mean()

# X1 = 1?
X_tmp[:,0] = 1
pred = mod_rf.predict(X_tmp)
pred.mean()

# X1 = 2?
X_tmp[:,0] = 2
pred = mod_rf.predict(X_tmp)
pred.mean()



# %% -----------------------------------------

# Let's do this systematically
X_tmp = X.copy()
target_var = 0
possible_values = np.arange(-3,3,.25)

store = list()
for val in possible_values:

    # Manipulate the value
    X_tmp[:,target_var] = val

    # Predict
    pred = mod_rf.predict(X_tmp)

    # Store the average prediction
    store.append([val,pred.mean()])


marginal_effect = pd.DataFrame(store,columns=['val','pred'])


# %% -----------------------------------------

# Visualize

(
    ggplot(marginal_effect,
           aes(x="val",y="pred")) +
    geom_path()
)


# %% -----------------------------------------


# Partial dependencies for two variables

X_tmp = X.copy()
possible_values = np.arange(-3,3,.5)
target_a = 0
target_b = 1

store = list()
for a in possible_values:

    # Manipulate the value for one variable
    X_tmp[:,target_a] = a

    for b in possible_values:

        # Manipulate the value for the other variable
        X_tmp[:,target_b] = b

        # Predict
        pred = mod_rf.predict(X_tmp)

        # Store the average prediction
        store.append([a,b,pred.mean()])


marginal_effect = pd.DataFrame(store,columns=['x0','x1','pred'])

# %% -----------------------------------------

# Visualize

(
    ggplot(marginal_effect,aes(x="x0",y="x1",fill="pred")) +
    geom_tile()
)
