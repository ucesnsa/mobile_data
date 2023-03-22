with od_top10dest as
(SELECT destination_code as node_code,sum(NUMBER_OF_USERS::numeric)
 FROM mobile_dest
  where 1=1
 @my_filter
 group by destination_code
 order by sum(NUMBER_OF_USERS::numeric) desc
 limit 10)
select ranked.* from
(select origin_code as source,destination_code as target, sum(NUMBER_OF_USERS::numeric) weight,
rank() over (partition by destination_code order by sum(NUMBER_OF_USERS::numeric) desc)
FROM mobile_dest
where destination_code in (select node_code from od_top10dest)
and origin_code != destination_code
@my_filter
group by origin_code, destination_code
having sum(NUMBER_OF_USERS::numeric) > 0) ranked
where rank < @edge_count;
