select title from movies
join stars on stars.movie_id = movies.id
join people on stars.person_id = people.id
where people.name like "helena bonham carter"
INTERSECT
select title from movies
join stars on stars.movie_id = movies.id
join people on stars.person_id = people.id
where people.name like "johnny depp";