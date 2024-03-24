from functions import *

filename2 = 'data/doge.csv'
filename = 'data/btc.csv'

data = get_data(filename)
data2 = get_data(filename2)

calculate_macd(data)
calculate_macd(data2)

data_buy_signals, data_sell_signals = generate_signals(data['macd_line'], data['signal_line'])
data2_buy_signals, data2_sell_signals = generate_signals(data2['macd_line'], data2['signal_line'])
print(data_buy_signals, data_sell_signals)
print(data2_buy_signals, data2_sell_signals)

simulate(data, data_buy_signals, data_sell_signals)
simulate(data2, data2_buy_signals, data2_sell_signals)

plot_openings(data, True, data_buy_signals, data_sell_signals)
plot_openings(data2, True, data2_buy_signals, data2_sell_signals)

plot_macd(data)
plot_macd(data2)

plot_simulation(data)
plot_simulation(data2)

simulation_statistics(data, filename)
simulation_statistics(data2, filename2)

plot_data(data, data2, data_buy_signals, data_sell_signals, data2_buy_signals, data2_sell_signals)
