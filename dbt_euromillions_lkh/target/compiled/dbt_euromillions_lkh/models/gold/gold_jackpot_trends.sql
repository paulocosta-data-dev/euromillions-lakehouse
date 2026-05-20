

with source_data as (

    select *
    from "analytics"."main"."silver_draws"

),

aggregated as (

    select
        year(draw_date) as draw_year,

        count(*) as total_draws,

        avg(jackpot_amount) as avg_jackpot,

        max(jackpot_amount) as max_jackpot,

        min(jackpot_amount) as min_jackpot,

        sum(jackpot_amount) as total_jackpot_amount

    from source_data

    group by 1

)

select *
from aggregated



where draw_year not in (
    select draw_year
    from "analytics"."main"."gold_jackpot_trends"
)

