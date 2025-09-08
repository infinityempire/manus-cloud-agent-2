from telegram import Bot, error as tg_error

from manus2.config import settings

MSG_TIMEOUT = "תם הזמן לבקשה, נסה שוב."
MSG_FAIL = "שליחת ההודעה נכשלה, נסה שוב מאוחר יותר."
MSG_RATE = "נדרש להמתין לפני שליחה נוספת"
MSG_NOT_CONFIGURED = "חסר טוקן או מזהה צ׳אט"


async def send_message(text: str) -> str | None:
    """Send a Telegram message and return an error string in Hebrew on failure.

    Returns ``None`` on success.
    """
    token = settings.telegram_bot_token
    chat_id = settings.telegram_chat_id
    if not token or not chat_id:
        return MSG_NOT_CONFIGURED

    bot = Bot(token=token)
    try:
        await bot.send_message(chat_id=chat_id, text=text)
        return None
    except tg_error.RetryAfter:
        return MSG_RATE
    except tg_error.TimedOut:
        return MSG_TIMEOUT
    except Exception:
        return MSG_FAIL
