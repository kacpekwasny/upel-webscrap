from multiprocessing.sharedctypes import Value
from bs4 import BeautifulSoup

def get_user_profile_data(s, profile_id):
    """
    return {
        "username": "Sir Timothy",
        "since_last_login": "13 hours 44 mins",
    }
    """
    profile_page = s.get(f"https://upel2.cel.agh.edu.pl/wiet/user/profile.php?id={profile_id}")
    profile = BeautifulSoup(profile_page.content, "html.parser")

    # find time since "Last access to site"
    try:
        last_activity = profile.find(id="region-main").find("div").find("div").find("div").find_all("section")[3].find("div").find("ul").find_all("li")[1]
        last_activity_string = last_activity.text.split("(")[1].strip(")") # to pretty string, ex.: 15 mins 12 secs
    except IndexError:
        # if one is trying to follow himself
        try:
            last_activity = profile.find(id="region-main").find("div").find("div").find("div").find_all("section")[4].find("div").find("ul").find_all("li")[1]
            last_activity_string = last_activity.text.split("(")[1].strip(")") # to pretty string, ex.: 15 mins 12 secs
        except IndexError:
            might = "" if "invalid user" in profile.text.lower() else "might"
            print(last_activity.text)
            raise ValueError(f"Error when parsing retrived page. You {might} have passed a wrong profile_id: {profile_id}")
    
    try:
        # username is the only <h1> on that page
        username_string = profile.find("h1").text
    except:
        raise ValueError(f"Error when parsing retrived page. You {might} have passed a wrong profile_id: {profile_id}")

    return {
        "username": username_string,
        "since_last_login": last_activity_string,
    }


def time_since_last_login(s, profile_id):
    """return time since last login as string
    example: 14 hours 21 mins"""

    return get_user_profile_data(s, profile_id)["since_last_login"]


def course_grades(s, course_id):
    course_page = s.get(f"https://upel2.cel.agh.edu.pl/wiet/grade/report/user/index.php?id={course_id}")
    course = BeautifulSoup(course_page.content, "html.parser")
    grades_table = course.find(id="region-main").find("div").find("table")
    return grades_table
