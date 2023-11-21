
import requests

def generate_fake_user(country_code):
    url = f'https://randomuser.me/api/1.2/?nat={country_code}'  # Construct the URL with the country code
    response = requests.get(url)

    if response.status_code == 200:
        fake_user = response.json()
        kk = response.text
        # Extract relevant information from the fake user data
        user_info = fake_user['results'][0]
        formatted_info = kk
        return formatted_info
    else:
        return "Sorry, couldn't generate fake user information for the provided country code."

def fake_user_info(bot, message):
    try:
        country_code = message.text.split(' ', 1)[1]  # Extract the country code from the command
        if not country_code:
            bot.send_message(message.chat.id, "Invalid country code. Please provide a valid country code.")
        else:
            fake_user_data = generate_fake_user(country_code)
            bot.send_message(message.chat.id, fake_user_data)
    except IndexError:
        bot.send_message(message.chat.id, "Invalid usage. Please use /fake {country_code} format.")
