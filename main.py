from constatns import LOGIN_URL, COURSE_ID
from secrets import USERNAME, PASSWORD
import requests
from bs4 import BeautifulSoup

def login(login_url, username, password):
    s = requests.session()
    login_page = s.get(login_url)

    # Find logintoken which is necesary to make a POST request and Log In
    soup = BeautifulSoup(login_page.content, "html.parser")
    login_div = soup.find(id="login")
    inputs = login_div.find_all("input")
    logintoken = inputs[1]["value"]

    data = {
    'anchor': '',
    'logintoken': logintoken,
    'username': username,
    'password': password,
    'rememberusername': '1'
    }
    s.post(LOGIN_URL, data=data)
    return s

def time_since_last_login(s, profile_url):
    """return time since last login as string"""
    profile_page = s.get(profile_url)
    profile = course = BeautifulSoup(profile_page.content, "html.parser")

    # find time since "Last access to site"
    last_activity = profile.find(id="region-main").find_all("div")[0].find_all("div")[0].find_all("div")[0].find_all("section")[3].find_all("div")[0].find_all("ul")[0].find_all("li")[1]
    return last_activity.text.split("(")[1].strip(")") # to pretty string

def less_than_5min(string):
    """return time since last access < 5 minutes"""

    if not "secs" in string:
        # So much time has passed that secs are irrelevant
        return False
    
    if not "mins" in string:
        # secs are relevant, but mins are not counted, so I gues it has been less than minute
        return True
    
    # Mins and secs are present. I guess that if hours were present secs would not be shown.
    mins, secs = string.split("mins")
    mins = mins.strip()
    secs = secs.strip().strip("secs")
    return 5*60 > int(mins)*60 + int(secs)

def main():
    s = login(LOGIN_URL, USERNAME, PASSWORD)  
    if less_than_5min(time_since_last_login(s, "https://upel2.cel.agh.edu.pl/wiet/user/profile.php?id=7838")):
        print("Leszek jest online, jest nadzieja!")
    else:
        print("O nie! Jesteśmy zgubieni!")



if __name__ == "__main__":
    main()
