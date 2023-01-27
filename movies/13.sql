
select  distinct name from people where id in
(select person_id from stars where movie_id in
(select movie_id from stars where person_id in
(select id from people where name like "kevin bacon" AND birth = 1958))) AND name not like "kevin bacon";