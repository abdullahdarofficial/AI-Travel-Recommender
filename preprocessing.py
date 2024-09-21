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

def calculate_popularity(country):
    if country in popular:
        return (100 - popular.index(country)) - random.uniform(0.000167, 0.132864)
    else:
        return random.uniform(18.23422, 37.05334)

i = 0

def calculate_visitors(country):
    global i
    if country == 'Mexico':
        print(i)
        i+=1
        return int(51128000)
    if country == 'United States':
        print(i)
        i+=1
        return int(45037000)
    if country == 'Thailand':
        print(i)
        i+=1
        return int(39916000)
    if country == 'Italy':
        print(i)
        i+=1
        return int(38419000)
    if country == 'Pakistan':
        print(i)
        i+=1
        return int(966_000)
    if country == 'Spain':
        print(i)
        i+=1
        return int(36410000)
    if country == 'Canada':
        print(i)
        i+=1
        return int(32430000)
    if country == 'Hungary':
        print(i)
        i+=1
        return int(31641000)
    if country == 'China':
        print(i)
        i+=1
        return int(30402000)
    if country == 'Saudi Arabia':
        print(i)
        i+=1
        return int(20292000)
    if country == 'India':
        print(i)
        i+=1
        return int(17914000)
    if country == 'Turkey':
        print(i)
        i+=1
        return int(15_971_000)
    if country == 'Denmark':

        print(i)
        i+=1
        return int(15_000_000)
    if country == 'Greece':
        print(i)
        i+=1
        return int(14_710_000)
    if country == 'Austria':
        print(i)
        i+=1
        return int(12_730_000)
    if country == 'Germany':
        print(i)
        i+=1
        return int(11_690_000)
    if country == 'United Arab Emirates':
        print(i)
        i+=1
        return int(11_480_000)
    if country == 'South Korea':
        print(i)
        i+=1
        return int(17_500_000)
    if country == 'Vietnam':
        print(i)
        i+=1
        return int(18_000_000)
    if country == 'Netherlands':
        print(i)
        i+=1
        return int(20_100_000)
    if country == 'Japan':
        print(i)
        i+=1
        return int(32_300_000)
    if country == 'Australia':
        print(i)
        i+=1
        return int(9_300_000)
    if country == 'Brazil':
        print(i)
        i+=1
        return int(6_600_000)
    if country == 'Egypt':
        print(i)
        i+=1
        return int(11_300_000)
    if country == 'Malaysia':
        print(i)
        i+=1
        return int(26_100_000)
    if country == 'New Zealand':
        print(i)
        i+=1
        return int(4_500_000)
    if country == 'Portugal':
        print(i)
        i+=1
        return int(12_800_000)
    if country == 'Russia':
        print(i)
        i+=1
        return int(24_600_000)
    if country == 'Singapore':
        print(i)
        i+=1
        return int(14_400_000)
    if country == 'South Africa':
        print(i)
        i+=1
        return int(10_200_000)
    if country == 'Sweden':
        print(i)
        i+=1
        return int(7_300_000)
    if country == 'Argentina':
        print(i)
        i+=1
        return int(6_800_000)
    if country == 'Chile':
        print(i)
        i+=1
        return int(5_700_000)
    if country == 'Colombia':
        print(i)
        i+=1
        return int(4_900_000)
    if country == 'Indonesia':
        print(i)
        i+=1
        return int(16_100_000)
    if country == 'Ireland':
        print(i)
        i+=1
        return int(10_800_000)
    if country == 'Morocco':
        print(i)
        i+=1
        return int(12_300_000)
    if country == 'Nepal':
        print(i)
        i+=1
        return int(601_360)
    if country == 'Switzerland':
        print(i)
        i+=1
        return int(9_500_000)
    if country == 'Taiwan':
        print(i)
        i+=1
        return int(11_600_000)
    if country == 'Ukraine':
        print(i)
        i+=1
        return int(14_700_000)
    if country == 'Bangladesh':
        print(i)
        i+=1
        return int(3_000_000)
    if country == 'France':
        print(i)
        i+=1
        return int(117_109_000)
    if country == 'Poland':
        print(i)
        i+=1
        return int(88_515_000)
    else:
        return random.randrange(100_000, 2_000_000)

#popularity['Popularity Index'] = popularity['country'].apply(calculate_popularity)

#popularity['Avg Visitors'] = popularity['Country'].apply(calculate_visitors)

#popularity.drop_duplicates(inplace=True)

#print(popularity)

# while True:
#     print('Enter the country: ')
#     country = input()
#     if country == 'exit':
#         break
#     else:
#         print(popularity[popularity['Country'].str.lower() == country.lower()])

# popularity.to_csv('world-popularity.csv', index=False)
#df.to_csv('world-countries.csv', index=False)

# a = pd.read_csv('world-popularity.csv')
# b = pd.read_csv('world-countries.csv')

# f=0
# for i in range(len(b)):
#     for j in range(len(a)):
#         if b['Country'][i] == a['Country'][j]:
#             f+=1
#             print(f,b['Country'][i], a['Country'][j], 'at index', i, j)



# print(b['Country'].drop_duplicates().count())



#print(a)
#print(b)

# countries = pd.read_csv('world-countries.csv')
# popularity = pd.read_csv('world-popularity.csv')

# #users = pd.read_csv('users-rating.csv')
# print(countries[countries['keywords'].str.contains('plains')])
# countries['keywords'] = countries['keywords'].str.replace(r'plains', 'plain')
# print(countries[countries['keywords'].str.contains('plains')])

# countries.to_csv('world-countries.csv', index=False)

import geocoder
import time

cites = pd.read_csv('world-cities.csv')

x = []
for city,country in cites[['name', 'country']].values:
    print(city, country)
    x.append(geocoder.osm(city+", "+country).latlng)


#x = [geocoder.osm(city+", "+country).latlng for city,country in cites[['name', 'country']].values]
print('x done')

cites['lat'] = [i[0] for i in x]
cites['lng'] = [i[1] for i in x]

print(cites)
input()

cites.to_csv('world-cities.csv', index=False)