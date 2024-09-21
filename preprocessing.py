import pandas as pd
import random


#data = pd.read_csv('world-cities.csv')
#df = pd.read_csv('world-countries.csv')
# print(data)

# Add a new column with random values
# data["avg temp"] = [random.randint(75, 150) for _ in range(len(data))]

# df.drop('avg cost per day', axis=1, inplace=True)

# df.drop('keyword', axis=1, inplace=True)



#a = data.groupby('country')['avg cost per day'].mean().astype(int)
#df = df.set_index('country').join(a).reset_index()
#df['avg cost per day'] = df['avg cost per day'].fillna(0).astype(int)

def fun(row):
    set1 = ['food', 'history', 'culture', 'beach', 'mountain', 'plain']
    set_weather1 = ['cold', 'mix']
    set_weather2 = ['hot', 'cold', 'mix']
    set_weather3 = ['hot', 'mix']
    set2 = ['food', 'history', 'culture', 'beach', 'mountain', 'plain', 'wildlife', 'forest', 'desert']
    set3 = ['food', 'history', 'culture', 'beach', 'plain', 'desert', 'wildlife']
    set4 = ['food', 'history', 'culture', 'mountain', 'forest', 'beach', 'plain', 'wildlife']

    if 'europe' in row['keywords']:
        row['keywords'] += ' ' + set_weather1[random.randint(0, 1)]
        for i in range(random.randint(2, 4)):
            if set1[i] not in row['keywords']:
                row['keywords'] += ' ' + set1[i]
        return row

    elif 'asia' in row['keywords']:
        row['keywords'] += ' ' + set_weather2[random.randint(0, 2)]
        for i in range(random.randint(2, 5)):
            if set2[i] not in row['keywords']:
                row['keywords'] += ' ' + set2[i]
        return row

    elif 'africa' in row['keywords']:
        row['keywords'] += ' ' + set_weather3[random.randint(0, 1)]
        for i in range(random.randint(2, 4)):
            if set3[i] not in row['keywords']:
                row['keywords'] += ' ' + set3[i]
        return row

    elif 'northamerica' in row['keywords']:
        row['keywords'] += ' ' + set_weather3[random.randint(0, 1)]
        for i in range(random.randint(2, 5)):
            if set4[i] not in row['keywords']:
                row['keywords'] += ' ' + set4[i]
        return row

    elif 'southamerica' in row['keywords']:
        for i in range(random.randint(2, 4)):
            if set4[i] not in row['keywords']:
                row['keywords'] += ' ' + set4[i]
        return row
