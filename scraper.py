import pymongo
import requests
from bs4 import BeautifulSoup


MONGO_URI = "mongodb+srv://Database2026:Project2026@cluster0.5r3zyak.mongodb.net/?appName=Cluster0"

client = pymongo.MongoClient(MONGO_URI)
db = client["ProjectDB"]
collection = db["Papers"]

def check_project_title(title):
    
    existing_paper = collection.find_one({"title": title.lower()})
    if existing_paper:
        return "This name is already taken. Please choose another one."
    
    #
    print("\nSearching the website... Please Wait...\n")
    search_query = title.replace(' ', '+')
    url = f"https://arxiv.org/search/?query={search_query}&searchtype=title&order=-announced_date_first&size=50"
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # For results
        results = soup.find_all('li', class_='arxiv-result')
        name_taken = False
        
        # Filter (2023, 2024, 2025, 2026)
        for result in results:
            date_tag = result.find('p', class_='is-size-7')
            if date_tag:
                date_text = date_tag.text.strip()
                if any(year in date_text for year in ["2023", "2024", "2025", "2026"]):
                    name_taken = True
                    break
                    
        # Saving Final result in DB
        if name_taken:
            collection.insert_one({"title": title.lower(), "status": "taken"})
            return "This name is already taken in the last 4 years. Please choose another one."
        else:
            collection.insert_one({"title": title.lower(), "status": "available"})
            return "This title is available! You can proceed with your project."
            
    except Exception as e:
        return "Error connecting to the website. Please try again."

# For Taking user Input
#user_title = input("Enter the Project Title to checkp: ")
#bot_reply = check_project_title(user_title)

#print("\nBot Reply:", bot_reply)