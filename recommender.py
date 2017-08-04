from math import sqrt
import numpy as np
import pickle
import pandas as pd

# Returns the Pearson correlation coefficient for item1 and item2.
def pear(products,item1,item2):
    # Get the list similar items
    sim = {}
    for item in products[item1]:
        if item in products[item2]: sim[item] = 1
    
    # Find the number of elements
    n = len(sim)

    # if they are no ratings in common, return 0
    if n == 0: return 0
    
    # Add up all the ratings
    sum1 = sum([products[item1][user] for user in sim])
    sum2 = sum([products[item2][user] for user in sim])

    # Sum up the squares
    sum1Sq = sum([pow(products[item1][user],2) for user in sim])
    sum2Sq = sum([pow(products[item2][user],2) for user in sim])

    # Sum up the products
    pSum = sum([products[item1][user] * products[item2][user] for user in sim])

    # Calculate Pearson coefficient 
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1,2) / n) * (sum2Sq - pow(sum2,2) / n))
    if den == 0: return 0
    r = num / den
    return r

# Returns the best matches for a person from the products dictionary based on similarity coefficient.
# Number of results and similarity function are optional params.
def topMatches(products,person,n = 20,similarity = pear):
    sim = [(similarity(products,person,other),other) for other in products if other != person]

    # Sort the list so the highest scores appear at the top
    sim.sort( )
    sim.reverse( )
    
    return sim[0:n]

# Return a dictionary of customers where each customer contains the product and the ratings given.
def loadAmazonItems():
    # Get Amazon products
    df = pd.read_csv('C:/Users/Michael/Desktop/clothing.csv')
    df = df.rename(columns={'product/productId': 'pid', 'product/title': 'title', 'product/price': 'price', 
                            'review/userId': 'uid', 'review/profileName': 'profileName', 'review/helpfulness': 'helpfulness', 
                            'review/score': 'rating', 'review/time': 'time', 'review/summary': 'summary', 'review/text': 'text'})
    
    prefs = {}
    rData = list(zip(df.profileName,df.title,df.rating,df.time))
    for user, item, rating, ts in rData:
        prefs.setdefault(user, {})
        prefs[user][item] = float(rating)
    return prefs

# Get recommendations based on similar users' preferences
def getRecommendations(products,product,similarity=pear):
    totals = {}
    simSums = {}
    for other in products:
        # don't compare product that person has seen
        if other == product: continue
        sim = similarity(products,product,other)

        # ignore scores of zero or lower
        if sim <= 0: continue
        for user in products[other]:

            # only score products I haven't seen yet
            if user not in products[product] or products[product][user] == 0:
                # Similarity * Score
                totals.setdefault(user,0)
                totals[user] += products[other][user] * sim
                # Sum of similarities
                simSums.setdefault(user,0)
                simSums[user] += sim

    # Create the normalized list
    rankings=[(total/simSums[user],user) for user,total in totals.items( )]

    # Return the sorted list
    rankings.sort( )
    rankings.reverse( )
    return rankings

def calculateSimilarItems(products,n = 10):
    # Create a dictionary of items showing which other items they
    # are most similar to.
    result = {}
    c = 0
    for item in products:
        # Status updates for large datasets
        c += 1
        if c % 100 == 0: print ("%d / %d" % (c,len(products)))
        # Find the most similar items to this one
        scores = topMatches(products,item,n = n,similarity = pear)
        result[item] = scores
    return result

# Get recommendations based on similar items
def getRecommendedItems(products,itemMatch,user):
    userRatings = products[user]
    scores = {}
    totalSim = {}
    rankings = []
    
    # Loop over each user and obtain items rated
    for (item,rating) in userRatings.items( ):
        # Loop over items similar to this one
        for (similarity,item2) in itemMatch[item]:
            # Ignore if this user has already rated this item
            if item2 in userRatings: continue

            # Weighted sum of rating times similarity
            scores.setdefault(item2,0)
            scores[item2] += similarity * rating
            
            # Take the sum of similarities for that item
            totalSim.setdefault(item2,0)
            totalSim[item2] += similarity
            
    # Divide each weighted score by the total sum of similaries to get an average
    for item, score in scores.items():
        # Ignore ratings of 0 to avoid divide by zero
        if totalSim[item] == 0: continue
        rankings.append((score / totalSim[item],item))
        
    #rankings=[(score/totalSim[item],item) for item,score in scores.items( )]
    
    # Return the rankings from highest to lowest
    rankings.sort( )
    rankings.reverse( )
    return rankings

prefs = loadAmazonItems()
itemsim = calculateSimilarItems(products)

print(prefs['Julia'])
print(getRecommendations(prefs, 'Julia')[0:20])
print(getRecommendedItems(prefs, itemsim, 'Julia')[0:20])