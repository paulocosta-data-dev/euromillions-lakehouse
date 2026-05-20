select
    draw_id,
    draw_date,
    jackpot_amount,

    'EUR' as jackpot_currency,

    year(draw_date) as draw_year,

    month(draw_date) as draw_month

from raw_bronze_draws

where jackpot_amount > 0