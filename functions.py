import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def get_data(filename):
    data_file = pd.read_csv(filename)
    dates = [d for d in data_file['Data']]
    openings = [o for o in data_file['Otwarcie']]
    data = {
        'dates': dates,
        'openings': openings
    }
    return data


def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    prices = data['openings']

    short_ema = pd.Series(prices).ewm(span=short_window, min_periods=short_window).mean()
    long_ema = pd.Series(prices).ewm(span=long_window, min_periods=long_window).mean()

    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=signal_window, min_periods=signal_window).mean()

    data['macd_line'] = list(macd_line)
    data['short_ema'] = list(short_ema)
    data['long_ema'] = list(long_ema)
    data['signal_line'] = list(signal_line)


def generate_signals(macd_line, signal_line):
    buy_signals = []
    sell_signals = []
    for i in range(1, len(macd_line)):
        if macd_line[i] > signal_line[i] and macd_line[i - 1] <= signal_line[i - 1]:
            buy_signals.append(i)
        elif macd_line[i] < signal_line[i] and macd_line[i - 1] >= signal_line[i - 1]:
            sell_signals.append(i)
    return buy_signals, sell_signals


def simulate(data, data_buy_signals, data_sell_signals, money = 1000, invested = 0):
    data['money'] = [money]
    data['invested'] = [invested]
    data['hypothetical_money'] = [money + invested*data['openings'][0]]

    for i in range(1, len(data['dates'])):
        data['money'].append(money)
        data['invested'].append(invested)
        data['hypothetical_money'].append(money + invested*data['openings'][i])

        if(i in data_buy_signals and money > 0):
            buy_amount = money
            invested += buy_amount/data['openings'][i]
            money -= buy_amount
            print("Transaction!", str(data['dates'][i]))
            print("Exchange: ", str(data['openings'][i]))
            print("Bought " + str(buy_amount/data['openings'][i]) + " stuff for " + str(buy_amount) + " money.")
            print("Money: " + str(money))
            print("Stuff: " + str(invested))
            print()

        if (i in data_sell_signals and invested > 0):
            sell_amount = invested
            money += sell_amount*data['openings'][i]
            invested -= sell_amount
            print("Transaction!", str(data['dates'][i]))
            print("Exchange: ", str(data['openings'][i]))
            print("Sold " + str(sell_amount*data['openings'][i]) + " stuff for " + str(sell_amount) + " money.")
            print("Money: " + str(money))
            print("Stuff: " + str(invested))
            print()


def simulation_statistics(data, name="data"):
    print()
    print("STATISTICS for " + name)
    print('Starting money: ' + str(data['hypothetical_money'][0]))
    print('Ending money: ' + str(data['hypothetical_money'][-1]))
    print('Earnings: ' + str(data['hypothetical_money'][-1] - data['hypothetical_money'][0]))
    print('Money multiplier: ' + str(data['hypothetical_money'][-1] / data['hypothetical_money'][0]))
    print('Best moment: ' + str(max(data['hypothetical_money'])))
    print('Worst moment: ' + str(min(data['hypothetical_money'])))
    print('----------------------------')
    print('Starting exchange: ' + str(data['openings'][0]))
    print('Ending exchange: ' + str(data['openings'][-1]))
    print('Exchange multiplier: ' + str(data['openings'][-1] / data['openings'][0]))
    print('----------------------------')

def plot_macd(data):
    #plt.plot(data['dates'], data['openings'], label='Openings')
    #plt.plot(data['dates'], data['short_ema'], label='Short EMA')
    #plt.plot(data['dates'], data['long_ema'], label='Long EMA')
    plt.plot(data['dates'], data['signal_line'], label='Signal Line')
    plt.plot(data['dates'], data['macd_line'], label='MACD')

    plt.xticks([
        data['dates'][0],
        data['dates'][int(len(data['dates']) / 3)],
        data['dates'][int(2 * len(data['dates']) / 3)],
        data['dates'][-1]
    ])

    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('MACD Analysis')
    plt.legend()
    plt.show()


