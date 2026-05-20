
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select draw_date
from "analytics"."main"."silver_draws"
where draw_date is null



  
  
      
    ) dbt_internal_test