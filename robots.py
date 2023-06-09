from roboLogic import roboStasLogic, roboTraceLogic

def roboIgor(prices, rubles, dollars):

    config = {'buy': [], 'sell': []}

    choice = input("Правила покупки = правила продажи?: ")
    for i in range(2 if choice == 'n' else 1):
        if i == 0:
            print('Введите правила покупки (процентСпада=процентОтСуммыНаСчету)')
        else:
            print('Введите правила продажи (процентПовышения=процентОтСуммыНаСчету)')

        strConfigParameter = input()
        while strConfigParameter != 'stop':
            [percent, percentOfSum] = strConfigParameter.split('=')
            [percent, percentOfSum] = [float(percent), float(percentOfSum)]

            if i == 0:
                config["buy"].append([percent, percentOfSum])
            if i == 1 or choice == 'y':
                config["sell"].append([percent, percentOfSum])

            strConfigParameter = input()

    config['buy'] = sorted(
        config['buy'], key=lambda array: array[0], reverse=True)
    config['sell'] = sorted(
        config['sell'], key=lambda array: array[0], reverse=True)

    previous = prices[0]
    operationsTrace = []

    for index, current in enumerate(prices):
        difference = (current - previous) / previous * 100
        if difference < 0:
            difference = -difference
            for configuration in config['buy']:
                if (difference >= configuration[0]):
                    sumBuying = rubles * configuration[1] / 100
                    rubles -= sumBuying
                    dollars += sumBuying / current
                    previous = current
                    operationsTrace.append(
                        {"operation": 'buy', 'course': current, 'index': index})
                    break

        else:
            for configuration in config['sell']:
                if (difference >= configuration[0]):
                    sumSelling = dollars * configuration[1] / 100
                    dollars -= sumSelling
                    rubles += sumSelling * current
                    previous = current
                    operationsTrace.append(
                        {"operation": 'sell', 'course': current, 'index': index})
                    break

    return {"rubles": rubles, "dollars": dollars, "operationsTrace": operationsTrace}


def roboStas(prices, rubles, dollars, percentStep, buy_fix=True):
    buyConfig = []
    saleConfig = []
    for i in range(2):
        ok = False
        while not ok:
            if i == 0:
                print("Введите распределение на ПОКУПКУ (курс падает) (ПроцентОтНачальнойСуммы):")
            else:
                print("Введите распределение на ПРОДАЖУ (курс растёт) (ПроцентОтНачальнойСуммы):")
            ok = True
            total = 0
            while total < 100:
                inputPercent = float(input())
                if i == 0:
                    buyConfig.append(inputPercent)
                else:
                    saleConfig.append(inputPercent)
                total += inputPercent
                if total > 100:
                    print('Общий процент больше 100. Попробуйте ещё раз')
                    if i == 0:
                        buyConfig.clear()
                    else:
                        saleConfig.clear()
                    ok = False
                    break

    originalBuyConfig = [] + buyConfig
    data = roboStasLogic(prices, rubles, dollars, percentStep, buyConfig, saleConfig, buy_fix)

    return {"rubles": data['rubles'], "dollars": data['dollars'], "operationsTrace": data['operationsTrace'], 'count': data['count'], 'commission': data['commission'], 'distribution': originalBuyConfig}

def roboTrace(prices, rubles, dollars, percentStep, first_buy_fix):
    buyConfig = []
    ok = False
    while not ok:        
        print("Введите распределение на ПОКУПКУ (курс падает) (ПроцентОтНачальнойСуммы):")
        ok = True
        total = 0
        while total < 100:
            inputPercent = float(input())
            buyConfig.append(inputPercent)
            total += inputPercent
            if total > 100:
                print('Общий процент больше 100. Попробуйте ещё раз')
                buyConfig.clear()
                ok = False
                break

    originalBuyConfig = [] + buyConfig
    data = roboTraceLogic(prices, rubles, dollars, percentStep, buyConfig, first_buy_fix)
    
    return {"rubles": data['rubles'], "dollars": data['dollars'], "operationsTrace": data['operationsTrace'], 'count': data['count'], 'commission': data['commission'], 'distribution': originalBuyConfig}
    

# { "" }

# data = roboTrace([100, 99, 98, 99, 98, 99, 100, 99, 98,
#                 97, 96, 97, 98, 99, 100], 1000000, 20000)
# print(data)
