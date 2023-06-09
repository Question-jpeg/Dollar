from roboLogic import roboStasLogic, roboTraceLogic

def roboStas(prices, rubles, dollars, percentStep, buyConfig, saleConfig, buyFix):
    buyConfig = buyConfig + []
    saleConfig = saleConfig + []

    data = roboStasLogic(prices, rubles, dollars, percentStep, buyConfig, saleConfig, buyFix)

    return {"rubles": data['rubles'], "dollars": data['dollars'], 'count': data['count'], 'commission': data['commission']}

def roboTrace(prices, rubles, dollars, buysFactor, percentStep, first_buy_fix):
    buyConfig = [100 / buysFactor for buy in range(buysFactor)]

    data = roboTraceLogic(prices, rubles, dollars, percentStep, buyConfig, first_buy_fix)

    return {"rubles": data['rubles'], "dollars": data['dollars'], 'count': data['count'], 'commission': data['commission']}
