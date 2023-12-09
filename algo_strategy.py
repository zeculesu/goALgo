import pandas as pd
import finta
import matplotlib.pyplot as plt

# Подключаем данные ЛЮБОЙ акции
data = pd.read_csv('GAZP_final_v2.csv', parse_dates=['begin', 'end'], encoding='cp1251')
# Обрезаем до последнего года, не обязательно
data = data.loc[150000:, :]
data = data.set_index('end')

parameters  = [210, 289, 860, 470, 66, 35, 28, 96, 1.6847228786653599, 0.4600834317359753]
#Следующие параметры это вторая стратегия, она лучше для графика
#Однако первая более прибыльная, если "не думать"
#Default это просто не ставить этот параметр, то бишь заменить его на ноль и убрать его индекс в коде
#parameters  = [21, 26, default, default, 21, 20, 10, 75, 1.01, 0.99]
#И еще sberbank просто название, потому что тестилось на нем, работает на ЛЮБОЙ акции
def sberbank_strategy(data):
        
        # Рассчитываем RSI
    data['rsi'] = finta.TA.RSI(data, int(parameters[0]))

        # Рассчитываем EMA (скользящую экспоненциальную среднюю) для закрытия
    data['ema_close'] = finta.TA.EMA(data, int(parameters[1]))

        # Рассчитываем Stochastic Oscillator
    data['stoch'] = finta.TA.STOCH(data, int(parameters[2]))

        # Рассчитываем MACD
    data['macd'] = finta.TA.MACD(data, int(parameters[3]))['MACD']

        # Рассчитываем объемы
    data['volume_ema'] = finta.TA.EMA(data, int(parameters[4]), 'volume')  # Используем EMA для сглаживания объемов

        # Создаем сигналы на основе пересечения различных индикаторов
    data['Signal'] = 0
        # Покупка: когда RSI < 20 и Stochastic < 10 и объем выше среднего
    data.loc[((data['rsi'] < int(parameters[5])) & (data['stoch'] < int(parameters[6])) & (data['volume'] > data['volume_ema'])), 'Signal'] = 1
        # Продажа: когда RSI > 80 и Stochastic > 90 и объем выше среднего
    data.loc[((data['rsi'] > (100-int(parameters[5]))) & (data['stoch'] > (100-int(parameters[6]))) & (data['volume'] > data['volume_ema'])), 'Signal'] = -1

        # Рассчитываем позицию
    data['Position'] = data['Signal'].diff()

        # Добавляем столбцы для уровней тейк-профита и стоп-лосса
    data['Take_Profit'] = data['close'] * parameters[8]
    data['Stop_Loss'] = data['close'] * parameters[9]

        # Усредняем позицию для сглаживания сигналов
    data['Smooth_Position'] = data['Position'].rolling(window=7).mean()

        # Фильтруем сигналы: покупаем только при значительном снижении RSI и продаем только при значительном росте RSI
    data.loc[(data['rsi'] > parameters[7]) & (data['Signal'] == 1), 'Signal'] = 0
    data.loc[(data['rsi'] < (100-parameters[7])) & (data['Signal'] == -1), 'Signal'] = 0

    return data

sberbank_data = sberbank_strategy(data)

# Визуализация результатов
plt.figure(figsize=(14, 8))

# График цены закрытия
plt.subplot(2, 1, 1)
plt.plot(sberbank_data['close'], label='Close Price', color='blue')
plt.title('Close Price with Signals')

# Используем sberbank_data.index вместо data.index
plt.scatter(sberbank_data.index[sberbank_data['Signal'] == 1], 
            sberbank_data['close'][sberbank_data['Signal'] == 1], 
            marker='^', color='g', label='Buy Signal')

# Используем sberbank_data.index вместо data.index
plt.scatter(sberbank_data.index[sberbank_data['Signal'] == -1], 
            sberbank_data['close'][sberbank_data['Signal'] == -1], 
            marker='v', color='r', label='Sell Signal')

plt.legend()

# График позиций и уровней тейк-профита/стоп-лосса
plt.subplot(2, 1, 2)
plt.plot(sberbank_data['Position'], label='Position', color='orange')
plt.plot(sberbank_data['Smooth_Position'], label='Smoothed Position', linestyle='dashed', color='purple')
plt.axhline(y=0, color='gray', linestyle='--', linewidth=2)

# Используем sberbank_data.index вместо data.index
plt.scatter(sberbank_data.index, 
            sberbank_data['Take_Profit'], 
            marker='o', color='green', label='Take Profit')

# Используем sberbank_data.index вместо data.index
plt.scatter(sberbank_data.index, 
            sberbank_data['Stop_Loss'], 
            marker='o', color='red', label='Stop Loss')

plt.legend()

# Показываем график
plt.show()
