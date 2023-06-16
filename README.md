# WeRateDogs Twitter Project (WeRateDogs-Dataset)
*By Carla Mota Leal*

![WeRateDogs](/weratedogs.png)

The WeRateDogs Twitter project aimed to **gather, assess, and clean data** from various sources, including the *WeRateDogs Twitter archive*, *tweet image predictions*, and additional data obtained through the *Twitter API*. The objective was to wrangle the data and derive insights from it. Here I will provide you a summary of the wrangling efforts undertaken for this project.
## **Data Wrangling**
The data wrangling process involved several key steps, including data gathering, data assess- ment, and data cleaning.

**1. Data Gathering:** 
The necessary libraries, such as *tweepy, pandas, numpy, requests, and json*, were imported. The WeRateDogs Twitter archive data, stored in the file "twit- ter_archive_enhanced.csv," was downloaded. 
Additionally, the tweet image predictions file, "image_predictions.tsv," was programmatically downloaded using the Requests library. 
Further data was obtained by **querying the Twitter API and storing the resulting JSON data in a TXT file**.

**2. Data Assessment:**
A combination of visual and programmatic assessment techniques was employed to identify quality and tidiness issues within the dataset. Quality issues primarily included incorrect datatypes, duplicated data, missing values, and inconsistent ratings. Tidiness issues revolved around merging columns and adding relevant data to the main dataset.

## **Data Cleaning**
To address the identified issues, a systematic data cleaning process was implemented. The cleaning process involved the following steps:

**1. Quality Issues:** 
Several quality issues were addressed, including the removal of du- plicated data in the "expanded_urls" column and the elimination of rows with null values in the same column. Rows with non-null values in the "retweeted_status_id," "retweeted_status_user_id," and "retweeted_status_timestamp" columns were also re- moved. 
The datatype of the "timestamp" column was changed to datetime for consistency. Accurate ratings were obtained by selecting rows with denominators other than 10 and comparing them with the text column. 
Additionally, the datatypes of relevant columns such as "tweet_id," "in_reply_to_status_id," and "in_reply_to_user_id" were converted to string. Non-name words in the ’name’ column were removed, ensuring only valid names remained. The "P1," "P2," and "P3" columns in the "predict" dataset were capitalized to maintain con- sistency.

**2. Tidiness Issues:** 
Tidiness issues were addressed by merging the dog stage columns (doggo, floofer, pupper, puppo) into a single column within the "twit_arc" dataset. The "retweet_count" and "favorite_count" columns from the "twit_json" dataset were added to augment the archived tweet data. Additionally, a breed prediction column was added to the "twit_arc" dataset based on the image predictions.

## **Data Storage**
The final cleaned dataset was stored in a CSV file named "twitter_archive_master.csv."

## **Data Analysis and Visualization**

The cleaned dataset was analyzed to derive insights and create visualizations. Three key insights were obtained:

*1. Most Popular Breeds:* The analysis revealed that the top five most popular breeds on the WeRateDogs account were Golden Retriever, Labrador, Pembroke, Chihuahua, and Pug. However, it was noted that a significant number of breeds were not predicted in the dataset. To visualize this finding, a bar plot was created, showcasing the popularity of different breeds.

*2. Most Common Names:* The analysis showed that approximately 726 dogs had no recorded names, indicating a data recording issue. For female and male dogs, Lucy and Charlie emerged as the most popular names, respectively. Additionally, several other common names were identified based on qualification matches. A pie chart was created to visual- ize the distribution of dog names.

*3. Most Common Ratings:* The analysis revealed that the most popular ratings given by WeR- ateDogs were 10/10, 12/10, and 11/10. It was observed that WeRateDogs tended to give higher ratings to most of the dogs they featured. To visualize this finding, a bar plot was created, illustrating the distribution of ratings.
In conclusion, the WeRateDogs Twitter project involved extensive data wrangling efforts, in- cluding data gathering, assessment, and cleaning. The cleaned dataset provided a solid foun- dation for deriving insights and creating visualizations. 

> The resulting analysis shed light on the most popular breeds, common dog names, and popular ratings within the WeRateDogs Twitter account.
