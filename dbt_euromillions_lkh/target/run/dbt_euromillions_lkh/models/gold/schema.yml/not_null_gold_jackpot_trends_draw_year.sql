
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select draw_year
from "analytics"."main"."gold_jackpot_trends"
where draw_year is null



  
  
      
    ) dbt_internal_test