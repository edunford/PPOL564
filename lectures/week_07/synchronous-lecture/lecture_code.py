import pandas as pd
import numpy as np
from plotnine import *
import seaborn as sns
import matplotlib.pyplot as plt
import missingno as msno # https://github.com/ResidentMario/missingno


# Ignore warnings
import warnings
warnings.filterwarnings('ignore')



# %% -----------------------------------------

# Import data
dat = (pd.read_csv("country_data.csv")
       .eval("ln_pop = log(pop)")
       .eval("ln_gdppc = log(gdppc)")
       .drop(columns=['gdppc','pop'])
       )

dat.head()






# %% markdown -----------------------------------------

## Asking Questions of Data

### Common questions to ask:

+ What is the unit of observation?
    - Is the data tidy?
    - What does each row signify?
    - Does the unit of observation map to your unit of analysis (i.e. the theoretical population you care about)?
+ What is the coverage of the data?
    - Time (year, months, days)
    - Space (countries, subnational units like states, census tracks, point locations)
    - Groups (relevant populations)
+ Who put the data together?
    - Why was the data created and for what purpose?
    - Potential source of bias? (e.g. does everyone on the research team look the same and come from the same background?)
+ **How was the data generated?**
    - Human vs. Machine
    - Coding procedures
+ **Is the data complete?**
    - Extent of missingness globally
    - Extend of missingness by subgroup

Remember you're almost always "borrowing" data, commandeering it to fit a purpose it wasn't entirely built for,
so we must always be wary of our data.

We must investigate it, vet it, make sure it's a good fit for our analytical needs.





















# %% markdown -----------------------------------------

## Numerical Summarization Techniques

# %% -----------------------------------------

# What is the dimensionality of the data
dat.shape

# What are the data types of the variables
dat.dtypes


# Convert data to the appropriate type
dat.year = dat.year.astype("int")
dat.ccode = dat.ccode.astype("int")
dat.country = dat.country.astype("category")
dat.continent = dat.continent.astype("category")
dat.regime_type = dat.regime_type.astype("category")

# Categorical variables are similar to factor variables in R
dat.continent.unique()

# Look at the type again.
dat.dtypes


################################
##### CONTINUOUS VARIABLES #####
################################

# Numerical summaries of each numeric variable
dat.describe()

# Can rotate and round
dat.describe(include="float").round(1).T


# How correlated are the continous variables with one another?
# We can see this easily with a correlation matrix.
dat.select_dtypes(include=['float64']).corr()



#################################
##### CATEGORICAL VARIABLES #####
#################################


# Categorical summaries of each Categorical variavle
dat.describe(include="category").T



# Breakdown of the different categories
dat.continent.value_counts()

dat.regime_type.value_counts()

dat.country.value_counts(ascending=True)




# FRUSTRATED by the limited print options? Change the default behavior.
pd.options.display.max_rows = 500
dat.country.value_counts(ascending=True)



# Crosstabs: look at differences across categorical data.
pd.crosstab(dat.regime_type,dat.continent,margins=True)


# Cross tabs represented as proportions
pd.crosstab(dat.regime_type,dat.continent).apply(lambda x: x/x.sum(), axis=1).round(3) # By Row

pd.crosstab(dat.regime_type,dat.continent).apply(lambda x: x/x.sum(), axis=0).round(3) # By Column


# Categorical by Continuous Data: use groupby and numerical summaries
dat.groupby(['continent'])['gdppc'].mean().sort_values(ascending=False)



# %% markdown -----------------------------------------

## Visual Summaries


# %% -----------------------------------------

################################
##### CONTINUOUS VARIABLES #####
################################


# Visualizing Distributions

(
    ggplot(dat,aes(x="ln_gdppc")) +
    geom_histogram()
)


# %% -----------------------------------------

# Visualizing many distributions by generating histograms for each variable

# Need to first alter
d = dat.select_dtypes(include="float").melt()
d.head()



(
    ggplot(d.dropna(),aes(x="value")) +
    geom_histogram() +
    facet_wrap("variable",scales="free") +
    theme(figure_size=(10,5))
)



# %% -----------------------------------------
# Visualizing Correlations

(
    ggplot(dat,aes(x = "ln_gdppc",y='ln_pop')) +
    geom_point()
)


# %% -----------------------------------------

# Visualizing many corrlations with a pairs scatter plot

d = dat.filter(["ln_gdppc","ln_pop","life_exp"])

g = sns.PairGrid(d,height=7)
g = g.map_diag(plt.hist)
g = g.map_offdiag(plt.scatter)


# %% -----------------------------------------

