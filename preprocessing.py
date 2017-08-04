import csv
import gzip
import json
import simplejson
import pandas as pd
import pickle

# Parse txt file to separate each entry
def parse(filename):
    f = gzip.open(filename, 'rb')
    entry = {}
    for l in f:
        l = l.strip()
        colonPos = l.find(b':')
        if colonPos == -1:
            yield entry
            entry = {}
            continue
        eName = l[:colonPos]
        rest = l[colonPos+2:]
        entry[eName] = rest
    yield entry

# Convert txt file containing Clothing & Accessories dataset to JSON format
g = open("C:/Users/Michael/Desktop/clothing.json", "w")

data = []
count = 0
for e in parse('C:/Users/Michael/Desktop/Clothing_&_Accessories.txt.gz'):
    obj = json.loads(simplejson.dumps(e))
    data.append(obj)
    #count += 1
    #if count == 2: break
json.dump(data,g)
g.close()

# Convert JSON to CSV and rename the columns to make it more accessible
df = pd.read_json('C:/Users/Michael/Desktop/clothing.json')
df.to_csv('C:/Users/Michael/Desktop/clothing.csv')

df = pd.read_csv('C:/Users/Michael/Desktop/clothing.csv')
df = df.rename(columns={'product/productId': 'pid', 'product/title': 'title', 'product/price': 'price', 'review/userId': 'uid',
                       'review/profileName': 'profileName', 'review/helpfulness': 'helpfulness', 'review/score': 'rating', 'review/time': 'time',
                       'review/summary': 'summary', 'review/text': 'text'})

# Function that takes the dataframe of clothing.csv and creates a products dictionary that contains the customer and their ratings
def transformPrefs(df):
    result = {}
    for item in df.title:
        result.setdefault(item, {})
    count = 0
    for key in result.keys():
        print(key)
        print(count, len(result.keys()))
        count += 1

        person = df[df.title == key].profileName
        for p in person.unique():
            ratings = df[df.profileName == p].rating
            for r in ratings.unique():
            #avgRating = ratings.mean()
                result[key][p] = r
    return result

productDict = transformPrefs(df)

# Write the dictionary to a pickle file to avoid recomputation
output = open('C:/Users/Michael/Desktop/productDict.pkl', 'wb')
pickle.dump(productDict, output)
output.close()

