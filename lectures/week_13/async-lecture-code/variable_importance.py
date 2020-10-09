'''
Variable Importance
'''

import pandas as pd
import numpy as np

# Learning Models
from sklearn.ensemble import RandomForestRegressor as RF
from sklearn.linear_model import LinearRegression as LM
import sklearn.metrics as m

import matplotlib.pyplot as plt
import seaborn as sns
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


# %% Determining Variable Importance -----------------------------------------

# Determining Variable Importance

# Linear model is inherently interpretable. Just look at the coefficients (and t-stats...)
mod_lm.coef_

# For Black box model this is less clear.

# SIDE NOTE: Random Forest does have a way of calculating feature importance.
# But what we're interested in is a MODEL AGNOSTIC way to do this. We'd
# hate to have to restrict ourselves to a few models where interpreability was possible.
mod_rf.feature_importances_


# %% Permuting Data -----------------------------------------


v = np.array([1,3,5,2,6])
np.random.permutation(v)



# Idea: Permute the order of a specific feature to break the statistical
# association with the outcome. If the variable matters, then the model should
# performe WORSE.


baseline_performance =  m.mean_squared_error(y,mod_rf.predict(X))

# Make a copy (so we don't distort the actual data)
tmp = X.copy()

# permute a specific column.
tmp[:,0] = np.random.permutation(tmp[:,0])


perm_perf = m.mean_squared_error(y,mod_rf.predict(tmp))

# increase in the MSE
(perm_perf-baseline_performance)


# Permutating is a RANDOM PROCESS, so we want to permute a number of times

store = list()
times = 10
while times > 0:

    # Permute
    tmp[:,0] = np.random.permutation(tmp[:,0])

    # Calculate performance
    perm_perf = m.mean_squared_error(y,mod_rf.predict(tmp))

    # calc. reduction
    reduc = baseline_performance-perm_perf

    # Store value
    store.append(reduc)

    # Tick down
    times -= 1


# Get a distribution of values after 10 permutations.
store


# %% Doing this Systematically for all Features -----------------------------------------

def permutation_vi(model,X,y,n_permutations = 25):

    # Build a container
    store = {f"x_{i}":[] for i in range(X.shape[1])}

    # Iterate and permute the variables one at a time.
    for i, key in enumerate(store.keys()):

        baseline_performance =  m.mean_squared_error(y,model.predict(X))

        perms = n_permutations
        tmp = X.copy()

        while perms:

            # Permute
            tmp[:,i] = np.random.permutation(tmp[:,i])

            # Calculate performance
            perm_perf =  m.mean_squared_error(y,model.predict(tmp))

            # calc. reduction
            reduc = perm_perf - baseline_performance

            # Store value
            store[key].append(reduc)

            # Tick down
            perms -= 1

    # Turn it into a data object
    vi = pd.DataFrame(store)

    return vi


vi = permutation_vi(mod_rf,X,y)
vi.quantile([.025,.5,.975])


# %% -----------------------------------------

# Visualize
(
    ggplot(vi.melt(),aes(y="value",x='variable')) +
    geom_boxplot()  +
    coord_flip() +
    ylim(0,10)
)


# %% -----------------------------------------

# This method is useful because you can use it on any model and on out-of-sample data.

vi2 = permutation_vi(mod_rf,test_X,test_y)

(
    ggplot(vi2.melt(),aes(y="value",x='variable')) +
    geom_boxplot()  +
    coord_flip() +
    ylim(0,10)
)


# %% -----------------------------------------

# Let's use a completely different class of model, and the
# method still works. This is the model "agnostic" bit. 

from sklearn.svm import SVR

mod_svr = SVR()
mod_svr.fit(X,y)


vi3 = permutation_vi(mod_svr,X,y)


(
    ggplot(vi3.melt(),aes(y="value",x='variable')) +
    geom_boxplot()  +
    coord_flip() +
    ylim(0,10)
)



# %% -----------------------------------------

# Problematic when features are highly correlated.

# Set seed
np.random.seed(123)

# Generate correlated predictors
sigma = np.array([[1,.95],[.95,1]])
X = np.random.multivariate_normal([0,0],sigma, size = N)


(
    ggplot(pd.DataFrame(X,columns=["v1","v2"]),
           aes(y="v1",x="v2")) +
    geom_point()
)

# %% -----------------------------------------

# Now make those predictors a function of y

# Another var with no relationship
x3 = np.random.normal(loc=0,scale=1, size = N)

# Stack all the X together
X = np.stack([X[:,0],X[:,1],x3],axis=1)

# coefficients
b = np.array([-2,2,0])

# Error
e = np.random.normal(loc=0,scale=1, size  = N)

# y as a function of covars
y = X.dot(b) + e

mod_rf2 = RF()
mod_rf2.fit(X,y)


vi3 = permutation_vi(mod_rf2,X,y)

# %% -----------------------------------------

(
    ggplot(vi3.melt(),aes(y="value",x='variable')) +
    geom_boxplot()  +
    coord_flip() +
    ylim(0,10)
)
