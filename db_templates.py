import uuid
import urllib
from bs4 import BeautifulSoup
import text2emotion
#file provides functions to create various database doccuments

file = open("common_words.txt")
commons = file.read().replace('\t',' ').replace('\n',' ').split(' ')



def user_template(username='',first_name='',last_name='',email='',interests=[]):
    """returns dictionary representing a user for creating new user doccument"""
    user = {
        "user_id": str(uuid.uuid1()),
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "interests": interests,
    }
    return user

def topic_template(topic="empty-topic",sub_topics=[]):
    temp = {
        "topic": topic,
        "sub_topics":sub_topics
        }
    return temp


def get_sentiment(article):
    url = "https://www.cnn.com/2021/02/13/politics/trump-legal-problems-post-impeachment/index.html"
    html = urllib.request.urlopen(article['url']).read()
    soup = BeautifulSoup(html)

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    text = text.split(" ")
    print(type(text))
    common_word = {""}
    n = []
    for word in text:
        if (word.strip().islower() and word not in commons):
            n.append(word)
    text = ''.join(str(e+' ') for e in n)
    sentiment = text2emotion.get_emotion(text)
    print("Calulated Sentiment:",sentiment)
    return sentiment



    