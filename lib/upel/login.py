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
    resp = s.post(login_url, data=data)
    if "Invalid login" in resp.text:
        print("Failed login!", username, password)
        raise ValueError("Failed login! Invalid login, please try again.")
    return s
