from constatns import LOGIN_URL
from secrets import USERNAME, PASSWORD
from lib.upel import get_data, login, parse 

import json

def main():
    s = login.login(LOGIN_URL, USERNAME, PASSWORD)  
    time_str = get_data.time_since_last_login(s, 7838)
    print(f"{time_str} = {parse.string2secs(time_str)} secs")
    if parse.less_than_5min(time_str):
        print("Leszek jest online, jest nadzieja!")
    else:
        print("O nie! Jesteśmy zgubieni!")
    
    #grades = get_data.course_grades(s, 1099) # 1464 to jest id naszego kursu z analizy
    #print(json.dumps(parse.parse_grades(grades), indent=4))
    


if __name__ == "__main__":
    main()
