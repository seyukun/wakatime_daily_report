import requests
import datetime
import os

# 設定
WAKATIME_API_KEY = os.environ["WAKATIME_API_KEY"]
DISCORD_WEBHOOK_URL = os.os.environ["DISCORD_WEBHOOK_URL"]

def get_wakatime_summary():
    today = datetime.date.today()
    url = f"https://wakatime.com/api/v1/users/current/summaries"
    params = {
        "start": today,
        "end": today,
        "api_key": WAKATIME_API_KEY,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch WakaTime summary: {response.status_code}")
        return None

def send_to_discord(content):
    data = {"content": content}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("Message sent to Discord successfully!")
    else:
        print(f"Failed to send message to Discord: {response.status_code}")

def format_summary(summary):
    if not summary or "data" not in summary:
        return "No data available for today."
    
    data = summary["data"][0]  # 今日のデータ
    projects = data.get("projects", [])
    total_time = data.get("grand_total", {}).get("text", "0s")
    
    message = f"**WakaTime Daily Report**\n"
    message += f"Total Time: {total_time}\n\n"
    
    for project in projects:
        project_name = project.get("name", "Unknown")
        project_time = project.get("text", "0s")
        message += f"- {project_name}: {project_time}\n"
    
    return message

def main():
    summary = get_wakatime_summary()
    content = format_summary(summary)
    send_to_discord(content)

if __name__ == "__main__":
    main()

