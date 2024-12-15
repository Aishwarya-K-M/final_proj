
import pandas as pd
import string
import emoji

posf = open("data_generation\positive_text.txt",'r', encoding='UTF-8')

final = open("data_generation\dataset.csv",'w', encoding='UTF-8')
final.write("headline,label\n")

data = posf.readlines()

def unicode_escape(chars, data_dict):
    return ' '+chars.encode('unicode-escape').decode()+' '


for i in data:
    final.write(emoji.replace_emoji(i[1:len(i)-2].replace(',',''),replace=unicode_escape)+',0\n')

negf = open("data_generation/negative_text.txt",'r',encoding='UTF-8')
data = negf.readlines()

for i in data:
    final.write(emoji.replace_emoji(i[1:len(i)-2].replace(',',''),replace=unicode_escape)+',1\n')


df = pd.read_excel("data_generation/hasoc_2020_hi_train.xlsx", engine='openpyxl')

import re


df["text"] = df['text'].str.replace("(@[\w]*:)|((\. *)*)|(\!)|(\:)", "",regex=True)

df['text'] = df['text'].str.replace("@[\w]*", "",regex=True)
df['text'] = df['text'].str.replace("(RT )|(\n*)", "",regex=True)
df['text'] = df['text'].str.replace(" +", " ",regex=True)
df['text'] = df['text'].str.replace("…+", " ",regex=True)

df['text'] = df['text'].str.replace('[{}]*'.format(string.punctuation), '',regex=True)

def unicode_escape(chars, data_dict):
    return ' '+chars.encode('unicode-escape').decode()+' '

df['text'] = emoji.replace_emoji(df['text'].str, replace=unicode_escape)
print(type(df['text'].str))


for ind,row in df.iterrows():
    text = row['text']
    text = emoji.replace_emoji(text,replace=unicode_escape)
    flag = 1 if row['task1']=='HOF' else 0
    final.write(text+','+str(flag)+'\n')

final.close()
posf.close()
negf.close()



import stanza


nlp = stanza.Pipeline(lang='hi', processors='tokenize')

df = pd.read_csv("cyber_bullying_detection\data_generation\dataset.csv")

final = open("cyber_bullying_detection\data_generation\dataset.csv",'w', encoding='UTF-8')

final.write('data,label\n')



df['headline'] = df['headline'].apply(lambda x :' '.join([word.text for sent in nlp(x).sentences for word in sent.words]))

df.to_csv("cyber_bullying_detection\data_generation\dataset.csv", encoding='utf-8', index=False)

final.close()
import pandas as pd
import string

df = pd.read_csv("cyber_bullying_detection\data_generation\dataset.csv")
df['headline'] = df['headline'].str.replace("[\'\"\|]*", "",regex=True)
df['headline'] = df['headline'].str.replace('[{}]*'.format(string.punctuation), '',regex=True)

df.to_csv("cyber_bullying_detection\data_generation\dataset.csv", encoding='utf-8', index=False)
