select title from movies
join stars on movies.id = stars.movie_id
join people on stars.person_id = people.id
join ratings on ratings.movie_id = movies.id
where people.name like "chadwick boseman"
order by ratings.rating DESC
limit 5;