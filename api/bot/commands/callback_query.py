import os
from telegram import Update
from telegram.ext import CallbackContext

from django.utils import timezone
from django.conf import settings
import pytz

from api.utils import toggle_workplace, toggle_service, send_telegram_message
from api.utils.debt import get_debt_list
from api.utils.excel import create_debt_list_file
from .workplaces import get_workplaces_keyboard
from .service_config import get_service_keyboard
from .debt import get_export_keyboard

BRANCHES_ID = settings.BRANCHES_ID
CHAT_ID = settings.CHAT_ID


def get_current_time() -> str:
    current_time_utc = timezone.now()
    tashkent_timezone = pytz.timezone("Asia/Tashkent")
    current_time = current_time_utc.astimezone(tashkent_timezone)

    formatted_time = current_time.strftime("%d/%m/%Y %H:%M:%S")
    return formatted_time


def callback_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data.split(":")

    if data[0] == "done":
        time = get_current_time()
        message = "СМС-сервис" if data[1] == "service" else "Рабочие места"
        message += f" обновлено/просмотрено пользователем {update.effective_user.full_name} в {time}"
        send_telegram_message(message)
        query.message.delete()
        return

    elif data[0] == "workplace":
        if not toggle_workplace(data[1]):
            query.answer(text="⚠️ Невозможно переключить рабочее место")

        new_markup = get_workplaces_keyboard()
        query.edit_message_text(
            text='Обновленные рабочие места\nнажмите "готово" чтобы выйти',
            reply_markup=new_markup,
        )

        query.answer(text="✅ Рабочее место успешно переключился")
        return

    elif data[0] == "service":
        toggle_service(data[1])

        new_markup = get_service_keyboard()
        query.edit_message_text(
            text='Служба смс обновлена.\nнажмите "готово" чтобы выйти',
            reply_markup=new_markup,
        )

        query.answer(text="✅ Служба SMS успешно обновлена")
        return

    elif data[0] == "currency":
        time = get_current_time()

        new_markup = get_export_keyboard(data[1])
        query.edit_message_text(
            text="Выберите один из вариантов ниже\n",
            reply_markup=new_markup,
        )

        return

    elif data[0] == "export":
        for branch in BRANCHES_ID:
            if data[1] == "false":
                debt_list = get_debt_list(branch, data[3])
                message = "Список клиентов, у которых есть задолженность\n\n"

                for i in range(0, len(debt_list["customers"])):
                    amount = "{:,.2f}".format(
                        debt_list["customers"][i]["amount"]
                    ).replace(",", " ")
                    message += f'{i + 1}. {debt_list["customers"][i]["name"]} --> {amount} {data[3]}\n\n'

                message += (
                    f"Общий долг (50 чел.): "
                    + "{:,.2f}".format(debt_list["total_debt"]).replace(",", " ")
                    + f" {data[3]}"
                )
                send_telegram_message(message)
            else:
                filename = "DebtList.xlsx"
                file_path = create_debt_list_file(
                    currency=data[3], filename=filename, branch=branch
                )

                context.bot.send_document(
                    chat_id=CHAT_ID,
                    document=open(file_path, "rb"),
                    caption="Список должников (топ-1000)",
                )
                os.remove(file_path)

        query.answer("✅ Список клиентов успешно отправлен в чат")
        query.message.delete()
