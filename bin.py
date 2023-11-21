import requests

def bin_lookup_handler(bot, message):
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
