import telebot
import requests
from googletrans import Translator

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
        text_to_translate = command_parts[2]

        translated_text = translator.translate(text_to_translate, dest=language_code)
        
        bot.send_message(message.chat.id, f"Translated text to {language_code}: {translated_text.text}")
    except Exception as e:
        bot.send_message(message.chat.id, "Oops! Something went wrong with the translation.")

def bin_lookup(bin_number):
    response = requests.get(bin_api_url + bin_number)

    if response.status_code == 200:
        return response.json()
    else:
        return None
        
@bot.message_handler(commands=['bin'])
def bin_lookup_handler(message):
    try:
        bin_number = message.text.split(' ', 1)[1][:6] 
        url = 'https://bins.antipublic.cc/bins/'
        response = requests.get(url + bin_number).json()

        if response:
            response_text = f"BIN Number: {response['bin']}\nBrand: {response['brand']}\nBank: {response['bank']}\nType: {response['type']}"
        else:
            response_text = "Sorry, couldn't find information for the provided BIN."

        bot.send_message(message.chat.id, response_text, reply_to_message_id=message.message_id)
    except Exception as e:
        bot.send_message(message.chat.id, "Oops! Something went wrong with the BIN lookup.")

print('bot is working')
bot.polling()
