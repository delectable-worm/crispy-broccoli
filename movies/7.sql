select title,rating from movies
join ratings on ratings.movie_id = movies.id
where year = 2010
order by rating DESC, title