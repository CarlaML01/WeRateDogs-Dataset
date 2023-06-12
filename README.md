# WeRateDogs-Dataset
WeRateDogs twitter archive dataset for data wrangling, data analyses and visualizations.

## Project Steps Overview
My tasks in this project are as follows:

Step 1: Gathering data

Step 2: Assessing data

Step 3: Cleaning data

Step 4: Storing data

Step 5: Analyzing, and visualizing data

Step 6: Reporting

## Data info

The dataset to be wrangling (and analyzing and visualizing) is the tweet archive of Twitter user @dog_rates, also known as WeRateDogs. WeRateDogs is a Twitter account that rates people's dogs with a humorous comment about the dog. 

These ratings almost always have a denominator of 10. The numerators, though? Almost always greater than 10. 11/10, 12/10, 13/10, etc. Why? Because "they're good dogs Brent." WeRateDogs has over 4 million followers and has received international media coverage.

This archive contains basic tweet data (tweet ID, timestamp, text, etc.) for all 5000+ of their tweets as they stood on August 1, 2017. 

## Step 1 Checklist

- I have downloaded and uploaded twitter_Archive_enhanced.csv
- I have downloaded image_predictions.tsv from the provided URL using Request library
- I have queried each tweet's retweet count and favorite ("like") count using the Tweepy library and stored the data in tweet_json.txt
- I have read the tweet_json.txt line by line into a pandas DataFrame with tweet ID, retweet count, and favorite count

_Additional Resource: Twitter API_
