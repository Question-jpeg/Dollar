from dollarGraphMaker import createModel, createGraph

initialCourse = float(input('Начальный курс: '))
endCourse = float(input("Конечный курс: "))
agreement = ''

while agreement != 'y':

    list_data = createModel(initialCourse, endCourse)
    print(len(list_data))

    agreement = input("Создать файл? (y/n): ").lower()

    if agreement == 'y':
        createGraph(list_data)


