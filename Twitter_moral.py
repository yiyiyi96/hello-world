import tweepy
from urllib.request import urlopen
import json
import re
import csv

#Getting rid of the punctuations
#re_tok = re.compile('([' + string.punctuation + '“”¨«»®´·º½¾¿¡§£₤‘’])')
#def tokenize(s):
#  return re_tok.sub(r' \1 ', s).split()

auth = tweepy.OAuthHandler("-------------",
                            "--------------------")
auth.set_access_token("------------------",
                        "------------------")

api = tweepy.API(auth)

moralwords = []

#importing words from moral word list .csv
with open('Moral_and_Non-moral_Word_List.csv', newline='') as csvfile:
    moralwordreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in moralwordreader:
        if row[1] == "Moral":
            moralwords.append(row[0])
        else: continue

Moral_keywords = {'hate', 'should', 'wrong', 'bad', 'moral', 'disgust',
                'impure','shame','guilt','good','wrong','blame','must',
                'mistake','suffer','trust','justice','good','fair','fairness',
                'authority','honor','guilty','shameful','shameless','saint',
                'praiseworthy','blameworthy','obnoxious','respect','respectful',
                'responsible','responsibility','obedience','obedient','sympathetic',
                'care','prejudice','liberal','conservative','tradition','cononical'
                'holy','sanctity','abuse','remorseful','kind','kindness','loyalty',
                'sage','samaritan','stoic','epicurean','moral','morality','ethical',
                'ought','traditional','sacred','cheat','hatred','duty','progressive',
                'awe','desire','fear','greed'}

for word in Moral_keywords:
    if word not in moralwords:
        moralwords.append(word)
    else: continue

while True:
    username = input ('Please enter twitter account: ')
    if username == 'quit':
        break

#get tweets from specific users
    user_tweets = api.user_timeline(username)
#This creates a list to hold all the moral tweets
    moral_tweet = list()

    for tweet in user_tweets:
        tweety = tweet.text.replace(',','').replace('.','').replace('!','').replace('?','').lower().split()
        #tweety = tweet.text.lower().split()
        #tweety = tokenize(tweet.text.lower())
        #this count is used to keep track of the number
        #of moral words in each tweet
        count = dict()
        #This creates the list for sorting moral words in each tweet
        moral_list = list()
        word_count = 0

        for keyword in moralwords:
            count[keyword] = 0
        for word in tweety:
            #print(word)
            if word in moralwords:
                count[word]=count.get(word,0) + 1
                word_count = word_count + 1
            else: continue
#If a tweet contains at least one moral word, then it is put
#into the moral tweet list
        if word_count > 0:
            moral_tweet.append(tweety)

    #Now the count should represent the number of moral words for the tweet.
    #Only moral keywords that actually appeared will be appended to the
    #moral list
        for (k, v) in count.items():
            if v > 0:
                moral_list.append((k, v))
            else: continue
        print(tweet.text)
        if moral_list == []:
            print('\nThis message does not contain moral words.\n')
        else:
            print(sorted(moral_list, key = lambda pair:[1], reverse = True))
