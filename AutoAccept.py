from asyncio import exceptions
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database import Database
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

import asyncio
import aiogram

bot = Bot(token="6692343081:AAFFpWhtupevNoZg67267MWpsYRNRIefycU", parse_mode='HTML')
sticker_id = "CAACAgIAAxkBAAEM_UdnE9lMW-wYlkzaF2DDSAYChi9ufwACAVsAAiUZoEgs8TFWd9ToZjYE"
admin_id = 1474037137
group_id = 1474037137
channelid = -1001635214395

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()

remove_keyboard_markup = types.ReplyKeyboardRemove()

class UserConfirmation(StatesGroup):
    confirmation = State()

@dp.chat_join_request_handler()
async def start1(update: types.ChatJoinRequest):
    confirm_button = KeyboardButton('Подтвердить')
    reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(confirm_button)
    user = update.from_user
    user_mention = user.get_mention()
    await update.bot.send_message(chat_id=user.id, text=f'<b>‼️ {user_mention}, для доступа к чату нажми кнопку "<u>Подтвердить</u>"</b>', reply_markup=reply_keyboard)
    state = dp.current_state(user=user.id)
    await state.set_state(UserConfirmation.confirmation)

@dp.message_handler(content_types=types.ContentType.TEXT, text=['Подтвердить'])
async def confirm_user(message: types.Message, state: FSMContext):
    await bot.approve_chat_join_request(chat_id=channelid, user_id=message.from_user.id)
    usersf = db.get_user(message.from_user.id)
    accepted_message = f'<b>✅ {message.from_user.get_mention()} твоя заявка в <a href="https://t.me/VapeVyazma">чат</a> была принята!\n\n🔗 Актуальная ссылка - <a href="https://t.me/VapeVyazma">чат</a>\n\n📄 Для ознакомления с правилами чата, пропиши <u>/rules</u>\n\n🔝 Для покупки продвижения объявления, пропиши <u>/donat</u>\n\n💬 Чтобы вступить в другие наши проекты, пропиши <u>/proect</u>\n\n🎁 Для проверки актуальных розыгрышей, пропиши <u>/present</u>\n\n❓ Для связи с агентами поддержки, пропиши <u>/help</u>\n\n⚠️ Для получения актуальной информации или помощи в случаи блокировки, пропиши <u>/start</u></b>'
    await message.answer_sticker(sticker_id)
    sent_message = await message.answer(accepted_message, disable_web_page_preview=True, reply_markup=remove_keyboard_markup)
    pinned_message = await bot.pin_chat_message(chat_id=message.chat.id, message_id=sent_message.message_id)
    if usersf is not None:
        db.add_user(message.from_user.id)
        await bot.send_message(chat_id=admin_id, text=f"<b>✅ Приняли в чат пользователя:</b> {message.from_user.get_mention()}")
    else:
        await bot.send_message(chat_id=admin_id, text=f"<b>✅ Приняли в чат пользователя:</b> {message.from_user.get_mention()}")
    await state.finish()

@dp.message_handler(content_types=[
    types.ContentType.PINNED_MESSAGE,
])
async def delete_system_messages(message: types.Message):
    if message.from_user.id:
        await message.delete()

@dp.message_handler(state=UserConfirmation.confirmation)
async def handle_confirmation(message: types.Message,state=FSMContext):
    print(state)
    await message.answer('<b>⚠️ Для доступа к чату нажми кнопку <u>"Подтвердить"</u></b>')

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    existing_user = db.get_user(message.from_user.id)
    await message.answer_sticker(sticker_id)
    await message.answer(f"<b>👋🏻 Привет, {message.from_user.get_mention()}\n\n🔗 Актуальная ссылка - <a href='https://t.me/VapeVyazma'>чат</a>\n\n📄 Для ознакомления с правилами чата, пропиши <u>/rules</u>\n\n🔝 Для покупки продвижения объявления, пропиши <u>/donat</u>\n\n💬 Чтобы вступить в другие наши проекты, пропиши <u>/proect</u>\n\n🎁 Для проверки актуальных розыгрышей, пропиши <u>/present</u>\n\n❓ Для связи с агентами поддержки, пропиши <u>/help</u>\n\n⚠️ Для получения актуальной информации или помощи в случаи блокировки, пропиши <u>/start</u></b>", disable_web_page_preview=True, reply_markup=remove_keyboard_markup)
    if existing_user is None:
        db.add_user(message.from_user.id)

