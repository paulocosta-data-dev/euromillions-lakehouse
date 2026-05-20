
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    draw_id as unique_field,
    count(*) as n_records

from "analytics"."main"."silver_draws"
where draw_id is not null
group by draw_id
having count(*) > 1



  
  
      
    ) dbt_internal_test