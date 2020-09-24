---------------------------------------
--- ANSWERS to WEEK 8 BREAKOUT ROOM ---
---------------------------------------


-- Question 1 --

select 
	continents.continent,
	econ.year,
	round(avg(econ.ln_gdppc),2) as ln_gdppc,
	round(avg(econ.ln_pop),2) as ln_gdppc,
	round(avg(life.infant_mort),2) as infant_mort,
	round(avg(regime.polity),2) as polity
from econ 
left join life on (econ.ccode = life.ccode  and econ.year = life.year)
left join regime on (econ.ccode = regime.ccode  and econ.year = regime.year)
left join continents on (econ.ccode = continents.ccode)
group by continents.continent, econ.year
order by avg(regime.polity)



-- Question 2 --
create temp table conflict_regime as 
select 
	conflict.country,
	conflict.year,
	regime.regime_type,
	sum(conflict.protests) as protests,
	sum(conflict.riots) as riots,
	sum(conflict.protests) + 	sum(conflict.riots) as popular_unrest
from conflict 
left join regime on (conflict.ccode = regime.ccode and conflict.year = regime.year)
where regime.regime_type is not NULL
group by conflict.country, conflict.year

select * from conflict_regime


-- Question 3 --
select 
	regime_type,
	sum(popular_unrest) as total_popular_unrest
from conflict_regime
group by regime_type
order by sum(popular_unrest) desc
	

