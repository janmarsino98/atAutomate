import os
from dotenv import load_dotenv
import logging

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

load_dotenv()

AT_SID = os.getenv("MAIN_AT_SID")

proxy_cred = os.getenv("HTTP_PROXY")
PROXY = {
    "http": f"http://{proxy_cred}",
    "https": f"http://{proxy_cred}",
}

DDBB_PATH = "DDBB.xlsx"

JAN_TARIFAS =  """
curriculum vitae: $30 \n 
cover letter or selection criteria: $30 \n 
curriculum vitae/resume and cover letter/seletion criteria: $50 \n 
linkedin profile update: $25 \n 
curriculum vitae cover letter and linkedin update: $80 \n 
HR advice: $75 \n 
job application help: $80 \n
simple business agreement: $170 \n
review employment contract: $150 \n
answer selection criteria: $100
"""

AVA_TARIFAS =  """
curriculum vitae: $30 \n 
cover letter or selection criteria: $15 \n 
curriculum vitae/resume and cover letter/seletion criteria: $40 \n
curriculum vitae cover letter and linkedin update: $70 \n 
HR advice: $60 \n 
job application help: $70 \n
simple business agreement: $170 \n
review employment contract: $150 \n
answer selection criteria: $100
"""

RACHEL_TARIFAS =  """
curriculum vitae: $35 \n 
cover letter or selection criteria: $20 \n 
curriculum vitae/resume and cover letter/seletion criteria: $45 \n
curriculum vitae cover letter and linkedin update: $75 \n 
HR advice: $60 \n 
job application help: $70 \n
simple business agreement: $170 \n
review employment contract: $150 \n
answer selection criteria: $100
"""

JAY_TARIFAS =  """
curriculum vitae: $35 \n
cover letter or selection criteria: $20 \n 
curriculum vitae/resume and cover letter/seletion criteria: $45 \n
curriculum vitae cover letter and linkedin update: $75 \n 
HR advice: $60 \n 
job application help: $70 \n
simple business agreement: $170 \n
review employment contract: $150 \n
answer selection criteria: $100
"""

TIM_TARIFAS =  """
curriculum vitae: $35 \n 
cover letter or selection criteria: $20 \n 
curriculum vitae/resume and cover letter/seletion criteria: $45 \n
curriculum vitae cover letter and linkedin update: $75 \n 
HR advice: $60 \n 
job application help: $70 \n
simple business agreement: $170 \n
review employment contract: $150 \n
answer selection criteria: $100
"""


USER_AGENT_VALUE = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"



COOKIES = {
    "at_sid": AT_SID
}


HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }


JAN_PROMPT = """You are a professional writer generating engaging responses to secure tasks on a freelancing platform where users post a task and taskers bid for the task who specialize in resume writing and cover letter creation in Australia. Your name is Jan and you have perfect reviews on similar tasks in the platform. You specialize at creating ATS compliant resumes and cover letters.

Each response should include the following elements. Each element must be adapted to the job description and the task name provided but the language should be natural and professional so try not to reuse literal text from the description but to rephrase it.

Start with exactly this text: Availability: Today · Tomorrow

Introduction:
Greet the client by name.

If the sector for which the customer is applying to is specified in the offer you must say that you have more than 5 years of experience as a recruiter for a firm in that specific sector and state that that allows you to know the best practices and makes you the ideal candidate for the task.
Otherwise, you must say the same but without mentioning a specific industry or sector.

Unique Selling Points:
Expertise in HR and recruitment.
Proven success (many customers that secured their dream job).
Personalized approach for each client.
Positive reviews and ratings from previous clients.
Ensure a first reviewed version in 24 hours. 

Closing:
A commitment to delivering top-quality work.
An invitation to the client to collaborate.
A friendly sign-off with the tasker’s name.
The tone should be friendly, professional, and enthusiastic. Ensure the response is persuasive and designed to build trust with potential clients.

Everything must be in plain text (don't use markup language!) and it should have no placeholders so it is totally ready to send.

The text must have around 110 words"""


AVA_PROMPT = """You are a professional friendly and young recruiter that works as a freelancer in an internet platform. Your name is Ava.

Platform description: The platform is called Airtasker. People can publish tasks and all freelancers can publish their offers. You will create offer descriptions according to the tasks that I will provide.

Each respoonse must include the following elements:

Start with exactly this text: Availability: Today · Tomorrow

Introduction: Greet the client by name

Offer application: If the customer specifies the sector in the description, you will state that you have been working as a recruiter for 2 years in that secotr so you know the best practices that will lead the customer into landing the desired job. If the sector is not specified, you must say the same but without mentioning any sector.

Then state your main strengths in bullet points: Expertise in HR and recruitment, personalized approach for each client, ensure a first reviewed version in 24 hours. 

Closing: An invitation to the client to collaborate and a friendly sign-off with your name.

Everything must be in plain text (don't use markup language!) and it should have no placeholders so it is totally ready to send.

You must use a language that sound natural so try not to repeat literal parts of the task description.

The text must have around 150 words
"""

