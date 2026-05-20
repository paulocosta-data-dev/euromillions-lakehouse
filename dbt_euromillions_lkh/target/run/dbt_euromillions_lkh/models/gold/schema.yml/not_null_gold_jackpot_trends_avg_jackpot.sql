
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select avg_jackpot
from "analytics"."main"."gold_jackpot_trends"
where avg_jackpot is null



  
  
      
    ) dbt_internal_test