from os import stat
import telegram
import subprocess
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import json
import logging
from expiringdict import ExpiringDict

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


temp_flood_ban_list = ExpiringDict(max_len=100, max_age_seconds=60)

def entry(bot, update):
    try:
        # res = bot.send_message(chat_id="-1001164870268", text=json.dumps(update.to_dict(), indent=2))
        # print(json.dumps(update.to_dict(), indent=2))
        logging.info(update)
        pass
    except Exception as e:
        logging.error(e)
        # bot.send_message(chat_id="-1001164870268", text=str(e))
        pass
    if update.message and update.message.chat.id == -1001484296634:
        if update.message.reply_to_message and update.message.reply_to_message.forward_from_chat and update.message.reply_to_message.forward_from_chat.id == -1001180443770:
            try:
                personal_chat_id = update.message.reply_to_message.text.split("#q")[-1]
                thread_link = 't.me/covid19indiaorg_medhelpchat/'+str(update.message.reply_to_message.message_id)+'?comment='+str(update.message.message_id)
                bot.sendMessage(
                    chat_id=personal_chat_id,
                    text="There is a new comment to your query.\nPlease continue discussion here\n\n"+thread_link)
            except Exception as e:
                logging.error(e)
            return
        pass
    if update.message and update.message.text and update.message.chat.type == "private":
        matches = ["Age", "Gender"]
        if any(x in update.message.text for x in matches):
            # res = bot.forwardMessage(chat_id=-1001180443770, from_chat_id=update.message.chat.id, message_id=update.message.message_id)
            if not temp_flood_ban_list.get(update.message.chat.id):
                res = bot.sendMessage(chat_id=-1001180443770, text=update.message.text+"\n\n"+"from: "+update.message.chat.first_name+" #q"+str(update.message.chat.id))
                bot.sendMessage(chat_id=update.message.chat.id, text="Query posted: https://t.me/covid19indiaorg_medhelp/"+str(res['message_id'])+'\n\nI will notify you when a Doctor responds. If you have additional requests or information please share in this thread.')
                temp_flood_ban_list[update.message.chat.id] = True
            else:
                bot.sendMessage(chat_id=update.message.chat.id, text="Please wait a few minutes before posting your next query 🙏")
        else:
            bot.sendMessage(
                chat_id=update.message.chat_id, 
                text="""
Please copy the following template and send your queries in this format\.
You will be notified when a Doctor responds to your query\.

```
Age: 
Gender: 
Location: 
Covid Test Result: 
SpO2/Temperature: 
List of Complaints: 
Other Comments: 

```
""",
                parse_mode='MarkdownV2'
            )