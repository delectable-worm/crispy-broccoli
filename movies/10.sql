select distinct name from people
join directors on directors.person_id = people.id
join ratings on directors.movie_id = ratings.movie_id
where rating >= 9.0;