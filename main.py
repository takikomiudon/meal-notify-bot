import requests
import schedule
import time
import os
from dotenv import load_dotenv

load_dotenv()

line_notify_token = os.getenv("LINE_NOTIFY_TOKEN")
line_notify_api = "https://notify-api.line.me/api/notify"

api_url = "https://gifukengakuryo.com/meal/check.php"
api_headers = {"Cookie": os.getenv("COOKIE")}

last_message = ""


def send_line_notify():
    global last_message

    api_response = requests.get(api_url, headers=api_headers).json()

    message = ""
    for data in api_response:
        message += "\n"
        message += (
            data["date"] + " 朝:" + str(data["m"]) + " 夕:" + str(data["e"])
        )

    if message == last_message:
        return

    last_message = message

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


send_line_notify()
schedule.every(1).minutes.do(send_line_notify)

while True:
    schedule.run_pending()
    time.sleep(1)
