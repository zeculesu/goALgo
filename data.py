import pandas as pd
import matplotlib.pyplot as plt


def get_data(ticker, data, start):  # тут имя акции
    table = pd.DataFrame()
    # data = "2023-12-01"  # тут сегодняшняя дата
    url = f'https://iss.moex.com/iss/engines/stock/markets/shares/securities/{ticker}/candles.csv?from={data}&interval=10&start={start}'
    df = pd.read_csv(url, sep=';', skiprows=2)
    table = pd.concat([table, df])
    return table


def draw_graf(filename, prices):
    # create figure
    plt.figure(figsize=(10, 10))

    # define width of candlestick elements
    width = .2
    width2 = .02

    # define up and down prices
    up = prices[prices.close >= prices.open]
    down = prices[prices.close < prices.open]

    # define colors to use
    col1 = 'black'
    col2 = 'steelblue'
    # plot up prices
    plt.bar(up.begin, up.close - up.open, width, bottom=up.open, color=col1)
    plt.bar(up.begin, up.high - up.close, width2, bottom=up.close, color=col1)
    plt.bar(up.begin, up.low - up.open, width2, bottom=up.open, color=col1)

    # plot down prices
    plt.bar(down.begin, down.close - down.open, width, bottom=down.open, color=col2)
    plt.bar(down.begin, down.high - down.open, width2, bottom=down.open, color=col2)
    plt.bar(down.begin, down.low - down.close, width2, bottom=down.close, color=col2)

    # rotate x-axis tick labels
    plt.xticks(rotation=45, ha='right', fontsize=6)

    # display candlestick chart
    plt.savefig(filename)


prices = get_data('YNDX', '2023-10-10', 16)[:15]
draw_graf('static/img/tbl3.png', prices)

prices = get_data('SBER', '2023-10-10', 0)[:15]
draw_graf('static/img/tbl4.png', prices)
prices = get_data('SBER', '2023-10-10', 16)[:15]
draw_graf('static/img/tbl5.png', prices)
