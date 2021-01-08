#!/usr/bin/env python
# coding: utf-8

# In[107]:


import re
import json
import urllib
import requests
import mysql.connector
from bs4 import BeautifulSoup


# In[163]:

# iit delhi branch faculty url's
chem_url = "http://chemical.iitd.ac.in/faculties/"
machanics_url = "https://am.iitd.ac.in/?q=node/24"
biochem_url = "https://beb.iitd.ac.in/faculty.html"
maths_url = "https://maths.iitd.ac.in/drupal/faculty"
textile_url = "https://textile.iitd.ac.in/faculty.php"
chemistry_url = "https://chemistry.iitd.ac.in/faculty.html"
electrical_url = "https://ee.iitd.ac.in/people/faculty.html"
civil_url = "https://civil.iitd.ac.in/index.php?lmenuid=faculty"
cse_url = "https://www.cse.iitd.ac.in/index.php/2011-12-29-23-14-30/faculty"


# In[164]:


headers = { "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9"}


# In[165]:


def create_database_connection():
    '''
    create connection with database
    '''
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Harshit77",
        database="NUTOM"
    )

    return mydb


# In[166]:


def get_soup(url):
    '''
    returns soup of website
    '''
    soup = None
    try:
        response  = requests.get(url, headers=headers, verify=False)
        data = response.text
        soup = BeautifulSoup(data,'lxml')
    except Exception as e:
        print(e)
    
    return soup


# In[167]:


def get_json(url):
    '''
    returns json data from website
    '''
    data = []
    try:
        response = urllib.urlopen(url)
        data = json.loads(response.read())
    except Exception as e:
        print(e)
    
    return data


# In[168]:


def create_table(mycursor):
    '''
    creates table
    '''
    sql_query = "DROP TABLE IF EXISTS professor_data"
    mycursor.execute(sql_query)

    sql_query = "create table professor_data(college varchar(50) NOT NULL,department varchar(50) NOT NULL,name varchar(100) NOT NULL,specialization varchar(500));"
    mycursor.execute(sql_query)


# In[169]:


def insert_data_into_table(mycursor, college, department, professor_name, professor_specialization):
    '''
    inserts data into faculty table
    '''
    try:
        sql_query = "INSERT INTO professor_data (college, department, name, specialization) VALUES (%s, %s, %s, %s)"
        val = (college, department, professor_name, professor_specialization)
        mycursor.execute(sql_query, val)
    except Exception as e:
        print(e)


# In[170]:


def fetch_biochem_faculty(url, mycursor):
    '''
    fetches biochemical department faculty and stores in mysql database
    '''
    soup = get_soup(url)
    data = soup.findAll('div', {'class' : 'card'})
    
    for i in range(0, len(data)):
        try:
            name = data[i].find('font', {'class' : 'name'}).text.strip()
            data_text = data[i].find('font', {'class' : 'details'}).text
            data_list = re.split('Interests|View', data_text)
            specialization = re.sub('\s+',' ',data_list[1])
        except:
            continue
        
        insert_data_into_table(mycursor, "IIT Delhi", "Biochemical", name, specialization)


# In[171]:


def fetch_chemical_faculty(url, mycursor):
    '''
    fetches chemical department faculty and stores in mysql database
    '''
    soup = get_soup(url)
    data = soup.findAll('div', {'class' : 'each'})
    
    for i in range(0, len(data)):
        try:
            name = data[i].find('a').text.strip()
            specialization = data[i].find('div', {'class' : 'Research_div table_middle'}).find('div', {'class' : 'faculty_responsive_val'}).text.strip()
        except:
            continue
        
        insert_data_into_table(mycursor, "IIT Delhi", "Chemical", name, specialization)


# In[172]:


def fetch_chemistry_faculty(url, mycursor):
    '''
    fetches chemistry department faculty and stores in mysql database
    '''
    soup = get_soup(url)
    data = soup.findAll('div', {'class' : 'col-sm-12'})[1].findAll('div', {'class' : 'row'})
    
    for i in xrange(0, len(data), 2):
        try:
            name = data[i].find('h3').text.strip()
            specialization = data[i].findAll('p')[1].text.strip()
            specialization = re.sub('\s+',' ',specialization)
        except:
            continue
        
        insert_data_into_table(mycursor, "IIT Delhi", "Chemistry", name, specialization)


# In[173]:


