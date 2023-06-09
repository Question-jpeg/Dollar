### AI line  ###
# robotName = ''
# while robotName not in ['stas', 'trace']:
#     robotName = input("Введите название робота (stas/trace): ")
#     if robotName == 'stas':

# elif robotName == 'trace':
#         ws.cell(3, 1, "Количество операций")
#         ws.cell(3, 2, "Глубина закупки")
#         ws.cell(3, 3, "Шаговый процент")
#         ws.cell(3, 4, "Закупка в начале курса")
#         ws.cell(3, 5, "Конечный капитал")
#         ws.cell(3, 6, 'Комиссия')

#         for bFactor in range(1, BUYS_FACTOR+1):
#             for percentStep in range(PSR[0], PSR[1] + PSR[2], PSR[2]):
#                 percentStep /= 10
#                 for first_buy_fix in [True, False]:

#                     data = roboTrace(prices, RUBLES, DOLLARS, bFactor, percentStep, first_buy_fix)
#                     resultRubles = data['dollars'] * prices[-1] + data['rubles']
#                     count = data['count']
#                     commission = round(data['commission'], 2)

#                     ws.cell(row, 1, count)
#                     ws.cell(row, 2, bFactor)
#                     ws.cell(row, 3, percentStep)
#                     ws.cell(row, 4, first_buy_fix)
#                     ws.cell(row, 5, resultRubles)
#                     ws.cell(row, 6, commission)

#                     row += 1

### dollar line 19 ###
# remove comment