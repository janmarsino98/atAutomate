import requests

url = "https://www.airtasker.com/api/v2/tasks?limit=50&path=tasks&threaded_comments=true&task_states=posted&after=0&task_types=online&radius=50000&carl_ids=&disable_recommendations=false&badges=&max_price=9999&min_price=5&sort_by=posted_desc&save_filters=true"


r = requests.get(url)

data = r.json()



