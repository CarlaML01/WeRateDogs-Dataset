#!/usr/bin/env python
# coding: utf-8

# # WeRateDogs Twitter Project: Wrangling and Analyze Data
# *By Carla Mota Leal*

# ### Importing the necessary packages:

# In[1]:


import tweepy
from tweepy import OAuthHandler
import pandas as pd
import numpy as np
import requests
import json
from timeit import default_timer as timer


# ## Data Gathering
# In the cell below, I will gather **all** three pieces of data for this project and load them in this notebook. 
# **Note:** the methods required to gather each data are different.
# 1. Directly downloading the WeRateDogs Twitter archive data (twitter_archive_enhanced.csv)

# In[2]:


#First, I downloaded the Twitter archive from Udacity and will read it into a dataframe.
twit_arc_raw = pd.read_csv('twitter-archive-enhanced.csv')


# 2. Using the Requests library to download the tweet image prediction (image_predictions.tsv)

# > 'image_predictions.tsv' is hosted on Udacity's server and will be downloaded programmatically using the Requests library. I will use this URL :'https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv'

# In[3]:


# Image predictions URL provided by Udacity
url = 'https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv'
response = requests.get(url)

with open (url.split('/')[-1], mode='wb') as file:
    file.write(response.content)


# In[4]:


predict_raw = pd.read_csv('image-predictions.tsv', sep='\t')


# 3. Using the Tweepy library to **query** additional data via the Twitter API (tweet_json.txt)

# > The Twitter archive provided by Udacity does not have all of the desired data, specifically retweet and favorite counts. I will use the Twitter API to read each tweet's JSON data into its own line in a TXT file. Then I will read this file line by line to create a dataframe with retweet and favorite counts. Some of the tweets provided by Udacity may have been deleted, so I will also keep track of this. Note that the consumer_key, consumer_secret, access_token, and access_secret have been deleted here.

# In[5]:


## Install Tweepy if haven't already:
#!pip install tweepy


# In[5]:


# Setting up Twitter API credentials:
consumer_key = 'HIDDEN'
consumer_secret = 'HIDDEN'
access_token = 'HIDDEN'
access_secret = 'HIDDEN'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

tweet_ids = twit_arc_raw.tweet_id.values
len(tweet_ids)

# Query Twitter's API for JSON data for each tweet ID in the Twitter archive
count = 0
fails_dict = {}
start = timer()
# Save each tweet's returned JSON as a new line in a .txt file
with open('tweet_json.txt', 'w') as outfile:
    # This loop will likely take 20-30 minutes to run because of Twitter's rate limit
    for tweet_id in tweet_ids:
        count += 1
        print(str(count) + ": " + str(tweet_id))
        try:
            tweet = api.get_status(tweet_id, tweet_mode='extended')
            print("Success")
            json.dump(tweet._json, outfile)
            outfile.write('\n')
        except tweepy.TweepError as e:
            print("Fail")
            fails_dict[tweet_id] = e
            pass
end = timer()
print(end - start)
print(fails_dict)


# In[6]:


twit_json_raw = pd.read_json('tweet-json.txt', lines=True)


# In[7]:


# Copies for cleaning
twit_arc = twit_arc_raw.copy()
predict = predict_raw.copy()
twit_json = twit_json_raw.copy()


# > Now I have a DataFrame *api_df* containing the tweet ID, retweet count, and favorite count for each tweet.
# > Note that I'll need to replace the placeholders with actual Twitter API credentials.

# ## Assessing Data
# In this section, I will detect and document **eight (9) quality issues and two (3) tidiness issue**. And I will use **both** visual assessment
# programmatic assessement to assess the data.
# 
# **Note:** 
# 
# * I only want original ratings (no retweets) that have images. Though there are 5000+ tweets in the dataset, not all are dog ratings and some are retweets.
# * Assessing and cleaning the entire dataset completely would require a lot of time, and is not necessary to practice and demonstrate my skills in data wrangling. Therefore, the requirements of this project are only to assess and clean at least 8 quality issues and at least 2 tidiness issues in this dataset.
# * The fact that the rating numerators are greater than the denominators does not need to be cleaned. This [unique rating system](http://knowyourmeme.com/memes/theyre-good-dogs-brent) is a big part of the popularity of WeRateDogs.
# * I do not need to gather the tweets beyond August 1st, 2017. I can, but note that I won't be able to gather the image predictions for these tweets since I don't have access to the algorithm used.
# 
# 

# In[8]:


