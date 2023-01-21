import requests
from bs4 import BeautifulSoup as soup

import random
import json


def linkedInScraper(country, city):
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

    # retrieving designations from parsed user resume
    with open('myapp/scrapers/jsonOutputs/resume_received.json') as json_file:
        data = json.load(json_file)

    # constructing url
    linkedin = "http://www.linkedin.com/jobs/search?keywords="
    keywords = data['designation']

    linkedin += keywords[0] + "%20" + "&location=" + city + "+" + country
    # still need to add country and city

    # url below is for now, eventually update with user info in url request
    url = linkedin.replace(" ", "")
    html = requests.get(url)

    # create beautiful soup object for parsing html returned from requests
    bsobj = soup(html.content, "lxml")

    # retrieve all links in given beautiful soup object to parse
    job_links = bsobj.find_all("div", {"class": "base-card relative w-full hover:no-underline focus:no-underline "
                                                "base-card--link base-search-card base-search-card--link "
                                                "job-search-card"})
    joblist = []
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
    with open('myapp/scrapers/jsonOutputs/linkedin_jobs.json', 'w') as outfile:
        json.dump(top_level_data, outfile, indent=4)

