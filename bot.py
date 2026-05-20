from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

from datetime import datetime
import asyncio

# ==============================
# CONFIGURA ESTO
# ==============================

TOKEN = "8638884663:AAE3BpulN6sIliZicJL6DWnKhzHZJ9UgNI4"
ADMIN_ID = 7957443258

# ==============================
# TIEMPO INTELIGENTE
# ==============================

def tiempo_inteligente(fecha):
    ahora = datetime.now()
    diferencia = ahora - fecha

    segundos = int(diferencia.total_seconds())
    minutos = segundos // 60
    horas = minutos // 60
    dias = diferencia.days

    if segundos < 60:
        return "Hace un momento"

    elif minutos == 1:
        return "Hace 1 minuto"

    elif minutos < 60:
        return f"Hace {minutos} minutos"

    elif horas == 1:
        return "Hace 1 hora"

    elif horas < 24:
        return f"Hace {horas} horas"

    elif dias == 1:
        return "Ayer a las " + fecha.strftime("%I:%M %p")

    elif dias == 2:
        return "Antier a las " + fecha.strftime("%I:%M %p")

    elif dias < 7:
        return fecha.strftime("%A a las %I:%M %p")

    else:
        return fecha.strftime("%d/%m/%Y %I:%M %p")

# ==============================
# ACTUALIZAR MENSAJE
# ==============================

async def actualizar_mensaje(
    context,
    chat_id,
    message_id,
    usuario,
    fecha
):
    while True:

        tiempo = tiempo_inteligente(fecha)

        texto = f"""
🔔 Nuevo usuario

👤 Usuario: @{usuario}
⏳ {tiempo}
"""

        try:
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=texto
            )

        except:
            pass

        await asyncio.sleep(60)

# ==============================
# START
# ==============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    fecha = datetime.now()

    usuario = user.username

    if not usuario:
        usuario = user.first_name

    # MENSAJE AL USUARIO
    await update.message.reply_text(
        "👋 Bienvenido al bot\n\n⚡ Ya estás conectado"
    )

    # MENSAJE AL ADMIN
    mensaje = await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"""
🔔 Nuevo usuario

👤 Usuario: @{usuario}
⏳ Hace un momento
"""
    )

    # ACTUALIZAR MENSAJE SOLO
    asyncio.create_task(
        actualizar_mensaje(
            context,
            ADMIN_ID,
            mensaje.message_id,
            usuario,
            fecha
        )
    )

# ==============================
# BOT
# ==============================

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

print("Bot encendido 😼")

app.run_polling()
