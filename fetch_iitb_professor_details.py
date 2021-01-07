#!/usr/bin/env python
# coding: utf-8

# In[434]:


import json
import urllib
import requests
import mysql.connector
from bs4 import BeautifulSoup


# In[435]:

# iit bombay branch faculty url's
civil_url = "https://www.civil.iitb.ac.in/faculty"
ee_url = "https://www.ee.iitb.ac.in/web/people/faculty"
maths_url = "http://www.math.iitb.ac.in/People/faculty.php"
mech_url = "https://www.me.iitb.ac.in/?q=full-time-faculty"
metta_url = "https://www.iitb.ac.in/mems/en/people/faculty"
aero_url = "https://www.aero.iitb.ac.in/home/people/faculty"
chemical_url = "https://www.che.iitb.ac.in/faculty-directory"
environment_url = "http://www.esed.iitb.ac.in/faculty-directory"
cse_url = "https://www.cse.iitb.ac.in/~internal-live/api/faculty/?format=json"


# In[436]:


def create_database_connection():
	'''
	connection to mysql database
	'''
	mydb = mysql.connector.connect(
		host="127.0.0.1",
		user="root",
		password="Harshit77",
		database="NUTOM"
    )

	return mydb


# In[437]:


def get_soup(url):
	'''
	returns soup of website
	'''
	soup = None
	try:
		response = requests.get(url)
		data = response.text
		soup = BeautifulSoup(data, 'lxml')
	except Exception as e:
		print e

	return soup


# In[438]:


def get_json(url):
	'''
	returns json data fetched from website
	'''
	data = []
	try:
		response = urllib.urlopen(url)
		data = json.loads(response.read())
	except Exception as e:
		print e

	return data


# In[439]:


def create_table(mycursor):
	'''
	creates mysql table for faculty
	'''
	sql_query = "DROP TABLE IF EXISTS professor_data"
	mycursor.execute(sql_query)

	sql_query = "create table professor_data(college varchar(30) NOT NULL,department varchar(30) NOT NULL,name varchar(50) NOT NULL,specialization varchar(500));"
	mycursor.execute(sql_query)


# In[440]:


def insert_data_into_table(mycursor, college, department, professor_name, professor_specialization):
	'''
	inserts data into faculty table
	'''
	try:
		sql_query = "INSERT INTO professor_data (college, department, name, specialization) VALUES (%s, %s, %s, %s)"
		val = (college, department, professor_name, professor_specialization)
		mycursor.execute(sql_query, val)
	except Exception as e:
		print e


# In[441]:


def fetch_aero_faculty(url, mycursor):
	'''
	fetches aero department faculty and stores in mysql database
	'''
	soup = get_soup(url)
	data = soup.find('table', {'class' : 'views-table cols-5'}).findAll('tr')

	for i in range(1, len(data)):
		try:
			name = data[i].find('a').text.strip()
			specialization = data[i].findAll('td')[1].text.strip()
		except:
			continue

	insert_data_into_table(mycursor, "IIT Bombay", "Aerospace", name, specialization)


# In[442]:


def fetch_chemical_faculty(url, mycursor):
	'''
	fetches chemical department faculty and stores in mysql database
	'''
	soup = get_soup(url)
	data = soup.find('table', {'id' : 'datatable'}).findAll('tr')

	for i in range(1, len(data)):
		try:
			name = data[i].findAll('td')[1].text.strip()
			specialization = data[i].findAll('td')[2].text.strip()
		except:
			continue

		insert_data_into_table(mycursor, "IIT Bombay", "Chemical", name, specialization)


# In[443]:


def fetch_civil_faculty(url, mycursor):

	soup = get_soup(url)
	data = soup.findAll('div', {'class' : 'tr-section sec-faculty'})

	for i in range(1, len(data)):
		try:
			name = data[i].find('h1').text.strip()
			specialization = data[i].findAll('h4')[1].text.strip()
		except:
			continue

	insert_data_into_table(mycursor, "IIT Bombay", "Civil", name, specialization)


