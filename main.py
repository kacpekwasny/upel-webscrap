from constatns import LOGIN_URL_POST, LOGIN_URL_GET, ID_KURSU_Z_ANALIZY
from secrets import NUMER_INDEXU, HASLO
import requests
from bs4 import BeautifulSoup


def main():
    s = requests.session()
    login_page = s.get(LOGIN_URL_GET)

    # Find logintoken which is necesary to make a POST request and Log In
    soup = BeautifulSoup(login_page.content, "html.parser")
    login_div = soup.find(id="login")
    inputs = login_div.find_all("input")
    logintoken = inputs[1]["value"]

    data = {
    'anchor': '',
    'logintoken': logintoken,
    'username': NUMER_INDEXU,
    'password': HASLO,
    'rememberusername': '1'
    }
    login_post_page = s.post(LOGIN_URL_POST, data=data)

    params = (
        ('id', '1464'),
    )
    course_page = s.get('https://upel2.cel.agh.edu.pl/wiet/course/view.php', params=params)

    course = BeautifulSoup(course_page.content, "html.parser")
    online = course.find_all(class_="listentry")
    for user in online:
        if user.text == "Lech Adamus":
            print("Leszek jest online, jest nadzieja!")
        else:
            print("Jesteśmy zgubieni!")



if __name__ == "__main__":
    main()
