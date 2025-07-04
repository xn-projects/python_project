'''
Use the view film_extended_view to avoid writing JOINs repeatedly.
This view combines the tables film, film_category, film_actor, actor, and category into a single unified table.
It simplifies queries and improves code readability.
'''
    
use sakila;
CREATE VIEW film_extended_view AS
SELECT
    f.film_id,
    f.title,
    f.description,
    f.release_year,
    f.rental_duration,
    f.rental_rate,
    f.length,
    f.rating,
    c.name AS category,
    GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name) SEPARATOR ', ') AS actors
FROM film f
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category c ON fc.category_id = c.category_id
JOIN film_actor fa ON f.film_id = fa.film_id
JOIN actor a ON fa.actor_id = a.actor_id
GROUP BY f.film_id, f.title, f.description, f.release_year, f.rental_duration, f.rental_rate, f.length, f.rating, c.name;
