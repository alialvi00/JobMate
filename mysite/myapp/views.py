import json
import os
import re

import language_tool_python
from bs4 import BeautifulSoup
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import login
from myapp.backends import login_backend
from base64 import b64encode
from .scrapers.linkedin_scraper import linkedInScraper as li
from .scrapers.glassdoor_scraper import glassDoorScraper as gs
import requests
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from PIL import Image
import fitz
# Create your views here.
# view class takes a request and returns a response (What an HTTP request would do)
# think of view class as a request handler
# action class


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('psw')

        user = login_backend.authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/homePage')
        else:
            messages.info(request, 'Username or Password is incorrect, please try again!')

    return render(request, 'login-page/login.html')


def signup_page(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.user_name = form.cleaned_data.get('user_name')
            user.email = form.cleaned_data.get('email')
            user.password = form.cleaned_data.get('password1')
            user.password2 = form.cleaned_data.get('password2')
            user.save()

            messages.success(request, 'Account has been successfully created for ' + user.user_name)
            return redirect('/loginPage')

    context = {'form': form}
    return render(request, 'signup/signup-page.html', context)


def redirect_home_page(request):
    return render(request, 'home-page/home-page.html')


def resume_upload(request):
    if request.method == 'POST':

        uploaded_resume = request.FILES['file-upload'].read()
        pdf_file = request.FILES['file-upload']
        file_name, file_extension = os.path.splitext(pdf_file.name)
        new_file_name = 'current_resume' + file_extension
        default_storage.save(new_file_name, pdf_file)
        resume_b64 = b64encode(uploaded_resume)
        r = requests.post('http://127.0.0.1:2000/sendResume', resume_b64)
        print(r.status_code, r.reason)

        parsed_resume = requests.get('http://127.0.0.1:2000/receiveParsedData')
        print(r.status_code, r.reason)

        # Use .json to read the json object
        print(parsed_resume.json())

        with open('myapp/scrapers/jsonOutputs/resume_received.json', 'w') as outfile:
            json.dump(parsed_resume.json(), outfile, indent=4)

        return redirect('/homePage')

    return render(request, 'resume-upload-page/resume-upload-page.html')


def find_job(request):
    if request.method == 'POST':
        country = request.POST.get('country')
        city = request.POST.get('city')
        job_board = request.POST.get('job-board')
        if job_board == "Linkedin":
            li(country, city)
            updateHTML("linkedin")
        elif job_board == "Glassdoor":
            gs(country, city)
            updateHTML("glassdoor")
        elif job_board == "Both":
            li(country, city)
            gs(country, city)
            updateHTML("both")
        return render(request, 'job-search-page/jobsearchpage_withjobs.html')

    return render(request, 'job-search-page/jobsearchpage.html')

def linkedInSearch(bsobj):
    with open("myapp/scrapers/jsonOutputs/linkedin_jobs.json", 'r') as f:
        data = json.load(f)
    for i in data["Jobs"]:
        joblistcontainer = bsobj.find(id="job-list-container")
        new_div = bsobj.new_tag("div")
        new_div["class"] = "job-listing"
        h2 = bsobj.new_tag("h2")
        jobtitle = i['Job Title:']
        h2.string = jobtitle
        new_div.append(h2)
        p1 = bsobj.new_tag("h2")
        employername = i['Employer name: ']
        p1.string = re.sub(r'[^\x00-\x7F]+', '', employername)
        new_div.append(p1)
        p2 = bsobj.new_tag("h2")
        joblocation = i['Job Location: ']
        p2.string = joblocation
        new_div.append(p2)
        new_div2 = bsobj.new_tag("div")
        new_div2["class"] = "job-description-container"
        new_div.append(new_div2)
        new_div3 = bsobj.new_tag("div")
        new_div3["class"] = "job-description"
        new_div2.append(new_div3)
        details = bsobj.new_tag("h4")
        jobdetails = i['Job Details: ']
        val = re.sub(r'[^\x00-\x7F]+', '', jobdetails)
        details.string = val
        new_div3.append(details)
        joblink = i['Link To Job: ']
        new_a = bsobj.new_tag("a", href=joblink)
        new_a.string = "View Job"
        new_div3.append(new_a)
        joblistcontainer.append(new_div)
        bsobj.body.append(joblistcontainer)
    with open("myapp/templates/job-search-page/jobsearchpage_withjobs.html", "w") as file:
        file.write(str(bsobj))

def glassdoorSearch(bsobj):
    with open("myapp/scrapers/jsonOutputs/glassdoor_jobs.json", 'r') as f:
        data = json.load(f)
        if (len(data["Jobs"]) != 0):
            for i in data["Jobs"]:
                joblistcontainer = bsobj.find(id="job-list-container")
                new_div = bsobj.new_tag("div")
                new_div["class"] = "job-listing"
                h2 = bsobj.new_tag("h2")
                jobtitle = i['Job Title:']
                h2.string = jobtitle
                new_div.append(h2)
                p1 = bsobj.new_tag("h2")
                employername = i['Employer name: ']
                p1.string = re.sub(r'[^\x00-\x7F]+', '', employername)
                new_div.append(p1)
                p2 = bsobj.new_tag("h2")
                joblocation = i['Job Location: ']
                p2.string = joblocation
                new_div.append(p2)
                new_div2 = bsobj.new_tag("div")
                new_div2["class"] = "job-description-container"
                new_div.append(new_div2)
                new_div3 = bsobj.new_tag("div")
                new_div3["class"] = "job-description"
                new_div2.append(new_div3)
                details = bsobj.new_tag("h4")
                jobdetails = i['Job Details: ']
                val = re.sub(r'[^\x00-\x7F]+', '', jobdetails)
                details.string = val
                new_div3.append(details)
                joblink = i['Link To Job: ']
                new_a = bsobj.new_tag("a", href=joblink)
                new_a.string = "View Job"
                new_div3.append(new_a)
                joblistcontainer.append(new_div)
                bsobj.body.append(joblistcontainer)
        with open("myapp/templates/job-search-page/jobsearchpage_withjobs.html", "w") as file:
            file.write(str(bsobj))

def bothSearch(bsobj):
    with open("myapp/scrapers/jsonOutputs/linkedin_jobs.json", 'r') as f:
        data = json.load(f)
    for i in data["Jobs"]:
        joblistcontainer = bsobj.find(id="job-list-container")
        new_div = bsobj.new_tag("div")
        new_div["class"] = "job-listing"
        h2 = bsobj.new_tag("h2")
        jobtitle = i['Job Title:']
        h2.string = jobtitle
        new_div.append(h2)
        p1 = bsobj.new_tag("h2")
        employername = i['Employer name: ']
        p1.string = re.sub(r'[^\x00-\x7F]+', '', employername)
        new_div.append(p1)
        p2 = bsobj.new_tag("h2")
        joblocation = i['Job Location: ']
        p2.string = joblocation
        new_div.append(p2)
        new_div2 = bsobj.new_tag("div")
        new_div2["class"] = "job-description-container"
        new_div.append(new_div2)
        new_div3 = bsobj.new_tag("div")
        new_div3["class"] = "job-description"
        new_div2.append(new_div3)
        details = bsobj.new_tag("h4")
        jobdetails = i['Job Details: ']
        val = re.sub(r'[^\x00-\x7F]+', '', jobdetails)
        details.string = val
        new_div3.append(details)
        joblink = i['Link To Job: ']
        new_a = bsobj.new_tag("a", href=joblink)
        new_a.string = "View Job"
        new_div3.append(new_a)
        joblistcontainer.append(new_div)
        bsobj.body.append(joblistcontainer)
    with open("myapp/scrapers/jsonOutputs/glassdoor_jobs.json", 'r') as f:
        data = json.load(f)
        if (len(data["Jobs"]) != 0):
            for i in data["Jobs"]:
                joblistcontainer = bsobj.find(id="job-list-container")
                new_div = bsobj.new_tag("div")
                new_div["class"] = "job-listing"
                h2 = bsobj.new_tag("h2")
                jobtitle = i['Job Title:']
                h2.string = jobtitle
                new_div.append(h2)
                p1 = bsobj.new_tag("h2")
                employername = i['Employer name: ']
                p1.string = re.sub(r'[^\x00-\x7F]+', '', employername)
                new_div.append(p1)
                p2 = bsobj.new_tag("h2")
                joblocation = i['Job Location: ']
                p2.string = joblocation
                new_div.append(p2)
                new_div2 = bsobj.new_tag("div")
                new_div2["class"] = "job-description-container"
                new_div.append(new_div2)
                new_div3 = bsobj.new_tag("div")
                new_div3["class"] = "job-description"
                new_div2.append(new_div3)
                details = bsobj.new_tag("h4")
                jobdetails = i['Job Details: ']
                val = re.sub(r'[^\x00-\x7F]+', '', jobdetails)
                details.string = val
                new_div3.append(details)
                joblink = i['Link To Job: ']
                new_a = bsobj.new_tag("a", href=joblink)
                new_a.string = "View Job"
                new_div3.append(new_a)
                joblistcontainer.append(new_div)
                bsobj.body.append(joblistcontainer)
    with open("myapp/templates/job-search-page/jobsearchpage_withjobs.html", "w") as file:
        file.write(str(bsobj))
def updateHTML(jobsFile):
    with open("myapp/templates/job-search-page/jobsearchpage.html", "r") as file:
        bsobj = (BeautifulSoup(file, "html.parser"))
        if jobsFile=="linkedin":
            linkedInSearch(bsobj)
        if jobsFile=="glassdoor":
            glassdoorSearch(bsobj)
        if jobsFile == "both":
            bothSearch(bsobj)


def rate_resume(request):
    # image = Image.open('current_resume.pdf')
    # image.save('preview.png', 'PNG')
    doc = fitz.open('media/current_resume.pdf')
    text = ""
    for page in doc:
        text += page.get_text()
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(text)
    with open("myapp/templates/rate-resume/rate-resume.html", "r") as thisFile:
        soup = BeautifulSoup(thisFile, "html.parser")
        container = soup.find("div", class_="container")
        table = soup.new_tag("table", id="my-table")
        tr1 = soup.new_tag("tr")
        td1_1 = soup.new_tag("td")
        td1_1.string = "Type of Potential Issue"
        td1_2 = soup.new_tag("td")
        td1_2.string = "Line to Check"
        td1_3 = soup.new_tag("td")
        td1_3.string = "Suggestions"
        tr1.append(td1_1)
        tr1.append(td1_2)
        tr1.append(td1_3)
        table.append(tr1)
        for match in matches:
            if(match.ruleIssueType != "whitespace"):
                new_row = soup.new_tag("tr")
                tdType = soup.new_tag("td")
                tdLine = soup.new_tag("td")
                tdSuggestion = soup.new_tag("td")
                tdType.string = match.message
                str_en = match.context.encode("ascii", "ignore")
                str_de = str_en.decode()
                tdLine.string = str_de
                tdSuggestion.string = match.replacements[0]
                new_row.append(tdType)
                new_row.append(tdLine)
                new_row.append(tdSuggestion)
                table.append(new_row)
            container.append(table)

        with open("myapp/templates/rate-resume/rate-resume-with-issues.html", "w") as finalFile:
            finalFile.write(str(soup))
    return render(request, 'rate-resume/rate-resume-with-issues.html')
