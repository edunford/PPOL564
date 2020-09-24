----------------------------------------------------------------
-- PPOL564 | Data Science 1 | Foundations 
-- Week 8
-- Introduction to Queries using SQLite
-- Script is intended to work with the country.sqlite database 
----------------------------------------------------------------



-- list all available tables 
SELECT name FROM sqlite_master WHERE type='table'



-- Query the Available Tables
select * from life
select * from conflict
select * from econ
select * from regime
select * from continents



-- Head top of the data
select  * 
from life 
limit 5;



-- Select specific variables 
select  country, year, polity
from regime 
limit 5;



-------------------------------
--- ROW-WISE MANIPULATIONS ----
-------------------------------



-- Arranging
select 
	country, 
	ccode, 
	year, 
	riots
from conflict 
order by riots 


-- Arranging (descending order)
select 
	country, 
	ccode, 
	year, 
	riots
from conflict 
order by riots desc



-- Filtering 
select 
	country, 
	ccode, 
	year, 
	riots
from conflict 
where country = "Nigeria" 




-- Filtering (with AND)
select 
	country, 
	ccode, 
	year, 
	riots
from conflict 
where country = "Nigeria" and year >= 2000




-- Filtering (with OR)
select 
	country, 
	ccode, 
	year, 
	riots,
	protests
from conflict 
where riots > 20 or protests > 20




-----------------------------------
--- COLUMN-WISE MANIPULATIONS ----
-----------------------------------



-- Renaming variables
select  
	country as COUNTRY_NAME, 
	year as YEAR, 
	polity as POLITY
from regime 
limit 20;





-- Mutating 
select 
	country, 
	ccode, 
	year, 
	riots,
	protests,
	riots + protests as displays
from conflict 
order by displays desc




-- Mutating with ifelse logic 
select 
	country, 
	ccode, 
	year, 
	protests,
	(case when protests > 0 then "Protest" else "No Protest" end) as protest_onset
from conflict 





-- Mutating with more involved ifelse clauses 

select 
	country, 
	ccode, 
	year, 
	protests,
	case 
			when protests > 0  and protests <=10 then "low"  
		    when protests > 10 then "high" 
		    else "none" 
	 end as protest_cat
from conflict 





-- Mutating the variable type
select 
	country, 
	ccode, 
	cast(year as integer) as year, 
	cast(riots as float) as riots,
	protests
from conflict 
order by riots desc
limit 5





-----------------------------------------------
--- SUMMARIZATION & GROUPBY MANIPULATIONS ----
-----------------------------------------------



-- Distinct Values 
select 
	distinct country
from econ





-- Counting N observations
select 
	count(*) as n_obs
from conflict




-- Counting N distinct
select 
	count(distinct country) as n_countries 
from conflict





--Numerical Summaries
select 
	round(avg(riots),2) as ave_riots,
	sum(riots) as total_riots,
	min(riots) as min_riots,
	max(riots) as max_riots
from conflict 





-- GROUP BY  + Summarization
select 
	country,  
	year, 
	sum(riots) as riots,
	sum(protests) as protests
from conflict 
group by country, year






-- GROUP BY  + Counting 
select 
	country,  
	count(*) as n
from conflict 
group by country



-------------------------
--- TEMPORARY TABLES ----
-------------------------



-- Create a temporary table for the aggregated version of the conflict data.  
create temp table conflict_cy as
select 
		country,  
		year, 
		sum(riots) as riots,
		sum(protests) as protests
from conflict 
group by country, year



-- we can then later call this table when need be. 
select * from conflict_cy



-- deleting a temp table 
drop table conflict_cy


-- Must delete a temp table before overwritting an existing one. 




----------------------
--- JOINING TABLES ----
----------------------



-- INNER Joining Two Table
select 
	life.*,
	econ.ln_gdppc
from life
inner join econ on (life.ccode = econ.ccode and life.year=econ.year)



-- using monikers when joining
 select 
	a.*,
	b.ln_gdppc
from life a
inner join econ b on (a.ccode = b.ccode and a.year=b.year)



-- LEFT Joining Two Table
select 
	a.*,
	b.ln_gdppc
from life a
left join econ b on (a.ccode = b.ccode and a.year=b.year)


-- Joining on more than one table
select 
	a.*,
	b.ln_gdppc,
	c.regime_type
from life a
left join econ b on (a.ccode = b.ccode and a.year=b.year)
left join regime c on (a.ccode = c.ccode and a.year=c.year)




-- Unfortunately, SQLite does not support the RIGHT JOIN clause and also the FULL OUTER JOIN clause. 
-- However, you can easily emulate the FULL OUTER JOIN by using the LEFT JOIN clause.


-- Let's make this clear by creating two temporary tables


--- First only contains Nigeria and Egypt from 2011 onward
		create temp table tabA as
		select 
			country,
			cast(ccode as integer) as ccode,
			cast(year as integer) as year,
			round(ln_gdppc,2) as var1
		from econ 
		where country in ("Nigeria", "Egypt") and year > 2010



--- Second only contains Nigeria and Egypt from 2011 onward
		create temp table tabB as
		select 
			country,
			cast(ccode as integer) as ccode,
			cast(year as integer) as year,
			round(ln_gdppc,2) as var2
		from econ 
		where country in ("Nigeria", "Botswana") and year > 2010
		
		
select * from tabA
select * from tabB




--- Let's merge ... 
select 
	tabA.*,
	tabB.var2
from tabA
left join tabB on (tabA.country = tabB.country and tabA.ccode = tabB.ccode and tabA.year = tabB.year)



--- We can stack tables with a union (note that var2 field is lost when we do this)

select * 
from tabA
union all
select *
from tabB



--- To get it so that no values are dropped (a FULL MERGE) we'd need to do the following 
select 
	tabA.*,
	tabB.var2
from tabA 
left join tabB on (tabA.country = tabB.country and tabA.ccode = tabB.ccode and tabA.year = tabB.year)
union all
select
	tabB.country,
	tabB.ccode,
	tabB.year,
	tabA.var1,
	tabB.var2
from tabB
left join tabA on (tabA.country = tabB.country and tabA.ccode = tabB.ccode and tabA.year = tabB.year)
where tabA.var1 is null;