# Now that the data is gathered, I will assess it. 
# First I will perform a visual assessment:

twit_arc 


# In[12]:


twit_arc.info()


# In[13]:


predict 


# In[14]:


predict.info()


# In[15]:


twit_json


# In[16]:


twit_json.info()


# In[9]:


# checking for duplicates 

twit_arc.duplicated().sum()


# In[10]:


predict.duplicated().sum()


# In[11]:


twit_json.id.duplicated().sum()


# In[12]:


# checking for datatype 01 & missing values

twit_arc.info()


# In[44]:


# checking for wrong names

pd.set_option('display.max_rows', 30)
twit_arc.name.value_counts()


# In[13]:


twit_arc.query("name in ['a', 'an', 'the', 'not', 'actually']").name.value_counts()
# there were many names which were clearly wring names ( a, the, an, not ....) 
# I will change those names into "None" 


# In[14]:


# First, converting the rating_numerator and rating_denominator columns to integers using the astype() method:
twit_arc_check = twit_arc['rating_numerator'].astype(int)
twit_arc_check = twit_arc['rating_denominator'].astype(int)


# In[15]:


# checking for the wrong ratings

twit_arc_check = twit_arc.query('rating_denominator != 10')
twit_arc_check = twit_arc_check[['text','rating_numerator', 'rating_denominator']]
twit_arc_check.head()

# Some rows have wrong rating denominator & rating numerator.
# They must be amended manually, based on what's written on "text" column.


# In[16]:


# checking for datatypes 02

predict.info()


# In[35]:


# checking for datatypes 03

twit_json.info()


# ### Quality issues
# 
# *twit_arc* 
# 1. Remove duplicated data in "expanded_urls" column & the rows with null value in the same column
# 2. Remove rows that have values in "retweeted_status_id", "retweeted_status_user_id" and "retweeted_status_timestamp" columns
# 3. Change the datatype of "timestamp" column to datatime
# 4. Get the right ratings in "rating nominator" & "rating denominator", and merge into one column
# 5. Change the datatype of "tweed_id" columnb to str
# 6. Remove words that are not names in 'name' column
# 
# *twit_json*
# 
# 7. Change the datatype of "tweed_id" columnb to str
# 
# *predict*
# 
# 8. "P1", "P2", "P3" columns should start with upper case letter
# 9. Change the datatype of "tweed_id" columnb to str

# ### Tidiness issues
# *twit_arc*
# 1. Dog stage (doggo, floofer, pupper, puppo) must be merged into one column.
# 
# *twit_json*
# 2. Add the retweet_count and favorite_count columns to the twit_arc, since this data is meant to augment the archived tweet data.
# 
# *predict*
# 3. Add breed prediction column to twit_arc as it could give more information on which breed of dog has been posted most.

# ## Cleaning Data
# In this section, I will clean **all** of the issues I have documented while assessing. 
# 
# **Note:** I have done a copy of the original data before cleaning. Cleaning includes merging individual pieces of data according to the rules of [tidy data](https://cran.r-project.org/web/packages/tidyr/vignettes/tidy-data.html). The result should be a high-quality and tidy master pandas DataFrame (or DataFrames, if appropriate).

# ### Issue #1: *twit_arc* Remove duplicated data in "expanded_urls" column & the rows with null value in the same column
# 

# #### Define: 
# 1. Remove null values in expanded_urls with .dropna functions
# 2. Split the value with .split function, and choose the first value

# #### Code

# In[8]:


# 1. Removing null values in expanded_urls with .dropna functions

twit_arc.dropna(subset = ['expanded_urls'], inplace = True)

# 2. Splitting the value with .split function, and choose the first value
def delete_duplicated_urls(url):
    true_url = url.split(',')[0]
    return true_url

twit_arc['correct_expanded_urls'] = twit_arc.apply(lambda x: delete_duplicated_urls(x['expanded_urls']), axis=1)
twit_arc.drop('expanded_urls', axis=1, inplace=True)

#The apply() function is then used to apply the delete_duplicated_urls() function to each row in the twit_arc DataFrame, using the axis=1 parameter to apply the function row-wise. The resulting URLs are stored in a new column called correct_expanded_urls.
#the original expanded_urls column is dropped from the twit_arc DataFrame using the drop() function, with axis=1 specifying that we want to drop a column rather than a row


# #### Test

# In[9]:


for index,row in twit_arc.iterrows():
    if len(row['correct_expanded_urls'].split(',')) > 1:
        print(row['correct_expanded_urls']) #worked!


