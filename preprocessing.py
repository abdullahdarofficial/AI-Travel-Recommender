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

def fun2(row):
    if 'mix' in row['keywords']:
        row['keywords'] = row['keywords'].replace('mix', '')
        row['climate'] = 'mix'
        row['keywords'] = row['keywords'].replace('  ', ' ')
        return row
    elif 'hot' in row['keywords']:
        row['keywords'] = row['keywords'].replace('hot', '')
        row['climate'] = 'hot'
        row['keywords'] = row['keywords'].replace('  ', ' ')
        return row
    elif 'cold' in row['keywords']:
        row['keywords'] = row['keywords'].replace('cold', '')
        row['climate'] = 'cold'
        row['keywords'] = row['keywords'].replace('  ', ' ')
        return row

def convert(row):
    row['avg cost per day'] = int(row['avg cost per day'])
    # if row['country'] == 'Sri Lanka':
    #     row['avg cost per day'] = int(data[data['country'] == 'Sri Lanka'].groupby('country')['avg cost per day'].mean().astype(int))
    return row

# df = df.apply(convert, axis=1)

# print(df)



#popularity = pd.DataFrame()

#popularity['Country'] = df['country']

#popularity = pd.read_csv('world-popularity.csv')

popular = ['France','Spain','United States','China','Italy','Mexico','Turkey','Germany','United Kingdom','Thailand','Japan','Canada',
'Russia','Malaysia','Greece','Portugal','Austria','Australia','Netherlands','Switzerland','Singapore','South Korea','Hong Kong',
'Czech Republic','Poland', 'Sweden', 'Denmark', 'Egypt', 'Croatia','Norway', 'Indonesia', 'Ireland', 'Romania','Belgium','Vietnam',
'Philippines','Argentina', 'Finland', 'Peru','United Arab Emirates','Morocco','New Zealand','Colombia','Bulgaria','Saudi Arabia',
'Hungary', 'Tunisia', 'Dominican Republic','Qatar', 'Chile','Slovakia','Oman','India','South Africa','Brazil','Cyprus','Nigeria',
'Maldives', 'Pakistan', 'Uganda', 'Madagascar', 'Malawi', 'Sri Lanka']
