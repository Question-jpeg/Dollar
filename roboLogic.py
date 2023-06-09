import configparser

config = configparser.ConfigParser(inline_comment_prefixes="#")
config.read('config.ini') 
COM_TIN_FACTOR = 1 - config.getfloat('commission_info', 'COM_TIN') / 100

def roboStasLogic(prices, rubles, dollars, percentStep, buyConfig, saleConfig, buy_fix):
    buyConfig.sort()
    saleConfig.sort()
    originalBuyConfig = [] + buyConfig
    originalSaleConfig = [] + saleConfig

    previous = 100
    for index, percent in enumerate(buyConfig):
        buyConfig[index] = percent / previous
        previous = previous - percent
    previous = 100
    for index, percent in enumerate(saleConfig):
        saleConfig[index] = percent / previous
        previous = previous - percent

    lastBuyConfigIndex = len(buyConfig)-1
    lastSaleConfigIndex = len(saleConfig)-1

    startDiggingCourse = 0
    startSellingCourse = 999_999_999
    previous = prices[0]
    operationStack = {'buy': 0, 'sell': 0}
    operationsTrace = []
    commission = 0
    count = 0

    for index, current in enumerate(prices):
        difference = (current - previous) / previous * 100
        if abs(difference) >= percentStep:
            if difference < 0:
                if (True if not buy_fix else current < (startSellingCourse * (1 - percentStep / 100))):
                    operationStack['sell'] = 0

                    if operationStack['buy'] == 0:
                        startDiggingCourse = current

                    if operationStack['buy'] > lastBuyConfigIndex:
                        operationsTrace.append(
                            {"operation": 'wait', 'course': current, 'index': index})
                        continue

                    multiplier = buyConfig[operationStack['buy']]
                    sumBuying = rubles * multiplier
                    rubles -= sumBuying
                    dollars += (sumBuying * COM_TIN_FACTOR) / current
                    previous = current
                    commission += sumBuying * (1 - COM_TIN_FACTOR)
                    operationsTrace.append(
                        {"operation": 'buy', 'course': current, 'index': index, 'dollars': dollars, "rubles": rubles, 'size': originalBuyConfig[operationStack['buy']]})

                    count += 1
                    operationStack['buy'] += 1

            elif True if not buy_fix else current > (startDiggingCourse * (1 + percentStep / 100)):
                operationStack['buy'] = 0

                if operationStack['sell'] == 0:
                    startSellingCourse = current

                if operationStack['sell'] > lastSaleConfigIndex:
                    operationsTrace.append(
                        {"operation": 'wait', 'course': current, 'index': index})
                    continue

                multiplier = saleConfig[operationStack['sell']]
                sumSelling = dollars * multiplier
                dollars -= sumSelling
                rubles += sumSelling * COM_TIN_FACTOR * current
                previous = current
                commission += sumSelling * (1 - COM_TIN_FACTOR) * current
                operationsTrace.append(
                    {"operation": 'sell', 'course': current, 'index': index, 'dollars': dollars, "rubles": rubles, 'size': originalSaleConfig[operationStack['sell']]})
                
                count += 1
                operationStack['sell'] += 1

    return {'rubles': rubles, 'dollars': dollars, 'count': count, 'operationsTrace': operationsTrace, 'commission': commission}

def roboTraceLogic(prices, rubles, dollars, percentStep, buyConfig, first_buy_fix):
    buyConfig.sort()
    previous = 100
    for index, percent in enumerate(buyConfig):
        buyConfig[index] = percent / previous
        previous = previous - percent

    buyConfigLastIndex = len(buyConfig)-1
    previous = prices[0]
    buyOperationsStack = []
    buyMultiple = 0
    operationsTrace = []
    commission = 0
    count = 0    

    if first_buy_fix:
        buyOperationsStack.append({ 'course': previous, 'quantity': dollars })

    for index, current in enumerate(prices):
        difference = (current - previous) / previous * 100
        if abs(difference) >= percentStep:
            if difference < 0:
                if buyMultiple > buyConfigLastIndex:
                    operationsTrace.append(
                        {"operation": 'wait', 'course': current, 'index': index})
                    continue

                multiplier = buyConfig[buyMultiple]
                sumBuying = rubles * multiplier
                sumBuyingDollars = (sumBuying * COM_TIN_FACTOR) / current                

                rubles -= sumBuying
                dollars += sumBuyingDollars

                commission += sumBuying * (1 - COM_TIN_FACTOR)
                
                buyOperationsStack.append({ 'course': current, 'quantity': sumBuyingDollars })

                previous = current
                operationsTrace.append(
                    {"operation": 'buy', 'course': current, 'index': index, 'dollars': dollars, "rubles": rubles, 'size': sumBuying })

                buyMultiple += 1
                count += 1                
            else:
                buyMultiple = 0
                if len(buyOperationsStack) == 0:
                    operationsTrace.append(
                        {"operation": 'wait', 'course': current, 'index': index})
                    continue

                sumSelling = buyOperationsStack.pop()['quantity']
                dollars -= sumSelling
                rubles += sumSelling * COM_TIN_FACTOR * current
                previous = current
                commission += sumSelling * (1 - COM_TIN_FACTOR) * current
                operationsTrace.append(
                    {"operation": 'sell', 'course': current, 'index': index, 'dollars': dollars, "rubles": rubles, 'size': sumSelling })
                
                count += 1

    return {'rubles': rubles, 'dollars': dollars, 'count': count, 'operationsTrace': operationsTrace, 'commission': commission}                

