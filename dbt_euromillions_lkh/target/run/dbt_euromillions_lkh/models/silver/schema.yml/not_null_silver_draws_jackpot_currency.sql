
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select jackpot_currency
from "analytics"."main"."silver_draws"
where jackpot_currency is null



  
  
      
    ) dbt_internal_test