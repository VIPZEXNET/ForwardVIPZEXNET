from rubka import Robot
from rubka.context import Message
import os
import time

bot=Robot("")
USER_LOG_FILE="users.txt"
ADMINS=[""]
def log_user(user_id):
    if not os.path.exists(USER_LOG_FILE):
        open(USER_LOG_FILE,"w").close()
    with open(USER_LOG_FILE,"r+")as f:
        users=set(f.read().splitlines())
        if str(user_id)not in users:
            f.write(f"{user_id}\n")
def get_all_users():
    if os.path.exists(USER_LOG_FILE):
        with open(USER_LOG_FILE,"r")as f:
            return[uid.strip()for uid in f.readlines()if uid.strip()]
    return[]
@bot.on_message()
def handle_messages(bot:Robot,message:Message):
    user_id=message.chat_id
    log_user(user_id)
    if message.text and message.text.strip()=="/start":
        message.reply("API VIPZEXNET فعال شد")
        return
    if str(user_id)in ADMINS:
        send_to_all_users(bot,message)
def send_to_all_users(bot:Robot,message:Message):
    all_users=get_all_users()
    if not all_users:
        return
    users_to_send=[uid for uid in all_users if uid not in ADMINS]
    if not users_to_send:
        return
    total_users=len(users_to_send)
    progress_msg=message.reply(f"{total_users}")
    success=0
    failed=0
    for user_id in users_to_send:
        try:
            bot.forward_message(
                to_chat_id=user_id,
                message_id=message.message_id,
                from_chat_id=message.chat_id
            )
            success+=1
            time.sleep(0.2)
        except Exception:
            failed+=1
    progress_msg.edit(f"{success}/{failed}")
print('')
bot.run(