with od_top10 as
(SELECT origin_code as node_code,sum(NUMBER_OF_USERS::numeric)
 FROM mobile_dest
 group by origin_code
 order by sum(NUMBER_OF_USERS::numeric) desc
 limit 10)
select origin_code as source,destination_code as target, sum(NUMBER_OF_USERS::numeric) as weight
FROM mobile_dest
where origin_code in (select node_code from od_top10)
and origin_code != destination_code
group by origin_code, destination_code
having sum(NUMBER_OF_USERS::numeric) > 0;
