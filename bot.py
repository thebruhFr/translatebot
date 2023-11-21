import telebot
import requests
from googletrans import Translator
import datetime
import time
from ping import ping
from fake import fake_user_info
from bin import bin_lookup_handler
import re

translator = Translator()

BOT_TOKEN = '6951947854:AAGCqOrf-UKCXiANjHAHuF2m8YtYYGGTnd8'
owner = 'yooon_ah'

bot = telebot.TeleBot(BOT_TOKEN)

def get_daily_horoscope(sign: str, day: str) -> dict:
    """Get daily horoscope for a zodiac sign.
    Keyword arguments:
    sign:str - Zodiac sign
    day:str - Date in format (YYYY-MM-DD) OR TODAY OR TOMORROW OR YESTERDAY
    Return:dict - JSON data
    """
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign, "day": day}
    response = requests.get(url, params)

    return response.json()
    
@bot.message_handler(commands=['horoscope'])
def sign_handler(message):
    text = "What's your zodiac sign?\nChoose one: *Aries*, *Taurus*, *Gemini*, *Cancer,* *Leo*, *Virgo*, *Libra*, *Scorpio*, *Sagittarius*, *Capricorn*, *Aquarius*, and *Pisces*."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, day_handler)

def day_handler(message):
    sign = message.text
    text = "What day do you want to know?\nChoose one: *TODAY*, *TOMORROW*, *YESTERDAY*, or a date in format YYYY-MM-DD."
    sent_msg = bot.send_message(
        message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(
        sent_msg, fetch_horoscope, sign.capitalize())
        
def fetch_horoscope(message, sign):
    day = message.text
    horoscope = get_daily_horoscope(sign, day)
    data = horoscope["data"]
    horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\\n*Sign:* {sign}\\n*Day:* {data["date"]}'
    bot.send_message(message.chat.id, "Here's your horoscope!")
    bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=['translate'])
def perform_translation(message):
    try:
        command_parts = message.text.split(' ', 2)
        language_code = command_parts[1]

        if message.reply_to_message and message.reply_to_message.text:
            text_to_translate = message.reply_to_message.text
            translated_text = translator.translate(text_to_translate, dest=language_code)
            bot.send_message(message.chat.id, f"Translated text to {language_code}: {translated_text.text}")
        else:
            bot.send_message(message.chat.id, "<b>*Inviald Input*</b>", parse_mode="HTML")
    except Exception as e:
        bot.send_message(message.chat.id, "Oops! Something went wrong with the translation.")


        
@bot.message_handler(commands=['bin'])
def bin_command_handler(message):
    bin_lookup_handler(bot, message)  # Call the bin_lookup_handler function here passing the bot and message


def clean_and_format_card(card_entry):

    match = re.search(r"(\d{16})[:|\/\r\n\n ](\d{1,2})[:|\/\r\n\n ](\d{2,4})[:|\/\r\n\n ](\d{3,4})", card_entry)
    
    if match:
        cc = match.group(1)
        mes = match.group(2)
        ano = match.group(3)
        cvv = match.group(4)

        if len(mes) == 1:
            mes = "0" + mes
        if len(ano) == 2:
            ano = "20" + ano


        return f"Cleaned Card Information:\nCC: {cc}\nExpiration: {mes}/{ano}\nCVV: {cvv}"
    
    return "Couldn't extract valid card information."

@bot.message_handler(commands=['clean'])
def clean_card_handler(message):
    card_info = message.reply_to_message.text if message.reply_to_message else message.text.split(' ', 1)[1]
    cleaned_message = clean_and_format_card(card_info)
    
    bot.reply_to(message, f'<pre>{cleaned_message}</pre>', parse_mode="HTML")

@bot.message_handler(commands=['fake'])
def fake_command_handler(message):
    fake_user_info(bot, message)

@bot.message_handler(commands=['ping'])
def ping_command(message):
    ping(bot, message)

bot.launch_time = time.time()  

print('working')
bot.infinity_polling()
