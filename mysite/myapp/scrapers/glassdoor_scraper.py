import requests
from bs4 import BeautifulSoup as soup
import random
import json


def glassDoorScraper(country, city):
    # setting headers required for http requests
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 '
        'Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 '
        'Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile '
        'Safari/537.36 ']

    # randomizing the choice of header so glassdoor doesn't block requests
    user_agent = random.choice(user_agents)
    headers = {'User-Agent': user_agent}

    # retrieving designations from parsed user resume
    with open('myapp/scrapers/jsonOutputs/resume_received.json') as json_file:
        data = json.load(json_file)

    # constructing url
    glassdoor = "glassdoor.com/Job/jobs.htm?sc.keyword="
    keywords = data['designation']

    glassdoor += keywords[0] + "%20"

    url = glassdoor.replace(" ", "%20")
    html = requests.get(url)

    # create beautiful soup object for parsing html returned from requests
    bsobj = soup(html.content, "lxml")

    # retrieve all links in given beautiful soup object to parse
    job_links = bsobj.find_all("td", {"class": "job_title"})
    job_links = job_links[:10]

    joblist = []
    # parsing all the links for information
    for i in job_links:
        for a in i.find_all('a', href=True):
            joburl = ("https://glassdoor.com/" + a['href'])
            result = requests.get(joburl, headers=headers)
            job_bsobj = soup(result.content, "lxml")
            job_title = job_bsobj.findAll("div", {"class": "css-17x2pwl e11nt52q6"})[0].text
            employer_name = job_bsobj.find("div", {"data-test": "employer-name"}).text
            job_location = job_bsobj.find("div", {"class": "css-1v5elnn e11nt52q2"}).text
            job_details = job_bsobj.find("div", {"class": "desc css-58vpdc ecgq1xb5"}).text
            job = (employer_name, job_location, job_details, joburl)
            # writing all scraped information to json

            keys = ['Job Title:', 'Employer name: ', 'Job Location: ', 'Job Details: ', 'Link To Job: ']
            duplicates = []
            if job_details not in duplicates:
                duplicates.append(job_details)
                values = [job_title.replace("\n", "").strip(), employer_name.replace("\n", "").strip(),
                          job_location.replace("\n", "").strip(), job_details.replace("\n", "").strip(),
                          joburl.replace("\n", "").strip()]
                jobs = dict(zip(keys, values))
                joblist.append(jobs)

    top_level_data = {"Jobs": joblist}
    with open('myapp/scrapers/jsonOutputs/glassdoor_jobs.json', 'w') as outfile:
        json.dump(top_level_data, outfile, indent=4)