@dp.message_handler(content_types="new_chat_members")
async def on_user_join(message: types.Message):
    await message.delete()
    await bot.send_message(chat_id=admin_id, text=f'✅ Новый участник в чате:\n\n'
                                               f'{message.from_user.get_mention()} | {message.from_user.full_name}\n'
                                               f'Id: {message.from_user.id}\n'
                                               f'Username: @{message.from_user.username}\n'
                                               )
    new_msg = await message.answer(f'{message.from_user.get_mention()} Добро пожаловать в чат!', disable_web_page_preview=True)
    await asyncio.sleep(15)
    try:
        await new_msg.delete()
    except Exception as e:
        pass

@dp.message_handler(content_types="left_chat_member")
async def on_user_join(message: types.Message):
    await message.delete()

@dp.message_handler(content_types="new_chat_title")
async def on_user_join(message: types.Message):
    await message.delete()

@dp.message_handler(content_types="new_chat_photo")
async def on_user_join(message: types.Message):
    await message.delete()

@dp.message_handler(content_types="delete_chat_photo")
async def on_user_join(message: types.Message):
    await message.delete()

@dp.message_handler(commands=['send'])
async def send_all_users(message: types.Message):
    if message.from_user.id == admin_id:
        users = db.get_users()
        successful_sends = 0
        failed_sends = 0
        text_to_send = f"<blockquote>{message.text.replace('/send ', '')}</blockquote>"
        for user in users:
            try:
                await bot.send_message(chat_id=user[0], text=text_to_send, parse_mode='HTML')
                await asyncio.sleep(0.5)
                successful_sends += 1
            except aiogram.utils.exceptions.TelegramAPIError as e:
                failed_sends += 1
        await bot.send_message(chat_id=admin_id, text=f"Рассылка завершена!\n\nУспешно отправлено сообщений: {successful_sends}\nСообщений с ошибками: {failed_sends}")

@dp.message_handler(content_types=['photo', 'video', 'document', 'text'], chat_id=group_id)
async def handle_comment(message: types.Message):
    if message.from_user.id != 777000:
        pass
    elif message.chat.id != group_id:
        pass
    else:
        await message.reply("+", disable_web_page_preview=True)

class SupportStates(StatesGroup):
    waiting_for_question = State()
    waiting_for_answer = State()

@dp.message_handler(commands=['rules'])
async def send_rules(message: types.Message):
    try:
        message_id = 30
        await bot.forward_message(chat_id=message.from_user.id, from_chat_id=channelid, message_id=message_id)
    except exceptions.ChatNotFound:
        await message.answer("К сожалению, я не могу найти правила. Попробуйте позже.")
    except exceptions.MessageNotFound:
        await message.answer("Сообщение с правилами не найдено.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message, state: FSMContext):
    await message.answer(f"<b>✉️ Для <u>связи</u> с администратором, задайте свой свой <u>вопрос</u> и отправьте его в этот чат</b>")
    await SupportStates.waiting_for_question.set()

@dp.message_handler(state=SupportStates.waiting_for_question)
async def handle_question(message: types.Message, state: FSMContext):
    await bot.send_message(
        chat_id=admin_id,
        text=f"<b>❓ Новый <u>вопрос</u> от пользователя</b> \n{message.from_user.get_mention()}\n\n<blockquote>{message.text}</blockquote>",
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("Ответить", callback_data=f"reply_{message.from_user.id}"),
            InlineKeyboardButton("Закончить диалог", callback_data=f"finish_{message.from_user.id}")
        )
    )
    await message.answer(f"<b>✅ Сообщение <u>отправлено</u> агенту поддержки, <u>ожидайте</u> ответа</b>")
    await state.finish()

@dp.message_handler(commands=['donat'])
async def handle_donat_command(message: types.Message):
    inline_keyboard = InlineKeyboardMarkup()
    purchase_button = InlineKeyboardButton("Покупка продвижения", url="https://t.me/interdine")
    inline_keyboard.add(purchase_button)
    await message.answer(
        f"<b>🔝 Для <u>покупки</u> продвижения своего <u>объявления</u>, <u>услуги</u> или <u>префикса</u> в чате, <u>свяжитесь</u> с технической поддержкой чата, нажав на <u>кнопку</u> ниже</b>",
        reply_markup=inline_keyboard
    )

