
    
    

select
    draw_date as unique_field,
    count(*) as n_records

from "analytics"."main"."silver_draws"
where draw_date is not null
group by draw_date
having count(*) > 1


