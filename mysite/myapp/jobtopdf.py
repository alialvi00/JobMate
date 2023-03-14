import json
from fpdf import FPDF
import difflib
from tika import parser
from base64 import b64encode
import requests
import os

pdf= FPDF()
pdf.add_page()
pdf1= FPDF()
pdf1.add_page()

def find_job(request):
    if request.method == 'POST':
        job_board = request.POST.get('job-board')
        if job_board == "Linkedin":
           return "mysite/myapp/scrapers/jsonOutputs/linkedin_jobs.json"
        elif job_board == "Glassdoor":
            return "mysite/myapp/scrapers/jsonOutputs/glassdoor_jobs.json"



def runscript():
    #Load the JSON data
    with open("mysite/myapp/scrapers/jsonOutputs/linkedin_jobs.json", 'r') as f:
        data = json.load(f)

    #load each job description
    jobs = data['Jobs']
    for i in range(10) : 
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Times", style='B', size=12)
        pdf.multi_cell(190, 10, json.dumps(jobs[i]["Job Details: "]) + "\n", align="L")
        pdf.output("mysite/myapp/static/jobdesc_pdf/linkedin-desc-job-"+str(i)+".pdf", "F")

    # Create PDF file with job descriptions
    #Job_Details_PDF = pdf.output("mysite/myapp/static/jobdesc_pdf/Job_Details_PDF.pdf/Job_Details_PDF.pdf")

   


def attach(i: int) -> str:
    runscript() 
     # Load the JSON data of the resume recieved
    with open("mysite/myapp/scrapers/jsonOutputs/resume_received.json", 'r') as g:
        data = json.load(g)

    # Load resume skills data 
    resume_skills = data["skills"]

    #create a json files for each 
    directory = "mysite/myapp/static/jobdesc_pdf"
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        with open(filepath, "rb") as f:
            contents = f.read()
            resume_b64 = b64encode(contents)
            r = requests.post('http://127.0.0.1:2000/sendResume', data=resume_b64)
        
            parsed_resume = requests.get('http://127.0.0.1:2000/receiveParsedData')

            parsed_data = parsed_resume.json()

            output_folder = "mysite/myapp/scrapers/jsonOutputs"
            output_filename = os.path.join(output_folder, filename + ".json")
            with open(output_filename, "w") as output_file:
                json.dump(parsed_data, output_file)
            #load the JSON data of the job descriptions 

    with open("mysite/myapp/scrapers/jsonOutputs/linkedin-desc-job-"+str(i)+".pdf"+".json", 'r') as e:
        response_data = json.load(e)

    # load job description skills from JSON 
    response_skills = response_data["skills"]

    diff = []
    count = 0 
    for skill in response_skills:
        if skill not in resume_skills:
            diff.append(skill)
        else:
            count = count + 1 
    ratio =  count/len(response_skills)*100
    output_string = "The ratio similarity bewteen you resume and job description {} is : {}\n".format(i+1, ratio)
    output_string += "Those are the skills you are missing: \n"
    output_string += "\n".join(diff)

    return output_string