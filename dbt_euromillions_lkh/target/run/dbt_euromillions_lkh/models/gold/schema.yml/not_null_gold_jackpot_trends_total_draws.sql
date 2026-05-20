
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select total_draws
from "analytics"."main"."gold_jackpot_trends"
where total_draws is null



  
  
      
    ) dbt_internal_test