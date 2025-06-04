from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from core.code_redeem import redeem_code, import_redeem_codes
from core.user_manager import add_points_to_user  # 请根据实际项目修改为积分操作函数
from loader import dp  # 如果你项目不是 loader.py 请改成你注册 dp 的地方

ADMIN_ID = 8088038471

class RedeemStates(StatesGroup):
    awaiting_code = State()

@dp.message_handler(commands=['redeem'])
async def cmd_redeem(message: types.Message):
    await message.reply("请输入您要兑换的兑换码：")
    await RedeemStates.awaiting_code.set()

@dp.message_handler(state=RedeemStates.awaiting_code)
async def process_code(message: types.Message, state: FSMContext):
    code = message.text.strip()
    user_id = message.from_user.id

    success, result = redeem_code(code, user_id)
    if not success:
        await message.reply(result)
    else:
        add_points_to_user(user_id, result)
        await message.reply(f"✅ 兑换成功！已为您增加 {result} 积分。")
    await state.finish()

@dp.message_handler(commands=['upload_codes'])
async def upload_codes(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.reply("❌ 您没有权限执行此命令")
        return
    await message.reply("请发送包含兑换码的 TXT 文件（格式：兑换码:积分值）")

@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_upload_file(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    document = message.document
    path = f"temp/{document.file_name}"
    await document.download(destination_file=path)
    count = import_redeem_codes(path)
    await message.reply(f"✅ 已成功导入 {count} 个兑换码")