def plot_openings(data, simulation = False, data_buy_signals = False, data_sell_signals = False):
    plt.plot(data['dates'], data['openings'])
    plt.xticks([
        data['dates'][0],
        data['dates'][int(len(data['dates']) / 3)],
        data['dates'][int(2 * len(data['dates']) / 3)],
        data['dates'][-1]
    ])
    if simulation:
        plt.scatter([data['dates'][d] for d in data_buy_signals],
                           [data['openings'][d] for d in data_buy_signals], color='green', marker='^', label='Kupno',
                           s=50)
        plt.scatter([data['dates'][d] for d in data_sell_signals],
                           [data['openings'][d] for d in data_sell_signals], color='red', marker='v', label='Sprzedaż',
                           s=50)

    plt.xlabel('Date')
    plt.ylabel('Opening')
    plt.title('Openings by dates')
    plt.show()


def plot_simulation(data):
    plt.plot(data['dates'], data['hypothetical_money'], label='Hypothetical money')
    #plt.plot(data['dates'], data['money'], label='Money')

    plt.xticks([
        data['dates'][0],
        data['dates'][int(len(data['dates']) / 3)],
        data['dates'][int(2 * len(data['dates']) / 3)],
        data['dates'][-1]
    ])

    plt.xlabel('Date')
    plt.ylabel('Hypothetical money')
    plt.title('Simulation')
    plt.legend()
    plt.show()


def plot_data(data, data2, data_buy_signals, data_sell_signals, data2_buy_signals, data2_sell_signals):
    # Initialise the subplot function using number of rows and columns
    figure, axis = plt.subplots(3, 2)

    # Openings D1
    axis[0, 0].plot(data['dates'], data['openings'])
    axis[0, 0].set_title("Openings Data 1")

    axis[0, 0].scatter([data['dates'][d] for d in data_buy_signals], [data['openings'][d] for d in data_buy_signals], color='green', marker='^', label='Kupno', s=20)
    axis[0, 0].scatter([data['dates'][d] for d in data_sell_signals], [data['openings'][d] for d in data_sell_signals], color='red', marker='v', label='Sprzedaż', s=20)

    # MADC D1
    axis[1, 0].plot(data['dates'], data['signal_line'], label='Signal Line')
    axis[1, 0].plot(data['dates'], data['macd_line'], label='MACD')
    axis[1, 0].set_title("MADC Data 1")

    # Simulation D1
    axis[2, 0].plot(data['dates'], data['hypothetical_money'], label='Hypothetical money')
    axis[2, 0].set_title("Hypothetical money")


    # Openings D2
    axis[0, 1].plot(data2['dates'], data2['openings'])
    axis[0, 1].set_title("Openings Data 2")

    axis[0, 1].scatter([data2['dates'][d] for d in data2_buy_signals], [data2['openings'][d] for d in data2_buy_signals],
                       color='green', marker='^', label='Kupno', s=20)
    axis[0, 1].scatter([data2['dates'][d] for d in data2_sell_signals], [data2['openings'][d] for d in data2_sell_signals],
                       color='red', marker='v', label='Sprzedaż', s=20)

    # MADC D2
    axis[1, 1].plot(data2['dates'], data2['signal_line'], label='Signal Line')
    axis[1, 1].plot(data2['dates'], data2['macd_line'], label='MACD')
    axis[1, 1].set_title("MADC Data 2")

    # Simulation D1
    axis[2, 1].plot(data2['dates'], data2['hypothetical_money'], label='Hypothetical money')
    axis[2, 1].set_title("Hypothetical money 2")

    for i in (0, 1, 2):
        axis[i, 0].set_xticks([
            data['dates'][0],
            data['dates'][int(len(data['dates']) / 3)],
            data['dates'][int(2 * len(data['dates']) / 3)],
            data['dates'][-1]
        ])
        axis[i, 0].set_xticklabels([
            data['dates'][0],
            data['dates'][int(len(data['dates']) / 3)],
            data['dates'][int(2 * len(data['dates']) / 3)],
            data['dates'][-1]
        ])

        axis[i, 1].set_xticks([
            data2['dates'][0],
            data2['dates'][int(len(data2['dates']) / 3)],
            data2['dates'][int(2 * len(data2['dates']) / 3)],
            data2['dates'][-1]
        ])
        axis[i, 1].set_xticklabels([
            data2['dates'][0],
            data2['dates'][int(len(data2['dates']) / 3)],
            data2['dates'][int(2 * len(data2['dates']) / 3)],
            data2['dates'][-1]
        ])

    plt.show()