# ### Issue #2: Remove rows that have values in "retweeted_status_id", "retweeted_status_user_id" and "retweeted_status_timestamp" columns

# #### Define
# Reason: because the "source" column contains HTML code that needs to be cleaned up before it can be analyzed properly.
# I will remove non-null rows, which are not required for our analysis. Since the three columns shares the same non-empty rows, we can just base on one of the columns.
# 
# 

# #### Code

# In[10]:


retweeted_status_id_index = twit_arc[twit_arc.retweeted_status_id.notnull()].index

twit_arc.drop(retweeted_status_id_index, axis = 0, inplace= True)


# #### Test

# In[11]:


twit_arc[twit_arc.retweeted_status_user_id.notnull()] #worked!


# ### Issue #3: Change the datatype of "timestamp" column to datatime

# #### Define

# datatype from timestamp colum to datatime

# #### Code

# In[12]:


twit_arc.timestamp = twit_arc.timestamp.astype('datetime64')


# #### Test

# In[13]:


twit_arc.info() #worked!


# ### Issue #4: Get the right ratings in "rating nominator" & "rating denominator", and merge into one column

# #### Define

# Finding the right *rating_denominator* and *rating_nominator* by selecting the rows with other denominators than 10. Than changing the values after comparing with what's written on the text column. Finally combining them into the complete ratings, by creating a new column.

# #### Code

# In[14]:


# We found out in the previous assessment that index 1068, 1165, 1662, 2335, 516 must be amended.

numbers = [1068, 1165, 1662, 2335, 516]

for n in numbers:
    print(twit_arc.query('rating_denominator != 10').loc[n, 'rating_numerator'],'/',twit_arc.query('rating_denominator != 10').loc[n, 'rating_denominator'])


# In[15]:


# amending 5 rows

twit_arc['rating_numerator'].replace([9,4, 7, 1,24], [14,13,10, 9, 10], inplace = True)
twit_arc['rating_denominator'].replace([11,20, 11, 2,7], [10,10,10, 10, 10], inplace = True)

# The last column (index 516) doesn't have any ratings in the note, but I will change it to 10/10 for convenience in calculation


# In[16]:


# combining into a single column
twit_arc['ratings'] = twit_arc['rating_numerator'].astype('str') + "/" +twit_arc['rating_denominator'].astype('str')


# #### Test

# In[17]:


numbers = [1068, 1165, 1662, 2335, 516]

for n in numbers:
    print(twit_arc.loc[n, 'ratings'])
    
# I will not drop the original ratings columns for now, since they might come in handy in future.


# ### Issue #5: Change the datatype of "tweed_id" columnb to str

# #### Define
# 
# I will change the datatype of *tweet_id*, *in_reply_to_status_id*, *in_reply_to_user_id* to str

# #### Code

# In[18]:


ids_list = ['tweet_id', "in_reply_to_status_id", "in_reply_to_user_id"]

def string_convert(dataset, column):
    dataset[column] = dataset[column].astype('str')
    result = dataset[column]
    return result

for ids in ids_list:
    string_convert(twit_arc, ids)


# #### Test

# In[19]:


twit_arc.info()


# ### Issue #6: Remove words that are not names in 'name' column

# #### Define
# 
# I will select the names which start with lower case, get their indexes and drop the rows

# #### Code

# In[20]:


mask = twit_arc.name.fillna("lower").str.islower()
column_name = 'name'
twit_arc.loc[mask, column_name] = np.nan
twit_arc.replace(np.nan, "None", inplace = True)


# #### Test

# In[21]:


twit_arc.query('name == "a"') #worked!


# ### Issue twit_json #7: Change the datatype to str & remove unncessary columns
# 

# #### Define
# Change the datatype of "tweed_id" column to str, and remove "in_reply_to_status_id_str", "in_reply_to_user_id_str", "quoted_status_id_str" columns.

# #### Code

# In[22]:


ids_list = ['id', "in_reply_to_status_id", "in_reply_to_user_id", "quoted_status_id"]

for ids in ids_list:
    string_convert(twit_json, ids) #converts from strings to integers
    
twit_json.drop(["in_reply_to_status_id_str", "in_reply_to_user_id_str", "quoted_status_id_str"], axis = 1, inplace = True)


# #### Test

# In[23]:


twit_json.info()


# ### Issue #8: "P1", "P2", "P3" columns should start with upper case letter

# #### Define
# 
# I will change the first letter using .capitalize() function. Since dog names in P1, P2, P3 must start with upper case letter for future analysis. 

