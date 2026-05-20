
        
            delete from "analytics"."main"."gold_jackpot_trends"
            where (
                draw_year) in (
                select (draw_year)
                from "gold_jackpot_trends__dbt_tmp20260520123839204022"
            );

        
    

    insert into "analytics"."main"."gold_jackpot_trends" ("draw_year", "total_draws", "avg_jackpot", "max_jackpot", "min_jackpot", "total_jackpot_amount")
    (
        select "draw_year", "total_draws", "avg_jackpot", "max_jackpot", "min_jackpot", "total_jackpot_amount"
        from "gold_jackpot_trends__dbt_tmp20260520123839204022"
    )
  