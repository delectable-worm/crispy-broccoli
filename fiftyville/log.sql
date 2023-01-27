-- Keep a log of any SQL queries you execute as you solve the mystery.
-- getting report details
select * from crime_scene_reports
where year = 2021
and month = 7
and day = 28
and street like "humphrey%";

--getting bkery table
select * from bakery_security_logs
where year = 2021
and month = 7
and day = 28
and hour = 10;



--get more info
select name,transcript from interviews where transcript like "%bakery%";

-- matching licence plates
select * from people where license_plate in(
select license_plate from bakery_security_logs
where year = 2021
and month = 7
and day = 28
and hour = 10
and minute > 15 and minute < 25);

--bank withdrawals
select * from atm_transactions
where year = 2021
and month = 7
and day = 28
and atm_location like "legget%";

--intersect
select * from people
where id in -- bank
(select person_id from bank_accounts where account_number in
(select account_number from atm_transactions
where year = 2021
and month = 7
and day = 28
and atm_location like "legget%"))
intersect
select * from people -- license
where license_plate in
(select license_plate from bakery_security_logs
where year = 2021
and month = 7
and day = 28
and hour = 10
and minute > 15 and minute < 25);

--at this point, it may be easier to use raw numbers rather than keep everything sqlised
--get callers
select * from phone_calls
where (caller = "(829) 555-5269"
or caller = "(389) 555-5198"
or caller = "(770) 555-1861"
or caller = "(367) 555-5533")
and year = 2021
and month = 7
and day = 28;

--find receivers
select * from people
join phone_calls on receiver = phone_number
where (caller = "(829) 555-5269"
or caller = "(389) 555-5198"
or caller = "(770) 555-1861"
or caller = "(367) 555-5533")
and year = 2021
and month = 7
and day = 28;

--flights
select * from flights
where year = 2021
and month = 7
and day = 29
and origin_airport_id in
(select id from airports where city like "fiftyville")
order by hour, minute;

select * from people
join passengers on passengers.passport_number = people.passport_number
join flights on flights.id = passengers.flight_id
where flights.id = 36
and (people.id = 396669
or people.id = 467400
or people.id = 514354
or people.id = 686048);

select city from airports
where id=4;


