from telegram import Update
from telegram.ext import CallbackContext

from django.utils import timezone
from django.conf import settings
import pytz

from api.utils import toggle_workplace, toggle_service, send_telegram_message
from api.utils.debt import get_debt_list
from .workplaces import get_workplaces_keyboard
from .service_config import get_service_keyboard

BRANCHES_ID = settings.BRANCHES_ID


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
        for branch in BRANCHES_ID:
            debt_list = get_debt_list(branch, time, data[1])
            message = "Список клиентов, у которых есть задолженность\n\n"

            for i in range(0, len(debt_list["customers"])):
                amount = "{:,.2f}".format(debt_list["customers"][i]["amount"]).replace(
                    ",", " "
                )
                message += f'{i + 1}. {debt_list["customers"][i]["name"]} --> {amount} {data[1]}\n'

            message += (
                f"\nОбщий долг (50 чел.): "
                + "{:,.2f}".format(debt_list["total_debt"]).replace(",", " ")
                + f" {data[1]}"
            )
            send_telegram_message(message)
        query.answer("✅ Список клиентов успешно отправлен в чат")
        query.message.delete()
        return
