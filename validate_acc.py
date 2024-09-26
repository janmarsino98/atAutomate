import requests
from dotenv import load_dotenv
import os
import constants as c
from users import user_jan, user_ava
from lsitings import my_listings


load_dotenv()
proxy_cred = os.getenv("HTTP_PROXY")

proxy = {
    "http": f"http://{proxy_cred}",
    "https": f"http://{proxy_cred}",
}   


all_cookies = {
    "at_sid": user_ava.at_sid
}

payload = {
        "title":"Expert Resume Writing Services",
        "description":"Need a resume that stands out? My name is Ava, and with 3 years of experience working as a recruiter in Australia, I know exactly what it takes to create a resume that catches the eye of hiring managers and passes Applicant Tracking Systems (ATS). Whether you’re looking for roles in finance, education, healthcare, or any other field, I’ll craft a professional resume tailored to your needs and optimized for the Australian job market. Let’s work together to get you one step closer to your dream job!",
        "availability_description": "I am available at any time this listing is posted 😊",
        "location_type":{
            "type":"remote"
            },
        "category":"writing_translation|resume_writing",
        "welcome_message":"Thank you for you request! I will get back to you as soon as possible!",
        "packages":[{
            "name":"24-Hour Resume + Cover Letter Creation",
            "price":{"value_subunits":5000,"currency_code":"AUD"},
            "description":"In a hurry to apply? I offer a 24-hour service that delivers a professionally written, ATS-compliant resume, drawing from my 3 years of experience as an Australian recruiter. Your resume will be tailored to highlight your skills, achievements, and qualifications in a way that appeals to Australian recruiters and passes ATS systems. Perfect for those who need a quick and polished resume to make their next job move!"  
            },
            {
            "name":"24-Hour Non-Profit / NGO Resume + Cover Letter Package",
            "price":{"value_subunits":7000,"currency_code":"AUD"},
            "description":"Looking for a complete application package? With this 24-hour service, you’ll receive both a custom-written resume and a cover letter, ensuring your application stands out. With 3 years of recruiting experience in Australia, I know what employers are looking for and will tailor your documents to highlight your strengths. This package is perfect for anyone looking to make a strong impression with their job application!"  
            },
            ],
        "tags":[
    "Professional Resume Writing",
    "ATS-Compliant Resume",
    "Resume and Cover Letter Package",
    "Australian Job Market Resume",
    "Quick Resume Writing Service",
    "Resume for Australian Employers",
    "Experienced Recruiter Resume Service",
    "Resume Writing by Ava",
    "Resume Optimization",
    "Resume for All Industries",
    "Resume and Cover Letter Creation",
    "Custom Resume for Australian Jobs",
    "24-Hour Resume Service",
    "Resume Writing Expert in Australia",
    "Tailored Resume Writing"
],
        "attachments":[{"url":"https://listings-attachments.s3.ap-southeast-2.amazonaws.com/63b94cae-13bb-4ef3-8e85-23fc8fc12fd2.jpg"}]
}



accepted_payload = {
  "title": "Professional Finance Resume Writing Services",
  "description": "Looking to enhance your finance career? I offer professional ATS-compliant resume creation services tailored to the finance sector. Whether you're applying for roles in accounting, banking, or financial analysis, I’ll craft a resume that showcases your experience and qualifications, optimized to pass Applicant Tracking Systems and appeal to Australian recruiters. Let me help you stand out in the competitive finance job market!",
  "availability_description": "I am available at any time this listing is posted 😊",
  "location_type": {
    "type": "remote"
  },
  "category": "writing_translation|resume_writing",
  "welcome_message": "Thank you for your interest in my resume services! I'm excited to help you create an ATS-compliant, professionally optimized resume for the Australian job market. Your new resume will be delivered within 24 hours of confirming your booking. If you have any specific details or preferences you'd like me to include, feel free to share them with me. Looking forward to working with you!",
  "packages": [
    {
      "name": "24-Hour Health Resume Creation Package",
      "price": {
        "value_subunits": 5000,
        "currency_code": "AUD"
      },
      "description": "Need a healthcare resume in a hurry? I provide a fast, professional resume tailored specifically for health sector roles, delivered within 24 hours. Your resume will be ATS-compliant and optimized for healthcare positions in the Australian market, ensuring it highlights your expertise and qualifications effectively. Ideal for nurses, medical staff, and healthcare professionals looking to make an impact quickly."
    }
  ],
  "tags": [
    "Health Resume Writing"
  ],
  "attachments": [
    {
      "url": "https://listings-attachments.s3.ap-southeast-2.amazonaws.com/6bf1439f-1ca8-4d37-bd93-9c3621b73831.jpg"
    }
  ]
}

for _ in range(100):
    r = requests.post("https://www.airtasker.com/api/client/v1/listings", headers=c.HEADERS, json=payload, proxies=proxy, cookies=all_cookies)
    print(r.status_code, r.reason)
