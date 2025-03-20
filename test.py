# test.py
import requests

def get_val():
    url = "http://127.0.0.1:8000/token"
    data = {
        "username": "string-1",  # Must match a user in your DB
        "password": "string"  # Must match the plaintext password
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code == 400:
            print("page not found")
        if response.status_code == 200:
            print(response.json())
        else:
            print("Request failed or non-JSON response")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")


if __name__ == "__main__":
    get_val()
