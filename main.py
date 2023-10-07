from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes,CallbackQueryHandler
import pandas as pd

token = ''                                         #bot token

data = pd.read_csv('quran.csv')


keyboard = [[InlineKeyboardButton(text=data['name'].loc[0],callback_data='0'),
            InlineKeyboardButton(text=data['name'].loc[1],callback_data='1')],
            [InlineKeyboardButton(text=data['name'].loc[2],callback_data='2'),
            InlineKeyboardButton(text=data['name'].loc[3],callback_data='3')],
            [InlineKeyboardButton(text=data['name'].loc[4],callback_data='4'),
            InlineKeyboardButton(text=data['name'].loc[5],callback_data='5')],
            [InlineKeyboardButton(text=data['name'].loc[6],callback_data='6'),
            InlineKeyboardButton(text=data['name'].loc[7],callback_data='7')],
            [InlineKeyboardButton(text=data['name'].loc[8],callback_data='8'),
            InlineKeyboardButton(text=data['name'].loc[9],callback_data='9')],
            [InlineKeyboardButton(text=data['name'].loc[10],callback_data='10'),
            InlineKeyboardButton(text=data['name'].loc[11],callback_data='11')],
            [InlineKeyboardButton(text=data['name'].loc[12],callback_data='12'),
            InlineKeyboardButton(text=data['name'].loc[13],callback_data='13')],
            [InlineKeyboardButton(text=data['name'].loc[14],callback_data='14'),
            InlineKeyboardButton(text=data['name'].loc[15],callback_data='15')],
            [InlineKeyboardButton(text=data['name'].loc[16],callback_data='16'),
            InlineKeyboardButton(text=data['name'].loc[17],callback_data='17')],
            [InlineKeyboardButton(text=data['name'].loc[18],callback_data='18'),
           ]]


users = []
users_num_messages = {}

def record_user(f):
    async def message(update:Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.message.from_user.full_name
        print(user)
        if user not in users:
            users.append(user)
            users_num_messages['user'] = 1 
        else:
            users_num_messages['user'] += 1
        await f(update,context)
    return message

async def button(update:Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    success = await query.answer()
    choosed = query.data
    await query.edit_message_text(data['link'].loc[int(choosed)])    

@record_user
async def start_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("انا بوت المصحف انا هنا لمساعدتك علي تنزيل القرأن الكريم")

@record_user
async def help_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('فقط اختار اسم الشيخ وسأرسل لك رابط تحميل القرأن بصوته')

@record_user
async def choose_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('قم بالاختيار بين هذه الشيوخ',reply_markup=menu)



'''async def handle_messages(update:Update, context:ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text in sheikh_list:
        await update.message.reply_text(links[text])
    else:
        await update.message.reply_text('لم يتم التعرف علي الشيخ')
        print(f'User {update.message.from_user.full_name} send message {update.message.text}')
'''
async def error(update:Update, context:ContextTypes.DEFAULT_TYPE):
    print(f'User {update.message.from_user.full_name} caused error {context.error}')
    

start = CommandHandler('start',start_command)
help = CommandHandler('help',help_command)
#message = MessageHandler(filters.TEXT, handle_messages)
menu = InlineKeyboardMarkup(keyboard)
choose = CommandHandler('choose',choose_command)
buttonHan = CallbackQueryHandler(button)

if __name__ == '__main__':
    app = Application.builder().token(token).build()
    app.add_handlers([start,help,choose,buttonHan])
    #app.add_error_handler(error)
    app.run_polling(poll_interval=3)