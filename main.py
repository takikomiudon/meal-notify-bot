import requests
import os
from dotenv import load_dotenv

load_dotenv()

line_notify_token = os.getenv("LINE_NOTIFY_TOKEN")
line_notify_api = "https://notify-api.line.me/api/notify"

api_url = "https://gifukengakuryo.com/meal/check.php"
api_headers = {"Cookie": os.getenv("COOKIE")}

last_message_file = "last_message.txt"


def get_last_message():
    if os.path.exists(last_message_file):
        with open(last_message_file, "r") as file:
            return file.read()
    return ""


def save_last_message(message):
    with open(last_message_file, "w") as file:
        file.write(message)


def get_new_message():
    api_response = requests.get(api_url, headers=api_headers)
    print(api_response.status_code)
    api_response = api_response.json()

    message = ""
    for data in api_response:
        message += (
            "\n" + data["date"] + " 朝:" + str(data["m"]) + " 夕:" + str(data["e"])
        )

    return message


def send_line_notify(message):
    payload = {"message": message}
    headers = {"Authorization": "Bearer " + line_notify_token}

    line_response = requests.post(
        line_notify_api, data=payload, headers=headers
    )

    if line_response.status_code == 200:
        print("メッセージが正常に送信されました！")
    else:
        print(
            "メッセージ送信に失敗しました。ステータスコード:", line_response.status_code
        )


last_message = get_last_message()
new_message = get_new_message()

if new_message != last_message:
    send_line_notify(new_message)
    save_last_message(new_message)
