import telebot
from telebot import types

# 1. INSERT YOUR REAL TOKEN BELOW
# Make sure the quote ' is at the beginning AND the end on this same line!
API_TOKEN = '8608488880:AAFc8mWRoqTL513ugCyc5tzP9vvlz650Llo'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "💰 *Welcome to SplitWise Lite*\n\n"
        "I help you split bills and calculate tips instantly.\n\n"
        "*Step 1:* Send me the total bill amount (e.g., 150 or 42.50)."
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_bill(message):
    # Clean the input (remove $ if they added it)
    clean_text = message.text.replace('$', '').strip()
    
    try:
        bill_amount = float(clean_text)
        
        # Create buttons for splitting
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("👥 2 People", callback_data=f"split_{bill_amount}_2"),
            types.InlineKeyboardButton("👥 3 People", callback_data=f"split_{bill_amount}_3"),
            types.InlineKeyboardButton("👥 4 People", callback_data=f"split_{bill_amount}_4"),
            types.InlineKeyboardButton("👥 5 People", callback_data=f"split_{bill_amount}_5"),
            types.InlineKeyboardButton("👥 6 People", callback_data=f"split_{bill_amount}_6"),
            types.InlineKeyboardButton("❓ Help", callback_data="split_help")
        )
        
        bot.send_message(
            message.chat.id, 
            f"✅ Total Bill: ${bill_amount:.2f}\nHow many people are splitting?", 
            reply_markup=markup
        )
    except ValueError:
        bot.send_message(message.chat.id, "❌ Please send a valid number (e.g., 120.00).")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "split_help":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "Simply type the total bill amount first, then tap a button to see the individual share.")
        return

    if call.data.startswith('split_'):
        # Extract bill and people count from callback_data
        _, bill, people = call.data.split('_')
        bill = float(bill)
        people = int(people)
        
        share = bill / people
        
        result_text = (
            f"📊 *Splitting Details*\n\n"
            f"💰 Total Bill: ${bill:.2f}\n"
            f"👥 People: {people}\n"
            f"➖➖➖➖➖➖➖➖\n"
            f"💳 *Each person pays: ${share:.2f}*"
        )
        
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, result_text, parse_mode="Markdown")

bot.polling()
