select
    draw_id,
    draw_date,
    jackpot_amount

from raw_silver_draws

where jackpot_amount > 0