# #### Code

# In[24]:


columns_list = ['p1', 'p2', 'p3']

for columns in columns_list:
    predict[columns] = predict[columns].str.capitalize()


# #### Test

# In[25]:


predict.sample(5) #First letter is indeed capitalized


# ### Issue #9: Change the datatype of "tweed_id" columnb to str

# #### Code

# In[26]:


# changing the datatype of tweet_id to str
string_convert(predict, 'tweet_id');


# #### Test

# In[27]:


print(predict['tweet_id'].dtype) #correct


# ### Tidiness : 
# *twit_arc*
# 1. Dog stage (doggo, floofer, pupper, puppo) must be merged into one column.

# #### Code

# In[28]:


twit_arc.doggo.replace('None', '', inplace=True)
twit_arc.doggo.replace(np.NaN, '', inplace=True)
twit_arc.floofer.replace('None', '', inplace=True)
twit_arc.floofer.replace(np.NaN, '', inplace=True)
twit_arc.pupper.replace('None', '', inplace=True)
twit_arc.pupper.replace(np.NaN, '', inplace=True)
twit_arc.puppo.replace('None', '', inplace=True)
twit_arc.puppo.replace(np.NaN, '', inplace=True)


# In[29]:


twit_arc['dog_stage'] = twit_arc.doggo + twit_arc.floofer + twit_arc.pupper + twit_arc.puppo
twit_arc.loc[twit_arc.dog_stage == 'doggopupper', 'dog_stage'] = 'doggo,pupper'
twit_arc.loc[twit_arc.dog_stage == 'doggopuppo', 'dog_stage'] = 'doggo,puppo'
twit_arc.loc[twit_arc.dog_stage == 'doggofloofer', 'dog_stage'] = 'doggo,floofer'
twit_arc.dog_stage.replace('', "None", inplace = True)

twit_arc.drop(['doggo', 'floofer', 'pupper', 'puppo'], axis=1, inplace=True)


# #### Test

# In[30]:


twit_arc.dog_stage.value_counts()


# ### Tidiness: 
# *twit_json*
# 2. Add the retweet_count and favorite_count columns to the twit_arc, since this data is meant to augment the archived tweet data.
# 

# #### Code

# In[31]:


# Rename the 'id' column to 'tweet_id' in the twit_json dataset
twit_json.rename(columns = {'id': 'tweet_id'}, inplace = True)
id_retweet = twit_json[['tweet_id','retweet_count', 'favorite_count']]
twit_arc = pd.merge(twit_arc, id_retweet, on = ['tweet_id'])


# #### Test

# In[46]:


twit_arc.info()


# ### Tidiness:
# *predict*
# 3. Add breed prediction column to twit_arc as it could give more information on which breed of dog has been posted most.

# #### Code

# In[32]:


# Function to extract the correct breed prediction
dog_predict = []

for i in range(len(predict)):
    if predict['p1_dog'][i] == True:
        dog_predict.append(predict['p1'][i])
    elif predict['p2_dog'][i] == True:
        dog_predict.append(predict['p2'][i])
    elif predict['p3_dog'][i] == True:
        dog_predict.append(predict['p3'][i])
    else: 
        dog_predict.append("No correct prediction")

        # Applying the function to the predict dataset
predict['dog_predict'] = dog_predict
predict_copy = predict[['tweet_id', 'dog_predict']]

# Merge the breed_prediction column into the twit_arc dataset
twit_arc = pd.merge(twit_arc, predict_copy, on = ['tweet_id'], how= 'left')


# #### Test

# In[33]:


print("Columns in twit_arc dataset:", twit_arc.columns) #breed_prediction column has been added


# In[34]:


twit_arc.sample(2)


# ## Storing Data
# Saving gathered, assessed, and cleaned master dataset to a CSV file named "twitter_archive_master.csv".

# In[35]:


# Save the master dataset to a CSV file
twit_arc.to_csv('twitter_archive_master.csv', index=False)
twit_arc


# ## Analyzing and Visualizing Data
# In this section, I will analyze and visualize the wrangled data.

# ### 1) Most popular breed?
# 
# #### Code

# In[36]:


import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')
print(twit_arc.columns) #to check if there's no error in the merge of the dataframes


# In[37]:


# Getting the counts of each breed prediction
breed_counts = twit_arc['dog_predict'].value_counts()

# Getting the top 5 most popular breeds
top_5_breeds = breed_counts.head(6)

