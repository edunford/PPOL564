### PRE-PROCESSING DATA ###

from sklearn.linear_model import LinearRegression
from sklearn import preprocessing as pp
import pandas as pd
import numpy as np

# Visualization
from plotnine import *
import warnings
warnings.filterwarnings("ignore")

# Data
from gapminder import gapminder as gap


# %% markdown -----------------------------------------

## Why pre-process data?



# %% -----------------------------------------

# Simulate some fake data
np.random.seed(123)
N=1000
x1 = np.random.normal(0,1,size=N)
x2 = np.random.normal(0,1,size=N)
y = x1 + x2 + np.random.normal(0,1,size=N)
ex_dat = pd.DataFrame(dict(y=y,
                           x1 = x1*500, # Scaling x1 by 500
                           x2 = x2))
ex_dat.head()



# %% -----------------------------------------

# plot the two distributions on one another
d = ex_dat[['x1','x2']].melt()
(
    ggplot(d,aes(x='value',fill = 'variable')) +
    geom_histogram(bins=30) +
    facet_wrap('variable',scales='free') +
    theme(figure_size = (10,5))
)

# But look what happens when we put them on the same scale
# set scales = "fixed"

# %% -----------------------------------------


# This point becomes clear when we try to model
mod = LinearRegression()
mod.fit(ex_dat[['x1','x2']],ex_dat.y)
mod.coef_




# %% markdown -----------------------------------------

### Preprocessing data transforms the data so that all the variables are on the same range.

### This helps `SKLEARN` estimate models.




# %% -----------------------------------------




X = ex_dat[['x1','x2']]
X = pp.scale(X)

mod.fit(X,ex_dat.y)
mod.coef_






# %% markdown -----------------------------------------

## Standardization

- Center the Mean ($\hat{x} = 0$)
- Unit variance ($var(x) = 1$)


$$x_{scaled} = \frac{x-\bar{x}}{\sigma_x}$$







# %% -----------------------------------------

#Implementation

X_train = np.array([[ 1., -1.,  2.],
                    [ 2.,  0.,  0.],
                    [ 0.,  1., -1.]])



# Initialize the scaling method
scaler = pp.StandardScaler()



# "fit" the method to your data and transform
scaler = scaler.fit(X_train)
X_scaled = scaler.transform(X_train)
X_scaled



# See that the property holds
X_scaled.mean(axis=0)
X_scaled.var(axis=0)










# %% markdown -----------------------------------------

### Why instantiate the scaler, e.g. `scaler = pp.StandardScaler()`, then fit?


- Anything we do to the *training* data we want to do to the *test* data.
- Need to ensure we're using the *same information* when we do this.




# %% -----------------------------------------



X_test = [[-1., 1., 0.]]
scaler.transform(X_test)


# Above scalar is using the mean and variation from the _training data_!
# When transforming the test data.

# Recall we don't want to use *ANY* information from the test data, even
# when we're transforming variables!






# %% markdown -----------------------------------------

## Other transformers

# %% markdown -----------------------------------------

## Range Scale

- $min(x) = 0$
- $max(x) = 1$

<br>

$$x_{range} = \frac{x-min(x)}{max(x) - min(x)}$$



# %% -----------------------------------------

# Implementation

X_train = np.array([[ 1., -1.,  2.],
                    [ 10.,  8.,  0.],
                    [ -2.,  1., -3.]])

min_max_scaler = pp.MinMaxScaler()
X_range = min_max_scaler.fit_transform(X_train)

X_range


# %% markdown -----------------------------------------

## Max Absolute Range Scalar



`MaxAbsScaler` works in a very similar fashion to `MinMaxScaler`, but scales in a way that the training data lies within the range [-1, 1] by dividing through the largest maximum value in each feature. It is meant for data that is already centered at zero or sparse data.

<br>

$$x_{range} = \frac{x-min(x)}{max(x) - min(x)}$$
$$x_{mars} = x_{range}\cdot(X_{max} - X_{min}) + X_{min}$$


# %% -----------------------------------------

# Implementation

X_train = np.array([[ 1., -1.,  2.],
                    [ 10.,  5.,  0.],
                    [ -2.,  1., -3.]])

max_abs_scaler = pp.MaxAbsScaler()
X_train_maxabs = max_abs_scaler.fit_transform(X_train) # Fit and transform in 1 step

X_train_maxabs







# %% markdown -----------------------------------------

## Rescaling doesn't change the distribution of your data!



# %% -----------------------------------------


(
    ggplot(gap,aes(x="gdpPercap")) +
    geom_histogram()
 )

# %% -----------------------------------------

mms = pp.MinMaxScaler()
new = mms.fit_transform(gap.gdpPercap.values.reshape(-1,1))
gap['gdp_scaled'] = new
(
    ggplot(gap,aes(x="gdp_scaled")) +
    geom_histogram()
 )





# %% markdown -----------------------------------------

## Dealing with Categories

- Transform categories, (.e.g `strings`) into numerical data
    + Convert to dummies
    + Convert to ordered scale.


# %% -----------------------------------------

# One Hot Encoder
enc = pp.OneHotEncoder()


cat = gap[['country']]
cat.head()

enc.fit(cat)
dummy = enc.transform(cat).toarray()
dummy


# Look at it as a data frame
pd.DataFrame(dummy,columns=gap.country.drop_duplicates())



# Recall, pandas also has a method that does this
pd.get_dummies(gap.country)







# %% -----------------------------------------

# Ordinal encoder - When we want to retain information on order

# Example Question data
questions =  [["Disagree","Neutral"],
              ["Agree","Agree"],
              ["Neutral","Disagree"],
              ["Agree","Disagree"]]
questions = pd.DataFrame(questions,columns=["Q1","Q2"])

enc = pp.OrdinalEncoder(categories=[
    ["Disagree","Neutral","Agree"],
    ["Disagree","Neutral","Agree"],
])
ordered_cats = enc.fit_transform(questions)


# Original
questions

# Transformed
ordered_cats














# %% markdown -----------------------------------------


## Takeaway
- Many more transformations. See [reading](https://scikit-learn.org/stable/modules/preprocessing.html)

- Choice on tranforming data depends on the data and the problem.

- Tranformations are "Tuning Parameters"! Choices we make that can alter the model's performance but that we can't learn from the data.
