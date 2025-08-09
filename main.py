from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os
import requests
from datetime import datetime, timezone

from constant import users

load_dotenv()

TELEGRAM_TOKEN = os.getenv('BOT_TOKEN')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

current_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
start_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
print(current_time)

headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

if TELEGRAM_TOKEN is None:
    raise ValueError("BOT_TOKEN not found in environment variables")

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')
    test()
    
async def reply_tweets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print('executed')
    data = await get_tweets()
    await update.message.reply_text(f'Saba: \n\n{data}')
    
async def get_tweets():
    for user in users:
        print(f'{user} executed')
        url = f'https://api.x.com/2/users/{user}/tweets?max_results=2'
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            
            data = response.json()
            return data.text
        else:
            print(f"Error {response.status_code}: {response.text}")

    
def test():
    print(users)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("reply_tweets", reply_tweets))

app.run_polling()
test()