# Using SQL + Pandas

import pandas as pd
import sqlite3


# https://sqlitebrowser.org/


# Establish a connection with the database
conn = sqlite3.connect("country.sqlite")


# Use the connection with the read_sql() method
pd.read_sql('select * from econ',conn)


# We can write pretty much any query we would in SQLite,
# evalutate it, and then return back the results from
# the query.
query = '''
select
	life.country,
    cast(life.ccode as integer) as ccode,
    cast(life.year as integer) as year,
    life.infant_mort,
    round(life.life_exp,2) as life_exp,
	round(econ.ln_gdppc,2) as ln_gdppc
from life
left join econ on ( life.country = econ.country and
                    life.year=econ.year)
where life.country in ('Algeria','Botswana','Egypt') and life.year = 2000
'''

pd.read_sql(query,conn)



# USEFUL TIP: Listing off all the tables in your sqlite database
pd.read_sql("select name from sqlite_master where type='table'",conn)


# NOTE: different databases are going to require different connections,
# in addition to credentials. But the connection logic is the same.


# Disconnect from connection when you're done.
conn.close()



# %% -----------------------------------------

#############################################
##### BUILDING YOUR OWN SQLite DATABASE #####
#############################################

# Initializing a connection to a database that doesn't exists
# creates one.
conn = sqlite3.connect("my_db.sqlite")


# We can then write data to this database using .to_sql() method
dat1 = pd.DataFrame(dict(A = [1,2,3,4],
                         B = [3,5,.7,8]))

dat1.to_sql(name="data_A",con=conn,index=False)


# Now if we query the database, we see that it is there.
pd.read_sql("select name from sqlite_master where type='table'",conn)

# Everything follows as per usual
pd.read_sql("select * from data_A",conn)


# Close when finished
conn.close()
