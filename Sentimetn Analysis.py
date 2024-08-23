#!/usr/bin/env python
# coding: utf-8

# In[19]:


import pandas as pd
import requests
from bs4 import BeautifulSoup

# Load your DataFrame
df = pd.read_excel('Input.xlsx')

for index, row in df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']  # Ensure this is the correct column name and it's correctly read
    
    # Debugging print
    print(f"Attempting to fetch: {url}")
    
    # Fetch the HTML content from the URL
    try:
        response = requests.get(url.strip())  # Strip any leading/trailing spaces
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the article title and content (modify as needed)
        article = soup.find('div', class_='td-post-content').get_text()
        
        # Save the article
        file_name = f'{url_id}.txt'
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(article)
        
        print(f'Article {url_id} saved successfully as {file_name}!')
    
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}: {e}")

print("All articles have been scraped and saved.")


# In[26]:


#loading the extracted text files

import os

def load_text_files(directory):
    articles = {}
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            url_id = filename.split('.')[0]
            with open(os.path.join(directory,filename), 'r',encoding='utf-8') as file:
                     articles[url_id] = file.read()
    return articles
articles = load_text_files(r'C:\Users\Lankala Vinay Kumar\Articles')                             
                             


# In[ ]:





# In[36]:


import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from collections import Counter


def analyze_article(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())
    
    #removing stopwords and Puntuations
    
    words = [words for words in words if words.isalpha()]
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    
    
    #loading the neg and postive word lists
    
    positive_words = set(open('positive-words.txt').read().split())
    negative_words = set(open('negative-words.txt').read().split())
     
    positive_score = sum(1 for word in words if word  in positive_words)
    negative_score = sum(1 for word in words if word in negative_words)
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score)+0.0000001)
    subjectivity_score = (positive_score + negative_score) / (len(words) + 0.000001)
    
    avg_sentence_length = len(words)/ len(sentences)
    syllable_count = lambda word: sum([1 for char in word if char in 'aeiou'])
    complex_word_count = sum(1 for word in words if syllable_count(word) > 2)
    percentage_complex_words = complex_word_count / len(words)
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    avg_words_per_sentence = len(words) / len(sentences)
    avg_word_length = sum(len(word) for word in words) / len(words)
    syllables_per_word = sum(syllable_count(word) for word in words) / len(words)
    personal_pronouns = sum(1 for word in words if word in ['i', 'we', 'my', 'ours', 'us'])

    return {
        'Positive Score': positive_score,
        'Negative Score': negative_score,
        'Polarity Score': polarity_score,
        'Subjectivity Score': subjectivity_score,
        'Avg Sentence Length': avg_sentence_length,
        'Percentage of Complex Words': percentage_complex_words,
        'Fog Index': fog_index,
        'Avg Number of Words Per Sentence': avg_words_per_sentence,
        'Complex Word Count': complex_word_count,
        'Word Count': len(words),
        'Syllables Per Word': syllables_per_word,
        'Personal Pronouns': personal_pronouns,
        'Avg Word Length': avg_word_length,
    }

analysis_results = {url_id: analyze_article(article) for url_id, article in articles.items()}





    
    


# In[45]:


import pandas as pd

output_data = []

for url_id, analysis in analysis_results.items():
    row = {'URL_ID': url_id , 'URL': url}
    row.update(analysis)
    output_data.append(row)

output_df = pd.DataFrame(output_data)
output_df.to_excel('Output Data Structure.xlsx', index=False)


# In[46]:


df1= pd.read_excel('Output Data Structure.xlsx')
df1.head()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




