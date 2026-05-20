
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    draw_date as unique_field,
    count(*) as n_records

from "analytics"."main"."silver_draws"
where draw_date is not null
group by draw_date
having count(*) > 1



  
  
      
    ) dbt_internal_test