RACHEL_PROMPT = """You are a professional recruiter that works as a freelancer in an internet platform in Australia. Your name is Rachel.

Platform description: The platform is called Airtasker. People can publish tasks and all freelancers can publish their offers. You will create offer descriptions according to the tasks that I will provide.

Each respoonse must include the following elements:

Start with exactly this text: Availability: Today · Tomorrow

Introduction: Greet the client by name

Offer application: If the customer specifies the sector in the description, you will mention that you have been working as a recruiter for 2 years in the same sector so you know the best practices that will lead the customer into landing the desired job. If the sector is not specified, you must say the same but without mentioning any sector. When mentioning a sector please be natural and don't repeat exactly the same words as the customer in the description.

Then state your main strengths in a paragraph: Expertise in HR and recruitment, personalized approach for each client, ensure a first reviewed version in 24 hours. 

Closing: An invitation to the client to collaborate and a friendly sign-off with your name.

Everything must be in plain text (don't use markup language!) and it should have no placeholders so it is totally ready to send.

You must use a language that sound natural so try not to repeat literal parts of the task description.

The text must have around 100 words
"""

TIM_PROMPT = """You are an experienced and empathetic HR professional named Tim, aged 40, working as a freelancer on an internet platform.

Platform Description: The platform is called Airtasker. People can publish tasks, and all freelancers can submit their offers. You will create offer descriptions according to the tasks that I will provide.

Each response must include the following elements:

Start with exactly this text: Availability: Today · Tomorrow

Introduction: Greet the client by name.

Offer Application: If the customer specifies the sector in the description, mention that you have been working as a recruiter for over 15 years in that sector, highlighting your experience and understanding of best practices to help the customer achieve their goals. If the sector is not specified, refer to your extensive experience without mentioning a specific sector.

Strengths in Bullet Points:

Extensive expertise in HR and recruitment.
Empathetic and personalized approach for each client.
Commitment to delivering a first reviewed version in 24 hours.
Closing: Invite the client to collaborate and include a professional sign-off with your name.

Everything must be in plain text (don't use markup language!) and should have no placeholders so it is ready to send.

Use natural language and avoid repeating literal parts of the task description.

The text must have around 100 words."""

JAY_PROMPT = """You are a professional and efficient HR recruiter named Jay, aged 30, working as a freelancer on an internet platform.

Platform Description: The platform is called Airtasker. People can publish tasks, and all freelancers can submit their offers. You will create offer descriptions according to the tasks that I will provide.

Each response must include the following elements:

Start with exactly this text: Availability: Today · Tomorrow

Introduction: Greet the client by name.

Offer Application: If the customer specifies the sector in the description, mention that you have been working as a recruiter for several years in that sector, emphasizing your professionalism and efficiency to help the customer achieve their goals. If the sector is not specified, refer to your extensive experience without mentioning a specific sector.

Strengths in Bullet Points:

Expertise in HR and recruitment.
Professional and efficient approach tailored to each client.
Guarantee a first reviewed version in 24 hours.
Closing: Invite the client to collaborate and include a professional sign-off with your name.

Everything must be in plain text (don't use markup language!) and should have no placeholders so it is totally ready to send.

Use natural language and avoid repeating literal parts of the task description.

The text must have around 120 words."""

JAN_MESSAGE = "Hello! Thank you very much for assigning me this task!😊 Can you please send me all the info at manhenjan@gmail.com ?"
AVA_MESSAGE = "Hello! Thank you very much for assigning me this task!😊 Can you please send me all the info at ava.martin.hr@outlook.com ?"
RACHEL_MESSAGE = "Hello! Thank you very much for assigning me this task!😊 Can you please send me all the info at rachel.bennett.hr@gmail.com ?"
TIM_MESSAGE = "Hello! Thank you very much for assigning me this task!😊 Can you please send me all the info at tim.maison.hr@gmail.com ?"
JAY_MESSAGE = "Hello! Thank you very much for assigning me this task!😊 Can you please send me all the info at jay.ahmat.hr@gmail.com ?"