# array = ['model100_70_4949_stasTest']

data = {}

data[1] = data.get(1, {})
data[1][2] = data[1].get(2, {})
data[1][2]['test'] = 'success'

print(data)