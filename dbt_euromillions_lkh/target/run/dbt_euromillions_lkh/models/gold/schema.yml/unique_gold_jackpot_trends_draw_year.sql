
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    draw_year as unique_field,
    count(*) as n_records

from "analytics"."main"."gold_jackpot_trends"
where draw_year is not null
group by draw_year
having count(*) > 1



  
  
      
    ) dbt_internal_test