
# coding: utf-8

# ### Пошук фізичної особи
# Отримання публічної інформації щодо особи, за її ПІБ: наявність в розшуку МВС, наявність стороною відповідача по справі в адміністративних, кримінальніх та господарських процесах (з лютого 2016), наявність в базі боржників за аліментами
# 
# ### Seach for 
# Obtaining public information about a person, for her name: presence in search of the Ministry of Internal Affairs, the presence of the party defendant in the case in administrative, criminal and economic processes (since February 2016), the presence of debtors on alimony

# #### OpenDataBot API: https://docs.opendatabot.com/

# In[1]:


# search for person via NAME*, SURNAME*, FATHERSNAME
# name = input()
name = "Ткаченко Катерина Володимирівна"
print(name)


# In[6]:


import requests
import json
# temperary API key
key = "MwMPpuQ6hW"
# resp = requests.get("https://opendatabot.com/api/v2/person?apiKey=" + key +"&pib="+name)
# data = resp.json()


# In[11]:


with open('test_data.txt') as json_file:  
    data = json.load(json_file)


# In[8]:


wanted = 'W'
sessions = 'S'
corrupt = 'C'


# In[37]:


def filter_by_name(recieved_name):
    if name in recieved_name:
        return True
    
def parser(data, identificator):
    data_list = []
    for item in range(0, len(data)):
        values = list(data[item].values()) 
        person_name = find_name(values,identificator)
        if filter_by_name(person_name):
            tr = trust_counter(values[1], identificator)
            data_list.append(values)
            data_list.append(tr)
    return data_list

def find_name(data, identificator):
    if identificator == wanted or identificator == corrupt:
        person_name = data[1]
    elif identificator == sessions:
        involved = data[3].split(',')
        person_name = involved[1].split(': ')[1]
    return person_name

def trust_by_forma(forma):
    counter = 0
    if forma == 'Адміністративні справи':
        counter += 20
    elif forma == 'Кримінальні справи':
        counter += 80
    return counter 

def trust_by_identificator(identificator):
    counter = 0
    if identificator == wanted or identificator ==  corrupt:
        counter += 100
    return counter

def trust_counter(forma, identificator):
    return trust_by_forma(forma) + trust_by_identificator(identificator)

def write_file(identificator, out_data, file):
    file.write(i)
    file.write(str(out_data))
    file.write("\n")


# In[38]:


file = open("output_file", "w")
for i in data:
    if i == 'wanted' and data[i] != {'count': 0}:
        write_file(i,parser(data[i]['persons'], wanted), file)
    elif i == 'sessions' and data[i] != {'count': 0}:
        write_file(i,parser(data[i]['sessions'], sessions), file)
    elif i == 'corrupt_officials' and data[i] != {'count': 0, 'corrupt_officials': []}:
        write_file(i,parser(data[i]['corrupt_officials'],corrupt), file)
file.close()

