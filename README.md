# Recommender System Project
Collaborative Filtering for Recommender Systems using Amazon dataset

## Introduction
Using concepts from the book, [Collective Intelligence](http://shop.oreilly.com/product/9780596529321.do) and the Amazon Clothing and Accessories dataset provided by [Stanford University](https://snap.stanford.edu/data/web-Amazon.html), I applied what I have learned so far to make a recommender system in Python that touches on **user-based** and **item-based filtering**.

## Preprocessing
The first thing done was to organize the data to make it more readable and easier to manipulate. The text file was parsed and then converted to a CSV format. The CSV file was then used to make a product dictionary which contained a user dictionary that contained all the ratings from the users for that specific product. To avoid recomputation of **19,194 items**, the product dictionary was saved as a pickle file for later use. 

An example of a product dictionary entry is shown below:
```
[...
("adidas Men's 3-Stripe Fleece Pant,Black/White,X-Large", {'J. Williams': 5.0, 'E. Hansen "Fitness Guy"': 4.0})
...]
```
## Finding Similarities
I used the **Pearson Correlation Coefficient** algorithm to determine how similar two items are with each other. The algorithm returns a number from +1 to -1. 

Here is a test example I used to determine the similarity of two Khaki items:
```
In [67]: pear(products, 'Amazon.com: Dockers Original Khaki Classic Fit - Pleated, W38 L32, Charcoal Heather: Clothing', 
                        'Amazon.com: Dockers Original Khaki Classic Fit - Pleated, W38 L34, Charcoal Heather: Clothing')
Out[67]: 1.0
```
After using the algorithm, items were given a similarity cofficient of either **1.0** or **0.0**, which meant they were similar or not similar.
In regards to the items returning a 1.0, however, Python rounded up the coefficient to 1.0 as it was truely around 0.999...

## Getting Recommendations
With the Pearson algorithm as the basis for obtaining our recommendations, I applied the user-based filtering first and afterwards item-based filtering in order to compare the two. **User-based filtering** finds similaries between an item that two users have in common and recommends items that one user has that the other doesn't. While, **item-based filtering** finds similar items to the one a user has and recommendeds those items.  

**Example of the Julia's product ratings:**
```
In [75]: prefs['Julia']
Out[75]: {'Amazon.com: American Apparel Spandex Jersey Yoga Pant (8300), Size: Large, Color: Heather Grey: Clothing': 4.0,
          'Amazon.com: Eagle Creek Travel Gear Pack-It Medium/Large Compression Sac Set: Clothing': 1.0,
          'Amazon.com: Exquisite Form Women&#39;s Front Close Cotton Posture Bra #5100531: Clothing': 5.0,
          'Amazon.com: Glamorise Sport Soft Cup Superior Support Bra G-1006: Clothing': 2.0,
          'Amazon.com: Hufflepuff House Scarf: Clothing': 5.0,
          'Amazon.com: JanSport Classics Series Superbreak Backpack (Alien Green): Sports &amp; Outdoors': 5.0,
          'Amazon.com: Ladies&#39; Jersey Tee Shirt: Clothing': 2.0,
          'Amazon.com: OnGossamer Women&#39;s Mesh Bump It Up Bra: Clothing': 4.0,
          'Amazon.com: Secret Wishes Maid Costume: Clothing': 2.0,
          'Amazon.com: Speedo Women&#39;s Lycra Tribal Etching Geoback Swim Suit, Blue, Size 38: Clothing': 5.0}
```

**User-based filtering based on Julia's product ratings:**
```
In [76]: getRecommendations(prefs, 'Julia')[0:20]
Out[76]: [(5.0, 'Vintage Retro Mirror Aviator Sunglass w/ free Pouch'),
          (5.0, 'High Sierra Water Bottle Sport Duffel'),
          (5.0, 'HARVEYS Seatbelt Zip Wallet'),
          (5.0, "Girl High Seas Buccaneer Toddler Costume - Kid's Costumes"),
          (5.0, 'Amazon.com: Women&#39;s Soft Lightweight Travel Money Belt - White: Clothing'),
          (5.0, 'Amazon.com: SPANX Power Panties Shapewear: Clothing'),
          (5.0, 'Amazon.com: JanSport Elefunk Metro Messenger Bag (Bubblegum): Clothing'),
          (5.0, 'Amazon.com: JanSport Elefunk Metro Messenger Bag (Blue Jean): Clothing'),
          (5.0, 'Amazon.com: Enell High Impact Sports Bra: Clothing'),
          (5.0, 'Amazon.com: Carhartt Men&#39;s Duck Coverall Quilted Lined: Clothing'),
          (5.0, 'Amazon.com: : Clothing'),
          (4.0, 'Amazon.com: V-Neck Katahdin Tek Pullover XXX-Large Black: Clothing'),
          (4.0, 'Amazon.com: V-Neck Katahdin Tek Pullover XX-Large Navy: Clothing'), 
         ...]
```

**Item-based filtering based on Julia's product ratings:**
```
In [78]: getRecommendedItems(prefs, itemsim, 'Julia')[0:20]
Out[78]: [(5.0, 'green sprouts 10 Pack Waterproof Absorbent Terry Bibs'),
          (5.0, 'ZANheadgear Desert Nylon Balaclava (Camouflage)'),
          (5.0, 'Superman Dress Up Set'),
          (5.0, 'Rothco Canvas Map Case'),
          (5.0, 'Robin Deluxe Muscle Chest Child Costume'),
          (5.0, 'Rear View Sunglasses'),
          (5.0, "NEON 80's style PARTY SUNGLASSES with dark lens (12 pack)"),
          (5.0, 'Men\'s HeatGear&#174; Compression 7" Shorts Bottoms by Under Armour'),
          (5.0, 'High Sierra Water Bottle Sport Duffel'),
          (5.0, 'Hannah Montana Tote Bag with Wig and Assorted Accessories'),
          (5.0, 'Gold Eyeglass Holder Fashion Chain By Apex Medical'),
          (5.0, "Child's Heirloom Elephant Costume (Size:X-small 4-6)"),
          (5.0, 'Child Pink Supergirl Costume'),
         ...]
```

## User-based vs. Item-based
It is known that item-based filtering is significantly faster than user-based filtering when dealing with large datasets.

When testing the execution time of both functions, the **user-based filtering approach took 0.1 seconds longer**. If we were to use this approach for all of Amazon's products then it would increase overhead. 

Whereas, **item-based filtering approach** first required an additional function to find all the similar items, which was very **time-consuming** considering we had to go through 19,000+ items. However, the approach returned the recommendations **almost immediately**, which shows it to be more efficient in dealing with large datasets.

## What to Improve
* Use a different similarity measure, like Jaccard or Cosine Similarity, and compare measures against each other.
* Determine whether a product is for Men, Women, or Children to give a more accurate recommendation.
  (eg. 'Julia' purchased a costume and she is recommended children's costumes)

## References
Segaran, Toby. “Chapter 2: Making Recommendations.” Programming Collective Intelligence: Building Smart Web 2.0 Applications, O'Reilly, 2007.

“Web Data: Amazon Reviews.” SNAP: Web Data: Amazon Reviews, Stanford University, snap.stanford.edu/data/web-Amazon.html.
