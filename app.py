
import os, asyncio, logging, datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from services.llm_client import chat as ai_chat
from services.gitlab_client import trigger_pipeline, wait_pipeline, download_artifact
from services.github_client import create_release_and_upload

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("manus-agent")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_USER_ID = os.getenv("ADMIN_USER_ID")

LAST_ARTIFACT_PATH = None
LAST_RELEASE_URL = None

def is_admin(user_id):
    if not ADMIN_USER_ID:
        return True
    return str(user_id) == ADMIN_USER_ID

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("שלום! אני Manus Cloud Agent.\nפקודות:\n/ask <שאלה>\n/build\n/release\n/status")

async def cmd_ask(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(ctx.args)
    try:
        answer = ai_chat(prompt)
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text(f"שגיאה: {e}")

async def cmd_build(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    global LAST_ARTIFACT_PATH
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ אין הרשאה")
        return
    await update.message.reply_text("🚀 מריץ Pipeline...")
    pid = trigger_pipeline()
    status = wait_pipeline(pid)
    LAST_ARTIFACT_PATH = download_artifact()
    await update.message.reply_text(f"Pipeline: {status}\nArtifact: {LAST_ARTIFACT_PATH}")

async def cmd_release(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    global LAST_RELEASE_URL
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ אין הרשאה")
        return
    if not LAST_ARTIFACT_PATH:
        await update.message.reply_text("אין קובץ להעלות")
        return
    tag = datetime.datetime.utcnow().strftime("v%Y.%m.%d-%H%M")
    LAST_RELEASE_URL = create_release_and_upload(tag, "Manus Artifact", LAST_ARTIFACT_PATH)
    await update.message.reply_text(f"✅ Release: {LAST_RELEASE_URL}")

async def cmd_status(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Artifact: {LAST_ARTIFACT_PATH}\nRelease: {LAST_RELEASE_URL}")

async def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("ask", cmd_ask))
    app.add_handler(CommandHandler("build", cmd_build))
    app.add_handler(CommandHandler("release", cmd_release))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cmd_ask))
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
