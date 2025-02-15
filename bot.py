import telebot
import requests
import time  
import re  

# Your Telegram Bot Token
BOT_TOKEN = "5909441299:AAEv7WSNh2lrRFTa7gAhH9x8wzOembjmD94"
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")  

# Free Dictionary API URL
DICTIONARY_API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

# Function to get word definition
def get_definition(word):
    response = requests.get(DICTIONARY_API_URL + word)
    if response.status_code == 200:
        data = response.json()
        
        # Extract meaning and part of speech
        part_of_speech = data[0]['meanings'][0]['partOfSpeech'].capitalize()
        meaning = data[0]['meanings'][0]['definitions'][0]['definition']
        
        return part_of_speech, meaning
    return None, None

# Add buttons for the 12 channels (with links)
def create_inline_button():
    keyboard = telebot.types.InlineKeyboardMarkup()
    
    button_channel_1 = telebot.types.InlineKeyboardButton(
        text="Writing", url="https://t.me/neo_writing"
    )
    button_channel_2 = telebot.types.InlineKeyboardButton(
        text="Listening", url="https://t.me/tpo_listening1"
    )
    button_channel_3 = telebot.types.InlineKeyboardButton(
        text="Speaking", url="https://t.me/+lWir8Hu6css5MGQ1"
    )
    button_channel_4 = telebot.types.InlineKeyboardButton(
        text="Resources", url="https://t.me/+gPhXbnd49yk0NTI1"
    )
    button_channel_5 = telebot.types.InlineKeyboardButton(
        text="YouTube Vocab", url="https://t.me/+oGceYYJCwrZjNDk9"
    )
    button_channel_6 = telebot.types.InlineKeyboardButton(
        text="Ketab", url="https://t.me/ketab_pdfs"
    )
    button_channel_7 = telebot.types.InlineKeyboardButton(
        text="TED Talks", url="https://t.me/moha_ted"
    )
    button_channel_8 = telebot.types.InlineKeyboardButton(
        text="4000 Words", url="https://t.me/+bz-2dmJTxTowZGZl"
    )
    button_channel_9 = telebot.types.InlineKeyboardButton(
        text="Extensive Reading", url="https://t.me/+OCr_ZwPHbCo4ZWM1"
    )

    # Add the buttons to the keyboard, 3 buttons in one row, 3 in the next row
    keyboard.row(button_channel_1, button_channel_2, button_channel_3)
    keyboard.row(button_channel_4, button_channel_5, button_channel_6)
    keyboard.row(button_channel_7, button_channel_8, button_channel_9)
    
    return keyboard

# Function to clean words (remove numbers like "1." or standalone numbers)
def clean_words(input_text):
    words = input_text.replace("\n", ",").split(",")  
    cleaned_words = []
    
    for word in words:
        word = re.sub(r'^\d+\.?', '', word).strip().lower()  # Remove leading numbers and dots
        if word and not re.search(r'\d', word):  # Ensure it doesn't contain other numbers
            cleaned_words.append(word)
    
    return cleaned_words

# Start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Send the welcome message with inline buttons
    bot.reply_to(
    message, 
    """🚀 𝚆𝚎𝚕𝚌𝚘𝚖𝚎 𝚝𝚘 𝚢𝚘𝚞𝚛 𝚞𝚕𝚝𝚒𝚖𝚊𝚝𝚎 𝙳𝚒𝚌𝚝𝚒𝚘𝚗𝚊𝚛𝚢 𝙱𝚘𝚝! 📚🔍
    𝙴𝚡𝚌𝚒𝚝𝚎𝚍 𝚝𝚘 𝚍𝚒𝚟𝚎 𝚒𝚗𝚝𝚘 𝚝𝚑𝚎 𝚎𝚗𝚌𝚑𝚊𝚗𝚝𝚒𝚗𝚐 𝚠𝚘𝚛𝚕𝚍 𝚘𝚏 𝚠𝚘𝚛𝚍𝚜? 🌍✨ 

  🏆 𝗧𝗿𝘆 𝘀𝗲𝗮𝗿𝗰𝗵𝗶𝗻𝗴 𝗳𝗼𝗿 𝗮𝗻𝘆 𝘄𝗼𝗿𝗱 𝗻𝗼𝘄!
📌 join: <a href="https://t.me/+ojJjzjv3CBEyOWZl">𝑬𝒍𝒊𝒕𝒆 𝑻𝑶𝑬𝑭𝑳 𝑨𝒄𝒂𝒅𝒆𝒎𝒚 | 𝚅𝚘𝚌𝚊𝚋𝚞𝚕𝚊𝚛𝚢</a>""",
    parse_mode="HTML",
    reply_markup=create_inline_button()
    )

# Handle words input
@bot.message_handler(func=lambda message: True)
def handle_word(message):
    words = clean_words(message.text)  

    if not words:
        bot.reply_to(message, "❌ <b>Please enter at least one valid word.</b>", parse_mode="HTML")
        return

    for word in words:
        part_of_speech, meaning = get_definition(word)

        if meaning:
            reply_text = f"""
📖 <b>Word:</b> <code>{word}</code>
📌 <b>Part of Speech:</b> <i>{part_of_speech}</i>
📝 <b>Meaning:</b> <code>{meaning}</code>
━━━━━━━━━━━━━━━━━━━━━━━
 <a href="https://t.me/MomeniTOEFL/725">𝑬𝒍𝒊𝒕𝒆 𝑻𝑶𝑬𝑭𝑳 𝑨𝒄𝒂𝒅𝒆𝒎𝒚</a>
"""
            # Send to user without inline buttons
            bot.send_message(message.chat.id, reply_text, parse_mode="HTML")
            
            # Send to channel with inline buttons
            channel_message = f"""
📖 <b>Word:</b> <code>{word}</code>
📌 <b>Part of Speech:</b> <i>{part_of_speech}</i>
📝 <b>Meaning:</b> <code>{meaning}</code>
━━━━━━━━━━━━━━━━━━━━━━━
<a href="https://t.me/MomeniTOEFL">Join 𝑬𝒍𝒊𝒕𝒆 𝑻𝑶𝑬𝑭𝑳 𝑨𝒄𝒂𝒅𝒆𝒎𝒚</a>
"""
            bot.send_message(
                "-1002369564811",  # Channel name
                channel_message,
                parse_mode="HTML",
                reply_markup=create_inline_button()  # Inline buttons for the channel
            )
        else:
            bot.send_message(
                message.chat.id, 
                f"❌ <b>Sorry, I couldn't find the meaning of</b> <code>{word}</code>.",
                parse_mode="HTML"
            )
        
        time.sleep(1)  # Add delay to avoid spam

# Start the bot
bot.polling()