#!/usr/bin/env python
# coding: utf-8

# # Opinion Mining
# 

# : Importing Libraries

# In[4]:


'''importing the libraries '''
import re 
import tweepy 
from tweepy import OAuthHandler 
import matplotlib.pyplot as plt
from textblob import TextBlob 

  


# :Authentication details to use Twitter API
# : Data Collection
# : Data Preprocessing
# : Obtaining polarity

# In[5]:


class TwitterClient(object): 
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''
    def __init__(self): 
        ''' 
        Class constructor or initialization method. 
        '''
        # keys and tokens from the Twitter Dev Console 
        consumer_key = 'yNiDNebQueqf3u0khRuOdc5L6'
        consumer_secret = 'TDA3XVBMfcnKHK6yK8rI6xO2FS0F21TKWl6kp6Fvsdpvs2MIbD'
        access_token = '1265313276273065984-veTIle2akFBZrWQAcubj310Muq4voG'
        access_token_secret = 'jBxhjuZHcrWbIZV8OoZ3VdjTgo4ZLMmDFxPIM3yaF550b'
  
  
        # attempt authentication 
        try: 
            # create OAuthHandler object 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 
  
    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 
  
    def get_tweet_sentiment(self, tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
  
    def get_tweets(self, query, count = 10): 
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        # empty list to store parsed tweets 
        tweets = [] 
  
        try: 
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search(q = query, count = count) 
  
            # parsing tweets one by one 
            for tweet in fetched_tweets: 
                # empty dictionary to store required params of a tweet 
                parsed_tweet = {} 
  
                # saving text of tweet 
                parsed_tweet['text'] = tweet.text 
                # saving sentiment of tweet 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
  
                # appending parsed tweet to tweets list 
                if tweet.retweet_count > 0: 
                    # if tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
  
            # return parsed tweets 
            return tweets 
  
        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e)) 
  


# : Main Function to print polarity, fetched Tweets: Data Visualization

# In[ ]:


def main(): 
    # creating object of TwitterClient Class 
    api = TwitterClient() 
    # calling function to get tweets 
    tweets = api.get_tweets(query = 'Corona', count = 200) 
    
     #printing a set tweets from the total fetched tweets
    print('A set of fetched tweets:')
    for tweet in tweets[:10]: 
        print(tweet['text']) 
  
    print('\n')
    
    print('Polarity of Tweets Fetched:')
    print('\n')
    
  
    # picking positive tweets from tweets 
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
    # percentage of positive tweets 
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 
    # picking negative tweets from tweets 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
    # percentage of negative tweets 
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
    # percentage of neutral tweets 
    print("Neutral tweets percentage: {} % ".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets))) 
    
    #plotting the output on pie chart
    # Data to plot
    labels = 'Positive', 'Negative', 'Neutral'
    sizes = [len(ptweets), len(ntweets),len(tweets) -(len( ntweets )+len( ptweets)),]
    colors = ['gold',  'lightcoral', 'lightskyblue']
    explode = (0, 0, 0.1) 

    # Plot
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,shadow=True,autopct='%1.1f%%', startangle=90)

    plt.axis('equal')
    plt.show()
  
   
  
if __name__ == "__main__": 
    # calling main function 
    main() 