# Visualizing correlations as a heatmap
M = dat.select_dtypes(include=['float64']).corr()


plt.figure(figsize = (10,10))
sns.heatmap(M,center=0,linewidths=.5,cmap="magma")
plt.show()


# %% -----------------------------------------

# In plotnine
M = dat.select_dtypes(include=['float64']).corr()
M2 = M.unstack().reset_index().add_prefix('var')
M2.head()


(
    ggplot(M2,aes(x="varlevel_1",y="varlevel_0",fill="var0")) +
    geom_tile() +
    labs(x="",y="",fill="corr")
)






# %% markdown -----------------------------------------

## Fits and Trends


# %% -----------------------------------------

# Fit a linear trend

(
    ggplot(dat,aes(x = "ln_gdppc",y='infant_mort')) +
    geom_point(color="grey",alpha=.5) +
    geom_smooth(method="lm",se=False)
)

# %% -----------------------------------------

# Fit a loess (local regression)
(
    ggplot(dat,aes(x = "ln_gdppc",y='infant_mort')) +
    geom_point(color="grey",alpha=.5) +
    geom_smooth(method="loess",se=False)
)

# %% -----------------------------------------

# Group and break up the trends
(
    ggplot(dat,aes(x = "ln_gdppc",y='infant_mort',color="continent")) +
    # geom_point(alpha=.5) +
    geom_smooth(method="loess",se=False,size=1.5)
)

# %% -----------------------------------------

# Examine Trends Over time

(
  ggplot(dat,aes(x = "year",y='infant_mort',color="continent")) +
  geom_smooth(method="loess",se=False,size=1.5)
)



# %% -----------------------------------------

# Examine trends for specific countries.

# Break up by country
d = dat.query("continent == 'Oceania'")
d.country = d.country.astype("str") # Turn off the categorical var

(
  ggplot(d,aes(x = "year",y='infant_mort',color="country")) +
  geom_path(size=1) +
  xlim(1950,2010)
)

# %% -----------------------------------------

# Examine trends across multiple variables
d = dat.query("continent == 'Oceania'")
d.country = d.country.astype("str") # Turn off the categorical var
d2 = (d
      .filter(['country','year','infant_mort',"ln_gdppc","ln_pop"])
      .melt(id_vars=["country","year"])
      )

# Generate Plot
(
    ggplot(d2,aes("year","value",color="country")) +
    geom_path(size=1) +
    facet_wrap("variable",scales="free_y") +
    xlim(1960,2010) +
    labs(color="") +
    theme(legend_position="bottom",
          figure_size = (10,5),
          subplots_adjust={'wspace':0.15})
)



# %% markdown -----------------------------------------

## Dealing with Missing Data


# %% -----------------------------------------

# Detecting missing data

# Missing data by row
dat.isna().sum(axis=1)

# Missing data by column
dat.isna().sum(axis=0)

# %% -----------------------------------------

d = dat.melt(id_vars=["country",'year',"continent",'ccode'])
d = d.assign(missing = 1*d.value.isna())
d = d.groupby(['country','variable']).missing.sum().reset_index()


(
 ggplot(d,aes(x="variable",y="country",fill="missing")) +
 geom_tile() +
 theme(figure_size = (10,15))
)


# %% -----------------------------------------

# Visualizing Missing Data for a specfic variable
d = dat.assign(missing = 1*dat.infant_mort.isna())

(
 ggplot(d,aes(x="year",y="country",color="missing")) +
 geom_point() +
 facet_wrap("continent",scales="free_y",ncol=1) +
 theme(legend_position="bottom",
       figure_size = (10,20))
)


# %% -----------------------------------------

# Using missingno to assess missingnees.

msno.matrix(dat)



# %% -----------------------------------------

msno.bar(dat)



# %% -----------------------------------------

msno.heatmap(dat)








# %% markdown -----------------------------------------

## Resolving Missingness


# %% -----------------------------------------
dd =  dat.sample(10,random_state=123)

# Easiest solution, drop all missing values (listwise deletion)
dd.shape
dd.dropna().shape


# zoom in on the missing entries
dd.infant_mort.isna()

# Fill values with some value like a 0
dd.infant_mort.fillna(0)

# or the column mean
dd.infant_mort.fillna(dd.infant_mort.mean())

# Or other values like the column
dd.life_exp.fillna(dd.life_exp.median())


# for categorical data, fill in data with the most common case.
ee = pd.DataFrame(dict(cat = ["A","A","B",np.nan,"C"],id = [1,2,3,4,5]))
ee
ee.apply(lambda x: x.fillna(x.value_counts().index[0]))
