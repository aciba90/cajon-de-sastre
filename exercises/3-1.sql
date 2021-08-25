-- Exercise 3-1
-- Retrieve the actor ID, first name, and last name for all actors. Sort by last
-- name and then by first name.
SELECT actor-id, first-name, last-name 
FROM actors
ORDER BY first-name, last-name