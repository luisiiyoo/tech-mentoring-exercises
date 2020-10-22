USE foodie;

SELECT * from menuEventMeals;
SELECT * from menuEvents;
SELECT * from meals;
SELECT * from diets;

SELECT 
	menuEvents.date, 
    diets.name AS diet,
    meals.name AS meal,    
    events.name AS event,
    offices.name AS office
from 
	menuEventMeals
INNER JOIN 
	meals ON menuEventMeals.meal = meals.id
INNER JOIN 
	diets ON meals.diet = diets.id
INNER JOIN 
	menuEvents ON menuEventMeals.menu_event = menuEvents.id
INNER JOIN 
	events ON menuEvents.event = events.id
INNER JOIN
	offices ON menuEvents.office = offices.id
WHERE 
	offices.name IN ('Guadalajara office')
AND 
	events.name IN ('Breakfast')
ORDER BY date ASC