# Print the top 5 most popular breeds
print("Top 5 most popular breeds:")
print(top_5_breeds)


# ### Insight:
# 
# > Top 5 most popular beeds on the "We Rate Dog" account are: Golden retriever, Labrador, Pembroke, Chihuahua and Pug.
# > There's a high number of breeds not predicted tho

# ### Visualization

# In[45]:


# Creating a bar chart of the top 5 most popular breeds
fig, ax = plt.subplots(figsize=(15,9))
ax.bar(top_5_breeds.index, top_5_breeds.values, color=['#c2c2f0', '#c2c2f0', '#c2c2f0', '#c2c2f0', '#c2c2f0'])

# Add labels and title to the chart
ax.set_xlabel('Dog Breed', size = 15)
ax.set_ylabel('Number of Occurrences', size = 15)
ax.set_title('Top 5 Most Popular Dog Breeds', size = 15)
plt.xticks(rotation= 20, size = 12)
plt.yticks(size = 12)

# Display the chart
plt.show()


# ### 2) Most common name?
# 
# #### Code

# In[39]:


# Get the counts of each dog name
name_counts = twit_arc['name'].value_counts()

# Print the most common dog name
print("The 1st most common dog name is:", name_counts.index[0])
print("The 2nd most common dog name is:", name_counts.index[1])
print("The 3rd most common dog name is:", name_counts.index[2])
print("The 4th most common dog name is:", name_counts.index[3])
print("The 5th most common dog name is:", name_counts.index[4])


# In[73]:


name_counts


# ### Insights

# > - A very high number of 726 have no dog name. Possibly were not properly recorded. 
# > - For female & male dogs: Lucy and Charlie are the most popular names.
# > - After None, 11 names can be place on the top 5 most common names, since their qualification matches (no difference of number of name, or only 1 name difference)
# 

# ### Visualization

# In[82]:


# Defining fun colors
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6', '#8fd9b6', '#d9b38c', '#80d4ff', '#bf80ff', '#ff6666', '#b3b3cc']
#Plotting
popular_name = twit_arc.name.value_counts()[:12] 
plt.figure(figsize = (9,9))
plt.title("Most Popular Dog Names", size = 20)
plt.pie(popular_name, labels = popular_name.index, colors = colors, autopct='%1.1f%%', textprops={'fontsize': 13});


# In[83]:


#checking with and without the None names:

# Extracting the top and top - first names (excluding the first most common name)
top_11_names = twit_arc['name'].value_counts().head(12)
top_10_names_excluding_first = twit_arc['name'].value_counts().iloc[1:12]

# Creating a 1x2 subplot for the pie charts
fig, axes = plt.subplots(1, 2, figsize=(18, 9))

# Plotting the first pie chart with the top 11 names
axes[0].pie(top_11_names, labels=top_11_names.index, colors=colors, autopct='%1.1f%%', textprops={'fontsize': 13})
axes[0].set_title('Top Most Common Dog Names', size=20)

# Plotting the second pie chart with the top 10 names (excluding the first most common name)
axes[1].pie(top_10_names_excluding_first, labels=top_10_names_excluding_first.index, colors=colors[1:], autopct='%1.1f%%', textprops={'fontsize': 13})
axes[1].set_title('Top Most Common Dog Names (without None)', size=20)

# Display the pie charts
plt.show()


# ### 3) Most common rating?
# 
# #### Code

# In[49]:


# Geting the counts of each rating
rating_counts = twit_arc['rating_numerator'].value_counts()

# Geting the 5 most common rating
most_common_rating = rating_counts.index[0:5]

# Printing the most common rating
print("The most common rating is:", most_common_rating)


# ### Insights

# > - The most popular rating is 10/10, 12/10, and 11/10. 
# > - It was found that *WeRateDogs* tend to give high ratings to most of the dogs they post.

# ### Visualization

# In[58]:


frequent_rating = twit_arc.ratings.value_counts()[:10]

plt.figure(figsize = (12,7))
plt.barh(y = frequent_rating.index, width= frequent_rating,  color=['#c2c2f0', '#c2c2f0', '#c2c2f0', '#c2c2f0', '#c2c2f0'])
plt.title("Top 10 Frequent Rating", size = 20)
plt.ylabel("Rating", size = 15)
plt.xlabel("Number of Tweet", size = 15)
plt.xticks(size = 13)
plt.yticks(size = 13)
plt.gca().invert_yaxis()

for index, value in enumerate(frequent_rating):
    plt.text(value, index, str(value), size = 13)
    
plt.show()

