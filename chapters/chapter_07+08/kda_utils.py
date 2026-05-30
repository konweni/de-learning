def compute_kda(kills, deaths, assists):
    # Реализовано безупречно. Функция max(deaths, 1) ювелирно защищает от деления на ноль,
    # если игрок выдал "сухой" матч с 0 смертей.
    result = (kills + assists) / max(deaths, 1)
    return result