def fetch_civil_faculty(url, mycursor):
    '''
    fetches civil department faculty and stores in mysql database
    '''
    soup = get_soup(url)
    data = soup.findAll('table')[1].findAll('tr')
    
    for i in range(0, len(data)):
        try:
            name = data[i].find('td').text.strip()
            data_text = data[i].find('p').text.strip()
            data_list = re.split('Interest', data_text)
            specialization = re.sub('\s+',' ',data_list[1])
        except:
            continue
        
        insert_data_into_table(mycursor, "IIT Delhi", "Civil", name, specialization)


# In[174]:


def fetch_cse_faculty(url, mycursor):
    '''
    fetches cse department faculty and stores in mysql database
    '''
    soup = get_soup(url)
    data = soup.findAll('table')[0].findAll('tr')
    
    for i in range(0, len(data)):
        try:
            name = data[i].find('a').text.strip()
            specialization = data[i].findAll('p')[1].text.strip()
        except:
            continue
        
        insert_data_into_table(mycursor, "IIT Delhi", "CSE", name, specialization)


# In[175]:


def fetch_electrical_faculty(url, mycursor):
    '''
    fetches electrical department faculty and stores in mysql database
    '''
    soup = get_soup(url)
    data = soup.find('table', {'class': 'contentarea'}).findAll('table')[1].findAll('tr')
    
    for i in range(0, len(data)):
        try:
            name = data[i].find('a').text.strip()
            data_text = data[i].text
            data_list = re.split('Area', data_text)
            specialization = re.sub('\s+',' ',data_list[1])
        except:
            continue
        
        insert_data_into_table(mycursor, "IIT Delhi", "Electrical", name, specialization)


# In[176]:


def fetch_maths_faculty(url, mycursor):
    '''
    fetches mathematics department faculty and stores in mysql database
    '''
    soup = get_soup(url)
    data = soup.find('table').findAll('tr')
    
    for i in range(0, len(data)):
        try:
            name = data[i].find('a').text.strip()
            data_text = data[i].findAll('p')[2].text.strip()
            data_list = re.split('interests', data_text)
            specialization = re.sub('\s+',' ',data_list[1])
        except:
            continue
        
        insert_data_into_table(mycursor, "IIT Delhi", "Mathematics", name, specialization)


# In[177]:


def fetch_textile_faculty(url, mycursor):
    '''
    fetches textile department faculty and stores in mysql database
    '''
    soup = get_soup(url)
    data = soup.findAll('div', {'class': 'col-sm-6'})
    
    for i in range(0, len(data)):
        try:
            name = data[i].find('div', {'class': 'faculty-list-name'}).text.strip()
            data_text = data[i].find('div', {'class': 'faculty-list-specilization'}).text.strip()
            data_list = re.split('Specialization', data_text)
            specialization = re.sub('\s+',' ',data_list[1])
        except:
            continue
        
        insert_data_into_table(mycursor, "IIT Delhi", "Textile", name, specialization)


# In[178]:


def fetch_machanics_faculty(url, mycursor):
    '''
    fetches machenics department faculty and stores in mysql database
    '''
    soup = get_soup(url)
    data = soup.find('div', {'class': 'view-content'}).findAll('table')
    
    for i in range(0, len(data)):
        try:
            name_list = data[i].findAll('td')[1].text.split(' ')
            name = name_list[0] + name_list[1]
            specialization = data[i].findAll('tr')[6].text.split('\n')[2]
        except:
            continue
        
        insert_data_into_table(mycursor, "IIT Delhi", "Machanics", name, specialization)


# In[179]:


def main():
    '''
    main function
    '''
    mydb = create_database_connection()
    mycursor = mydb.cursor()
    create_table(mycursor)
    
    fetch_biochem_faculty(biochem_url, mycursor)
    fetch_chemical_faculty(chem_url, mycursor)
    fetch_chemistry_faculty(chemistry_url, mycursor)
    fetch_civil_faculty(civil_url, mycursor)
    fetch_cse_faculty(cse_url, mycursor)
    fetch_electrical_faculty(electrical_url, mycursor)
    fetch_maths_faculty(maths_url, mycursor)
    fetch_textile_faculty(textile_url, mycursor)
    fetch_machanics_faculty(machanics_url, mycursor)
    
    mydb.commit()


# In[180]:


if __name__ == '__main__':
    main()


# In[ ]: