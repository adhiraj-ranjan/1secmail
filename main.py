import json
import requests
import time

def get_domains():
    response = requests.get("https://www.1secmail.com/api/v1/?action=getDomainList")
    return response.json()

def validate_domain():
    domains = get_domains()
    print(f"Default domain [ {domains[0]} ]")
    res = input("Change domain ? ( Y for yes ) : ").lower()
    if res == "y":
        print("\nChoose from list of domains...")
        for index, domain in enumerate(domains):
            print(f"[ {index} ] {domain}")
        
        while True:
            try:
                d_index = int(input("Enter > "))
                return domains[d_index]
            except:
                print("Not a valid input... Try again")
    else:
        return domains[0]


def generate_random():
    response = requests.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1').json()
    print(f"\n[ info ] Your Temporary Email Address : {response[0]}")
    print("[ info ] Waiting for messages...")

    username, domain = response[0].split('@')[0], response[0].split('@')[1]
    email_count = 1
    len_res = 0
    while True:
        response_m = requests.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}").json()
        if len(response_m) > len_res:
            print("\n")
            print(f"------------------------------{email_count}-------------------------------")
            email_count += 1
            len_res += 1
            read_m = requests.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain={domain}&id={response_m[0]['id']}")
            for r in read_m.json().keys():
                print(f"{r} - {read_m.json()[r]}")
        
        time.sleep(2)

def generate_custom(username):
    domain = validate_domain()
    print(f"\n[ info ] Your Temporary Email Address : {username}@{domain}")
    print("[ info ] Waiting for messages...")

    email_count = 1
    len_res = 0
    while True:
        response_m = requests.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}").json()
        if len(response_m) > len_res:
            print("\n")
            print(f"------------------------------{email_count}-------------------------------")
            email_count += 1
            len_res += 1
            read_m = requests.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain={domain}&id={response_m[0]['id']}")
            for r in read_m.json().keys():
                print(f"{r} - {read_m.json()[r]}")
        
        time.sleep(2)


def user_input():
    i = input("Generate Random Mail Address ( N for Custom ) : ").lower()
    if i == "n":
        custom_mail = input("Enter the address : ").lower()
        try:
            generate_custom(custom_mail)
        except KeyboardInterrupt:
            print("Keyboard Interrupt, Exiting...")
    else:
        try:
            generate_random()
        except KeyboardInterrupt:
            print("Keyboard Interrupt, Exiting...")

user_input()
