
# coding: utf-8

# In[24]:


#!pip install PyPDF2


# ## Generating Word Frequency Dataframe from PDF File

# In[25]:


import os
import sys
import re
import time
import PyPDF2
import numpy as np
import pandas as pd


# ### Creating Word-Corpus

# In[26]:


def getPageCount(pdf_file):

    pdfFileObj = open(pdf_file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pages = pdfReader.numPages
    return pages

def removegarbage(str):
    # Replace one or more non-word (non-alphanumeric) chars with a space
    str = re.sub(r'\W+', ' ', str)
    str = str.lower()
    return str

def extractData(pdf_file, page):

    pdfFileObj = open(pdf_file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pageObj = pdfReader.getPage(page)
    data = pageObj.extractText()
    data = removegarbage(data)
    return data

def getWordCount(data):

    data=data.split()
    return len(data)

# get the word count in the pdf file
pdfFile = 'rj.pdf'
numPages = getPageCount(pdfFile)
corpus = ""
for i in range(numPages):
    corpus = corpus + " " + extractData(pdfFile, i)
time.sleep(1)


# ### Creating Word-Frequency Dataframe

# In[27]:


wordlist = corpus.split()
wordfreq = []
for w in wordlist:
    wordfreq.append(wordlist.count(w))
    
wordlist = pd.Series(wordlist)
wordfreq = pd.Series(wordfreq)
df = pd.DataFrame({'Words': wordlist})
df['Frequency'] = wordfreq
df = df.sort_values(by=['Frequency'], ascending=False)


# ### Text Pre-processing

# In[29]:


df1 = df.copy()
df1.loc[:,"Words"] = df1.Words.apply(lambda x : str.lower(x))

import re
df1.loc[:,"Words"] = df1.Words.apply(lambda x : " ".join(re.findall('[\w]+',x)))

from nltk.corpus import stopwords
stop_words = stopwords.words('english')

def remove_stopWords(s):
    '''For removing stop words
    '''
    s = ' '.join(word for word in s.split() if word not in stop_words)
    return s

df1.loc[:,"Words"] = df1.Words.apply(lambda x: remove_stopWords(x))

df1['Words'].replace('', np.nan, inplace=True)
df1.dropna(subset=['Words'], inplace=True)
df1 = df1.groupby('Words').sum().sort_values(by=['Frequency'], ascending=False)
df1 = df1.reset_index()


# ### Creating Word Cloud

# In[30]:


import matplotlib as mpl
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

from subprocess import check_output
from wordcloud import WordCloud, STOPWORDS

#mpl.rcParams['figure.figsize']=(8.0,6.0)    #(6.0,4.0)
mpl.rcParams['font.size']=12                #10 
mpl.rcParams['savefig.dpi']=100             #72 
mpl.rcParams['figure.subplot.bottom']=.1 
stopwords = set(STOPWORDS)

wordcloud = WordCloud(
                          background_color='white',
                          stopwords=stopwords,
                          max_words=200,
                          max_font_size=40, 
                          random_state=42
                         ).generate(str(df1['Words']))

print(wordcloud)
fig = plt.figure(1)
plt.imshow(wordcloud)
plt.axis('off')
plt.show()
fig.savefig("word1.png", dpi=900)


# ### Importing Required libraries for sending Mail

# In[31]:


import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


# ### Send Email attaching the Wordcloud file

# In[23]:


import win32com.client as win32
outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = "abc@gmail.com"
mail.Subject = "Word cloud of the Novel PDF"
mail.Body = "Congratulation!, Your wordcloud has been generated. Please Find Attached toe required File!"

# To attach a file to the email (optional):
attachment  = "C:\\Users\\xyz\\word1.png"
mail.Attachments.Add(attachment)
#Sending the mail
mail.Send()

