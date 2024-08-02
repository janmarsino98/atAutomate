import requests
import pandas as pd
import constants as c



def run():
    d_tasks = {}
    link = "help-with-my-resume-x01j3ht5rt9k7npmgf1jqq9mya0"
    description = get_assigned_comment(link)
    
    print(description)
    # tasks = get_last_tasks_links()
    # for task in tasks:
    #     description = get_assigned_comment(task)
    #     d_tasks[task] = description
        
    # df = pd.DataFrame(list(d_tasks.items()), columns=["Task", "Description"])
    
    # df.to_excel("completed_tasks.xlsx")


def get_last_tasks_links():
    completed_tasks_url = "https://www.airtasker.com/api/v2/tasks?limit=300&path=tasks&threaded_comments=true&task_states=completed&after=0&search_term=resume&lat=-33.907256&lon=151.207706&location_name=Zetland%20NSW%2C%20Australia&task_types=both&radius=50000&carl_ids=&disable_recommendations=false&badges=&max_price=9999&min_price=5&sort_by=posted_desc&save_filters=true"
    
    response = requests.get(completed_tasks_url, c.HEADERS)
    
    if response.status_code != 200:
        return "The request was not successful!"
    
    data = response.json()
    
    links = []
    
    for task in data["tasks"]:
        links.append(task["slug"])
        
    return links

def get_assigned_comment(task_link):
    task_url = f"https://www.airtasker.com/api/v2/tasks/{task_link}/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Referer': 'https://www.airtasker.com/',
    }
    response = requests.get(task_url, headers=headers)
    print(response)
    
    if response.status_code != 200:
        return f"You were not able to request the task: {task_link}"
    
 
    data = response.json()
    
    for bid in data["bids"]:
        if bid["accepted"] == True:
            assigned_commment_id = bid["comment_id"]
            continue
        
    for comment in data["comments"]:
        if comment["id"] == assigned_commment_id:
            assigned_comment_description = comment["body"]
    
    return assigned_comment_description
            


if __name__ == "__main__":
    run()