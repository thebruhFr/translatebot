import datetime
import time

def ping(bot, message):
    start_time = time.time()
    bot_response = bot.send_message(message.chat.id, "Pinging...")
    end_time = time.time()

    response_time = round((end_time - start_time) * 1000, 2)

    current_time = datetime.datetime.now()
    uptime = current_time - datetime.datetime.fromtimestamp(bot.launch_time)

    bot.edit_message_text(
        f"Pong!🏓\nResponse Time: {response_time}ms\nBot Uptime: {uptime}",
        message.chat.id, bot_response.message_id)
  
