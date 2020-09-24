# Building up a SQL Asset for example purposes. 

# - GDP per capita (table) - country-year 
# - Population per Capita (table) - country-year
# - Life Expectancy (table) - country-year
# - Conflict (table) - country-month 
# - Continent Key (table)

require(tidyverse)
require(gapminder)


# Connections 
con <- DBI::dbConnect(RSQLite::SQLite(), "lectures/week_08/data/sql_asset/country.sqlite")

# Data asset 
dat <- read_csv("lectures/week_07/synchronous-lecture/country_data.csv") %>% 
  filter(year > 1996) %>% 
  filter(continent=="Africa") 

# Regime type
dat %>% 
  select(country,ccode,year,regime_type,polity) %>% 
  copy_to(dest = con,df=.,name="regime",overwrite=T,temporary=F)

# Regime type
dat %>% 
  select(country,ccode,year,infant_mort,life_exp) %>% 
  copy_to(dest = con,df=.,name="life",overwrite=T,temporary=F)

# econ
dat %>% 
  mutate(ln_gdppc = log(gdppc),ln_pop = log(pop)) %>% 
  select(country,ccode,year,ln_gdppc,ln_pop) %>% 
  copy_to(dest = con,df=.,name="econ",overwrite=T,temporary=F)


# Continents 
dat %>% 
  distinct(continent,country,ccode) %>% 
  copy_to(dest = con,df=.,name="continents",overwrite=T,temporary=F)
  


# Conflict 
con2 = DBI::dbConnect(RSQLite::SQLite(), "~/Dropbox/Dataverse/conflict_database.sqlite")
DBI::dbListTables(con2)
acled = tbl(con2,"acled_all_africa_1997_2019") %>% collect()

# Export to db 
acled %>% 
  mutate(month = lubridate::month(as.Date(event_date))) %>% 
  count(country,year,month,event_type) %>% 
  pivot_wider(names_from = event_type,values_from = n,values_fill=0) %>% 
  janitor::clean_names() %>% 
  mutate(ccode = countrycode::countrycode(country,"country.name","cown")) %>% 
  select(country,ccode,everything()) %>% 
  copy_to(dest = con,df=.,name="conflict",overwrite=T,temporary=F)

# Disconnect  
DBI::dbDisconnect(con)
DBI::dbDisconnect(con2)
