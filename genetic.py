#Не обращайте внимание на слово sberbank, это рудимент, работает для всех акций
from deap import base, creator, tools, algorithms
import random
import pandas as pd
import finta
import numpy as np

# Определение типа задачи (минимизация или максимизация)
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
def simulate_trading(data):
    capital = 1000000  # Начальный капитал
    position = 0  # Начальная позиция

    for index, row in data.iterrows():
        if row['Signal'] == 1 and position == 0:
            # Покупка, только если нет открытой позиции
            position = capital / row['close']
            capital = 0
        elif row['Signal'] == -1 and position > 0:
            # Продажа, только если есть открытая позиция
            capital = position * row['close']
            position = 0

    # Последний день торговли
    if position > 0:
        capital = position * data['close'].iloc[-1]

    return capital
# Функция для оценки пригодности (наша стратегия)
def objective_function(parameters):
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

    data = pd.read_csv('GAZP_final_v2.csv', parse_dates=['begin', 'end'], encoding='cp1251')
    data = data.set_index('end')
    data = data.loc[:150000, :]
    sberbank_data = sberbank_strategy(data)
    
    res = simulate_trading(sberbank_data)
    print(parameters, res)
    return res,


# Определение операторов генетического алгоритма
toolbox = base.Toolbox()
toolbox.register("attr_int0", random.randint, 1, 100)
toolbox.register("attr_int1", random.randint, 1, 100)
toolbox.register("attr_int2", random.randint, 1, 100)
toolbox.register("attr_int3", random.randint, 1, 100)
toolbox.register("attr_int4", random.randint, 1, 100)
toolbox.register("attr_int5", random.randint, 1, 100)
toolbox.register("attr_int6", random.randint, 1, 100)
toolbox.register("attr_int7", random.randint, 1, 100)
toolbox.register("attr_float8", random.uniform, 1, 2)
toolbox.register("attr_float9", random.uniform, 0, 1)
toolbox.register("individual", tools.initCycle, creator.Individual,
                 (toolbox.attr_int0, toolbox.attr_int1, toolbox.attr_int2, toolbox.attr_int3, 
                  toolbox.attr_int4, toolbox.attr_int5, toolbox.attr_int6, toolbox.attr_int7, toolbox.attr_float8, toolbox.attr_float9),
                 n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", objective_function)

def main():
    population_size = 100
    generations = 50
    mutation_rate = 0.1

    # Генерация начальной популяции
    population = toolbox.population(n=population_size)

    # Определение статистики для мониторинга процесса оптимизации
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("max", max)

    # Запуск генетического алгоритма
    algorithms.eaMuPlusLambda(population, toolbox, mu=population_size, lambda_=population_size*2, cxpb=0.7, mutpb=mutation_rate, ngen=generations, stats=stats, halloffame=None)

    # Находим лучший индивид
    best_individual = tools.selBest(population, k=1)[0]
    print("Best Parameters:", best_individual)

if __name__ == "__main__":
    main()