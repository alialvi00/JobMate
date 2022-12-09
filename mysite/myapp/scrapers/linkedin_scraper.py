import requests
from bs4 import BeautifulSoup as soup
import csv
import random

# Create a file called jobs.csv, create writer object to write to file, and set initial headers for csv file
file = open("jobs.csv", "w", newline="", encoding="utf-8")
writer = csv.writer(file)
initial_headers = ("Job Title", "Employer Name", "Job Location", "Job Details", "Job URL")
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
url = "https://ca.linkedin.com/jobs/search?keywords=software%20developer&location=Nepean%2C%20Ontario%2C%20Canada" \
      "&geoId=&trk=homepage-jobseeker_jobs-search-bar_search-submit&position=1&pageNum=0 "
html = requests.get(url)

# create beautiful soup object for parsing html returned from requests
bsobj = soup(html.content, "lxml")

# retrieve all links in given beautiful soup object to parse
job_links = bsobj.find_all("div", {"class": "base-card relative w-full hover:no-underline focus:no-underline "
                                            "base-card--link base-search-card base-search-card--link "
                                            "job-search-card"})

for i in job_links:
    for a in i.find_all('a', href=True):
        joburl = a['href']

        result = requests.get(joburl, headers=headers)
        if result.status_code == 200:
            job_bsobj = soup(result.content, "lxml")

            # job details fetch
            job_details = job_bsobj.find_all("div", {"class": "show-more-less-html__markup"})
            if len(job_details) > 0:
                job_details = job_details[0].text

            # employer name fetch
            employer_name = job_bsobj.find_all("a", {"class": "topcard__org-name-link topcard__flavor--black-link"})
            if len(employer_name) > 0:
                employer_name = employer_name[0].text

            # job location fetch
            job_location = job_bsobj.find("span", {"class": "topcard__flavor topcard__flavor--bullet"}).text

            # job title fetch
            job_title = job_bsobj.find("h1", {
                "class": "top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open "
                         "text-color-text mb-0 topcard__title"}).text

            # writing all scraped information to csv
            file = open("jobs.csv", "a", newline="")
            job = (employer_name, job_location, job_details, joburl)
            writer.writerow(job)
