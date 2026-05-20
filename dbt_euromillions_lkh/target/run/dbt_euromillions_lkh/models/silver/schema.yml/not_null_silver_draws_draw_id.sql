
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select draw_id
from "analytics"."main"."silver_draws"
where draw_id is null



  
  
      
    ) dbt_internal_test