# In[444]:


def fetch_cse_faculty(url, mycursor):
	'''
	fetches cse department faculty and stores in mysql database
	'''
	data = get_json(url)

	for i in range(0, len(data)):
		try:
			name = data[i]['firstname']
			specialization = data[i]['interest']
		except:
			continue

	insert_data_into_table(mycursor, "IIT Bombay", "CSE", name, specialization)


# In[445]:


def fetch_electrical_faculty(url, mycursor):
	'''
	fetches electrical department faculty and stores in mysql database
	'''
	soup = get_soup(url)
	data = soup.findAll('ul', {'class' : 'facultyview'})[1].findAll('li')

	for i in range(0, len(data)):
		try:
			name = data[i].find('a').text.strip()
			specialization = data[i].find('li', {'class' : 'fac_ri'}).text.strip()
		except:
			continue

	insert_data_into_table(mycursor, "IIT Bombay", "Electrical", name, specialization)


# In[446]:


def fetch_environemnt_faculty(url, mycursor):
	'''
	fetches environment department faculty and stores in mysql database
	'''
	soup = get_soup(url)
	data = soup.find('table', {'id' : 'datatable'}).findAll('tr')

	for i in range(1, len(data)):
		try:
			name = data[i].findAll('td')[1].text.strip()
			specialization = data[i].findAll('td')[2].text.strip()
		except:
			continue

	insert_data_into_table(mycursor, "IIT Bombay", "Environemnt", name, specialization)


# In[447]:


def fetch_maths_faculty(url, mycursor):
	'''
	fetches mathematics department faculty and stores in mysql database
	'''
	soup = get_soup(url)
	data = soup.findAll('div', {'class' : 'row'})

	for i in range(1, len(data)-3):
		try:
			name = data[i].findAll('a')[0].text.strip()
			specialization = data[i].findAll('a')[1].text.strip()
		except:
			continue

	insert_data_into_table(mycursor, "IIT Bombay", "Mathematics", name, specialization)


# In[448]:


def fetch_mech_faculty(url, mycursor):
	'''
	fetches mechanical department faculty and stores in mysql database
	'''
	soup = get_soup(url)
	data = soup.find('table', {'class' : 'views-table cols-5'}).findAll('tr')

	for i in range(1, len(data)):
		try:
			name = data[i].findAll('td')[0].text.strip()
			specialization = data[i].findAll('td')[4].text.strip()
		except:
			continue

	insert_data_into_table(mycursor, "IIT Bombay", "Mechanical", name, specialization)


# In[449]:


def fetch_metta_faculty(url, mycursor):
	'''
	fetches metallurgy department faculty and stores in mysql database
	'''
	soup = get_soup(url)
	data = soup.findAll('table')[1].findAll('tr')

	for i in range(1, len(data)):
		try:
			name = data[i].findAll('span')[1].text.strip()
			specialization = data[i].findAll('span')[7].text.strip()
		except:
			continue

	insert_data_into_table(mycursor, "IIT Bombay", "Metallurgy", name, specialization)


# In[451]:


def main():
	'''
	main function
	'''
	mydb = create_database_connection()
	mycursor = mydb.cursor()

	create_table(mycursor)
	fetch_aero_faculty(aero_url, mycursor)
	fetch_civil_faculty(civil_url, mycursor)
	fetch_chemical_faculty(chemical_url, mycursor)
	fetch_cse_faculty(cse_url, mycursor)
	fetch_electrical_faculty(ee_url, mycursor)
	fetch_environemnt_faculty(environment_url, mycursor)
	fetch_maths_faculty(maths_url, mycursor)
	fetch_mech_faculty(mech_url, mycursor)
	fetch_metta_faculty(metta_url, mycursor)

	mydb.commit()

# In[452]:

if __name__ == '__main__':
	main()