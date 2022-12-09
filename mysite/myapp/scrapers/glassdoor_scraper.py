import requests
from bs4 import BeautifulSoup as soup
import csv
import random

# Create a file called jobs.csv, create writer object to write to file, and set initial headers for csv file
file = open("jobs.csv", "w", newline="", encoding="utf-8")
writer = csv.writer(file)
initial_headers = ("Employer Name", "Job Location", "Job Details", "Job URL")
writer.writerow(initial_headers)

# setting headers required for http requests
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 '
    'Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 '
    'Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile '
    'Safari/537.36 '
]

# randomizing the choice of header so glassdoor doesn't block requests
user_agent = random.choice(user_agents)
headers = {'User-Agent': user_agent}

# url below is for now, eventually update with user info in url request
url = "https://www.glassdoor.com/Job/ottawa-software-developer-jobs-SRCH_IL.0,6_IC2286068_KO7," \
      "25.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=software%2520developer "
html = requests.get(url)

# create beautiful soup object for parsing html returned from requests
bsobj = soup(html.content, "lxml")

# retrieve all links in given beautiful soup object to parse
job_links = bsobj.find_all("td", {"class": "job_title"})

# parsing all the links for information
for i in job_links:
    for a in i.find_all('a', href=True):
        joburl = ("https://glassdoor.com/" + a['href'])
        result = requests.get(joburl, headers=headers)
        job_bsobj = soup(result.content, "lxml")
        employer_name = job_bsobj.findAll("div", {"class": "css-16nw49e e11nt52q1"})[0].text
        job_location = job_bsobj.find("div", {"class": "css-1v5elnn e11nt52q2"}).text
        job_details = job_bsobj.find("div", {"class": "desc css-58vpdc ecgq1xb5"}).text
        file = open("jobs.csv", "a", newline="")
        job = (employer_name, job_location, job_details, joburl)

        # writing all scraped information to csv
        writer.writerow(job)
