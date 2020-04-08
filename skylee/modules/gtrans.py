from typing import Optional, List
from gtts import gTTS
from datetime import datetime
import re

from telegram import ChatAction
from telegram import Message, Update, Bot, User
from telegram import MessageEntity
from telegram.ext import Filters, MessageHandler, run_async

from skylee import dispatcher, LOGGER
from skylee.modules.disable import DisableAbleCommandHandler

from googletrans import Translator

#Translator based on google translate API

@run_async
def gtrans(update, context):
    args = context.args
    oky = " ".join(args)
    lol = update.effective_message
    to_translate_text = lol.reply_to_message.text
    translator = Translator()
    try:
        translated = translator.translate(to_translate_text, dest=oky)
        oof = translated.src
        results = translated.text
        lol.reply_text("Translated from {} to {}.\n {}".format(oof, oky, results))
    except :
        lol.reply_text("Error! text might have emojis or invalid language code.")


def gtts(update, context):
    current_time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
    filename = datetime.now().strftime("%d%m%y-%H%M%S%f")
    try:
        reply = update.effective_message.reply_to_message.text
        update.message.chat.send_action(ChatAction.RECORD_AUDIO)
        tts = gTTS(reply)
        tts.save("skylee.mp3")
        with open("skylee.mp3", "rb") as x:
            linelist = list(x)
            linecount = len(linelist)
        if linecount == 1:
            update.message.chat.send_action(ChatAction.RECORD_AUDIO)
            tts = gTTS(reply)
            tts.save("skylee.mp3")
        with open("skylee.mp3", "rb") as speech:
            update.message.reply_voice(speech, quote=False)
    except :
        args = context.args
        reply = " ".join(args)
        update.message.chat.send_action(ChatAction.RECORD_AUDIO)
        tts = gTTS(reply)
        tts.save("skylee.mp3")
        with open("skylee.mp3", "rb") as x:
            linelist = list(x)
            linecount = len(linelist)
        if linecount == 1:
            update.message.chat.send_action(ChatAction.RECORD_AUDIO)
            tts = gTTS(reply)
            tts.save("skylee.mp3")
        with open("skylee.mp3", "rb") as speech:
            update.message.reply_voice(speech, quote=False)



__help__ = """
- /tr <lang> - To translate to your language!
- /tts <reply> - To some message to convert it into audio format! 
"""
__mod_name__ = "Translate"

dispatcher.add_handler(DisableAbleCommandHandler("tr", gtrans, pass_args=True))
dispatcher.add_handler(DisableAbleCommandHandler("tts", gtts, pass_args=True))