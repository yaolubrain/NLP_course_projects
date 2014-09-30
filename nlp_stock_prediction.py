import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB


def GetFeatures(file):
    text = open(file).read()

    events = re.compile('<DOCUMENT>(.*?)</DOCUMENT>', re.DOTALL).findall(text)
    events = [' '.join(event.split()) for event in events]    

    count_vect = CountVectorizer()
    word_counts = count_vect.fit_transform(events)    

    tfidf_transformer = TfidfTransformer()
    features = tfidf_transformer.fit_transform(word_counts)

    return features

def GetLabels(doc_file, price_file):    
    events_time = [int(line[5:-1]) for line in open(doc_file) if line.startswith('TIME:')][::-1]
    events_num = len(events_time)    

    idx = 0
    last_price = ''
    labels = np.zeros(events_num, dtype=int)    

    market_begin_time = '093000'
    market_close_time = '160000'

    with open(price_file) as f:
        next(f)
        for line in f:                              
            price = line.split(',')
            price_date = price[0].replace('-','')
            price_begin_time = int(price_date + market_begin_time)
            price_close_time = int(price_date + market_close_time)   
            
            if idx == 0:
                last_price = price
            
            last_price_date = last_price[0].replace('-','')
            last_price_begin_time = int(last_price_date + market_begin_time)
            
            if events_time[idx] >= price_begin_time and events_time[idx] <= price_close_time:
                #print events_time[idx], price_begin_time, price_close_time 
                price_diff = float(price[2]) - float(price[1])
                if abs(price_diff) / float(price[1]) > 0.01:
                    if price_diff > 0:
                        labels[idx] = 0
                    else:
                        labels[idx] = 1                        
                else:
                    labels[idx] = 2
                
            elif events_time[idx] >= price_close_time and events_time[idx] <= last_price_begin_time:
                #print events_time[idx], last_price_begin_time, price_close_time            
                price_diff = float(last_price[1]) - float(price[2])
                if abs(price_diff) / float(price[2]) > 0.01:
                    if price_diff > 0:
                        labels[idx] = 0
                    else:
                        labels[idx] = 1                        
                else:
                    labels[idx] = 2
            
            else:
                while events_time[idx] > last_price_begin_time and idx < events_num - 1:
                    idx += 1
                
            last_price = price

    return labels            
            

doc_file = "/home/yao/Downloads/NLP/8K-gz/A"
price_file = "/home/yao/Downloads/NLP/price_history/A.csv"

features = GetFeatures(doc_file)
labels = GetLabels(doc_file, price_file)

train_features = features[:100,:]
test_features = features[100:,:]
train_labels = labels[:100]
test_labels = labels[100:]

clf = MultinomialNB().fit(train_features, train_labels)

predicted = clf.predict(test_features)
print np.mean(predicted == test_labels)     