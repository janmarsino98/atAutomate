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

TARIFAS =  """ curriculum vitae: $30 \n 
cover letter or selection criteria: $30 \n curriculum vitae/resume and cover letter/seletion criteria: $50 \n 
linkedin profile update: $25 \n 
curriculum vitae cover letter and linkedin update: $80 \n 
HR advice: $75 \n 
job application help: $80 \n
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


GPT_SYSTEM_PROMPT = """Generate a professional response to apply for a task on Airtasker.

Start with exactly this text: Availability: Today · Tomorrow

The response should include the following paragraphs: 

1) A friendly and personalized greeting. 
2) A brief introduction highlighting over 10 years of experience in recruitment and HR management in Australia and focusing on how I am the perfect candidate for completing the task. 
3) If an industry is stated in the description you can for example say that you worked 10+ years a as a HR manager in that industry. 
Emphasize expertise in crafting professional and tailored resumes and cover letters, which are ATS compliant.
Reference perfect ratings and high customer satisfaction on Airtasker.
4) A polite and confident closing, encouraging the task poster to review your profile and consider your offer. 
Ensure the tone is professional, friendly, and focused on meeting the task poster's needs.

Separate the text in several paragraphs so it is easier to read.

Everything must be in plain text (don't use markup language!) and it should have no placeholders so it is totally ready to send.

The text must have around 65 words
My name is Jan and I am based in Australia. Unfortunately I can only communicate with customers thorugh email. You don't need to say that. I offer a reviewed version in less than 24 hours and I offer unlimited revisions until the customer is 100% satisfied."""


RESUME_TITLES = [
    "Crafting a Professional Resume",
    "Creating an Eye-Catching Resume",
    "Resume Building Basics",
    "Designing a Standout Resume",
    "Resume Writing for Job Seekers",
    "Building a Powerful Resume",
    "Creating a Winning Resume",
    "Optimizing Your Resume",
    "Professional Resume Writing Tips",
    "Effective Resume Creation Techniques",
    "Enhancing Your Resume",
    "Step-by-Step Resume Writing",
    "Innovative Resume Design",
    "Resume Writing Mastery",
    "Perfecting Your Resume Format",
    "Creating a Resume That Stands Out",
    "Professional Resume Tips and Tricks",
    "Resume Writing Strategies",
    "Essential Elements of a Strong Resume",
    "Resume Writing for Career Advancement"
]


RESUME_DESCRIPTIONS = [
    "Update my current resume with the latest job experience and skills to reflect my recent career growth.",
    "Rewrite my resume to highlight my leadership skills and managerial experience for a senior management role.",
    "Format my resume to ensure it is ATS-friendly, including appropriate keywords for the industry.",
    "Convert my resume into a creative template that stands out visually while maintaining professionalism.",
    "Tailor my resume to emphasize my technical skills and certifications for a position in IT.",
    "Create a one-page resume that concisely summarizes my qualifications for a fast-paced job application process.",
    "Revise my resume to focus on my achievements and quantifiable results in previous positions.",
    "Develop a targeted resume for a marketing role, highlighting my relevant experience and successful campaigns.",
    "Edit my resume to correct any grammar and spelling errors, ensuring it is error-free.",
    "Design a resume that incorporates my branding elements, such as a professional logo and consistent color scheme.",
    "Reorganize my resume to prioritize my most recent and relevant work experience for a job change.",
    "Generate a resume that includes a professional summary and key skills section at the top for quick scanning.",
    "Enhance my resume with action verbs and strong language to create a powerful impression.",
    "Adapt my resume for an international job application, ensuring it meets global standards.",
    "Integrate my LinkedIn profile information into my resume for a cohesive professional presence.",
    "Create a functional resume format that highlights my skills and abilities over chronological work history.",
    "Focus my resume on freelance and contract work, showcasing my flexibility and diverse project experience.",
    "Update my resume to include recent educational achievements and relevant coursework for a specialized position.",
    "Refine my resume to remove outdated or irrelevant information, ensuring it is up-to-date.",
    "Prepare a resume with a focus on my career objectives and how they align with the prospective employer’s goals."
]


CL_TITLES = [
    "Draft a General Cover Letter",
    "Customize Cover Letter for Specific Job",
    "Highlight Key Achievements in Cover Letter",
    "Write a Cover Letter for a Career Change",
    "Create an Entry-Level Cover Letter",
    "Develop a Cover Letter for Senior Position",
    "Format Cover Letter Professionally",
    "Revise Cover Letter for Grammar and Clarity",
    "Emphasize Soft Skills in Cover Letter",
    "Showcase Technical Skills in Cover Letter",
    "Craft a Cover Letter for Remote Jobs",
    "Write a Cover Letter for Internship",
    "Include Company Research in Cover Letter",
    "Address Employment Gaps in Cover Letter",
    "Tailor Cover Letter to Company Culture",
    "Highlight Transferable Skills in Cover Letter",
    "Create a Cover Letter for Referral",
    "Develop a Follow-Up Cover Letter",
    "Write a Cover Letter for Promotion",
    "Prepare a Cover Letter for Cold Applications"
]

CL_DESCRIPTIONS = [
    "Draft a general cover letter that can be customized for multiple job applications, focusing on key strengths and experience.",
    "Customize my cover letter to align with the specific job description and company values, highlighting relevant skills and achievements.",
    "Highlight key achievements in my cover letter to demonstrate my impact in previous roles and how I can bring similar success to the new position.",
    "Write a cover letter for a career change, emphasizing transferable skills and relevant experience from my previous industry.",
    "Create an entry-level cover letter that showcases my education, internships, and any volunteer work relevant to the position.",
    "Develop a cover letter for a senior position, focusing on my leadership experience, strategic thinking, and significant accomplishments.",
    "Format my cover letter professionally, ensuring it is visually appealing and follows standard business letter conventions.",
    "Revise my cover letter for grammar and clarity, making sure it is error-free and easy to read.",
    "Emphasize my soft skills in the cover letter, such as communication, teamwork, and problem-solving abilities.",
    "Showcase my technical skills in the cover letter, detailing specific software, tools, or methodologies I am proficient in.",
    "Craft a cover letter tailored for remote job applications, highlighting my ability to work independently and manage remote work challenges.",
    "Write a cover letter for an internship, focusing on my academic achievements, relevant coursework, and eagerness to learn.",
    "Include company research in my cover letter, demonstrating my knowledge of the company’s mission, values, and recent achievements.",
    "Address any employment gaps in my cover letter, explaining the circumstances and how I stayed productive during those periods.",
    "Tailor my cover letter to reflect the company culture, using language and examples that align with their values and work environment.",
    "Highlight transferable skills in my cover letter that are relevant to the new role, even if they were developed in a different industry.",
    "Create a cover letter for a job referral, mentioning the person who referred me and why I am a good fit for the position.",
    "Develop a follow-up cover letter to send after an interview, reiterating my interest in the position and addressing any points discussed.",
    "Write a cover letter for a promotion within the same company, emphasizing my achievements and readiness for increased responsibilities.",
    "Prepare a cover letter for cold applications, introducing myself and explaining why I am interested in potential opportunities with the company."
]