@dp.message_handler(commands=['proect'])
async def handle_proect_command(message: types.Message):
    await message.answer(
        f"<b>💬 Наши проекты, для входа нажмите на нужный вам чат и вступите в него\n\n"
        f"🚬 <a href='https://t.me/VapeVyazma'>vape барахолка | вязьма</a>\n"
        f"💬 <a href='https://t.me/ChatsVyazma'>чат общения | вязьма</a>\n"
        f"📢 <a href='https://t.me/FleamarketVyazma'>барахолка | вязьма</a>\n"
        f"🚓 <a href='https://t.me/+PESSI5xVBKJiZmUy'>без гаи | вязьма</a></b>",
        disable_web_page_preview=True
    )

@dp.message_handler(commands=['present'])
async def handle_present_command(message: types.Message):
    await message.answer(f"<b>❎ В данный момент нет доступных <u>розыгрышей</u>, <u>не блокируйте</u> бота и <u>не удаляйте</u> чат, чтобы мы <u>смогли</u> <u>отправить</u> вам <u>уведомления</u> о новом <u>розыгрыше</u></b>")

@dp.message_handler(content_types=[
    types.ContentType.NEW_CHAT_MEMBERS,        # Новые участники
    types.ContentType.LEFT_CHAT_MEMBER,        # Ушедший участник
    types.ContentType.NEW_CHAT_TITLE,          # Новое название чата
    types.ContentType.NEW_CHAT_PHOTO,          # Новое фото чата
    types.ContentType.DELETE_CHAT_PHOTO,       # Удаление фото чата
    types.ContentType.GROUP_CHAT_CREATED,      # Создание группового чата
    types.ContentType.MIGRATE_TO_CHAT_ID,      # Миграция чата
    types.ContentType.MIGRATE_FROM_CHAT_ID,    # Миграция из чата
    types.ContentType.PINNED_MESSAGE,          # Закрепленное сообщение

])
async def delete_system_messages(message: types.Message):
    if message.chat.id == channelid:
        await message.delete()

@dp.message_handler(lambda message: message.reply_to_message and message.reply_to_message.text.startswith("🆘 Новый вопрос от"), state="*")
async def handle_answer(message: types.Message, state: FSMContext):
    original_question = message.reply_to_message.text.split(":\n\n", 1)[1]
    user_id = message.reply_to_message.from_user.id
    await bot.send_message(
        chat_id=user_id, 
        text=f"<b>📩 <u>Ответ</u> от администрации:</b>\n\n<blockquote>{message.text}</blockquote>",
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("Ответить", callback_data=f"reply_{user_id}"),
            InlineKeyboardButton("Закончить диалог", callback_data=f"finish_{user_id}")
        )
    )

@dp.callback_query_handler(lambda c: c.data.startswith('finish_'))
async def finish_dialog(callback_query: types.CallbackQuery):
    user_id = int(callback_query.data.split('_')[1])
    is_admin = (callback_query.from_user.id == admin_id)
    if is_admin:
        await bot.send_message(user_id, f"<b>❎ <u>Диалог></u> с агентом поддержки <u>завершен></u></b>")
    else:
        await bot.send_message(admin_id, f"<b>❎ Пользователь <u>завершил</u> диалог с вами</b>")
    await bot.answer_callback_query(callback_query.id)
    await dp.current_state(user=user_id).finish()

@dp.callback_query_handler(lambda c: c.data.startswith('reply_'))
async def reply_to_user(callback_query: types.CallbackQuery):
    user_id = int(callback_query.data.split('_')[1])
    await bot.send_message(callback_query.from_user.id, "<b>✉️ <u>Напишите</u> свой ответ <u>пользователю</u></b>")
    await dp.current_state(user=callback_query.from_user.id).update_data(original_user_id=user_id)
    await dp.current_state(user=callback_query.from_user.id).set_state("waiting_for_reply")

@dp.message_handler(state="waiting_for_reply")
async def process_reply(message: types.Message, state: FSMContext):
    data = await state.get_data()
    original_user_id = data.get("original_user_id")
    try:
        await bot.send_message(
            original_user_id,
            f"<b>📩 <u>Ответ</u> от администрации:</b>\n\n<blockquote>{message.text}</blockquote>"
        )
        await message.answer("<b>✅ Ответ <u>отправлен</u> <u>пользователю</u></b>")
    except exceptions.ChatNotFound:
        await message.answer("<b>🚫 Не удалось отправить сообщение: Пользователь заблокировал бота или удалил аккаунт.</b>")
    except Exception as e:
        await message.answer(f"<b>🚩 Произошла ошибка: {str(e)}</b>")
    await state.finish()
    
if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True)
    finally:
        db.close()