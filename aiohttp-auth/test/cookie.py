import requests


def main():
    # Do auth
    login = requests.get("http://127.0.0.1:8080/login?user=asdfsa&password=asdf")
    cookie = login.cookies

    r = requests.get("http://127.0.0.1:8080/admin", cookies=cookie)
    
    print(r.text)
    
if __name__ == '__main__':
    main()
