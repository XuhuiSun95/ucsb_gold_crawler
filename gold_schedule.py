import sys
import getpass
import requests
from bs4 import BeautifulSoup

login_url = "https://my.sa.ucsb.edu/gold/Login.aspx"
url = "https://my.sa.ucsb.edu/gold/StudentSchedule.aspx"

def main():
    session_requests = requests.session()

    # Get login csrf token
    result = session_requests.get(login_url)
    plain_login = result.text
    soup = BeautifulSoup(plain_login, 'html.parser')

    # Create payload
    username = input("UCSB Net ID: \t")
    password = getpass.getpass("Password: \t")
    print("\n==============================")
    payload = {
        "__LASTFOCUS": "",
        "__VIEWSTATE": soup.find(id="__VIEWSTATE").get("value"),
        "__VIEWSTATEGENERATOR": soup.find(id="__VIEWSTATEGENERATOR").get("value"),
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__EVENTVALIDATION": soup.find(id="__EVENTVALIDATION").get("value"),
        "ctl00$pageContent$userNameText": username,
        "ctl00$pageContent$passwordText": password,
        "ctl00$pageContent$loginButton": "Login"
        }

    # Perform login
    source_code = session_requests.post(login_url, data = payload, headers = dict(referer = login_url))
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    if soup.find(string="Announcements") is None:
        sys.exit("Invalid UCSB NetID/Password combination")

    # Scrape url
    source_code = session_requests.get(url, headers = dict(referer = url))
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    for list in soup.find_all("div", class_="scheduleItem"):
        title = list.find("span")
        day = list.find(string="Days")
        print(title.string)
        print(day.next_element)

if __name__ == '__main__':
    main()
