import os
import json
import re
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from services.bmkg import get_gempa_terkini
from services.usgs import cari_gempa_usgs

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Handler for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Define custom keyboard layout for the bot menu
    keyboard = [
        ["🚨 Gempa Terkini", "🔍 Cari Riwayat Gempa"],
        ["📜 Sejarah Gempa Terparah", "🗺️ Zona Potensi Bencana"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "👋 Selamat datang di *Ingfo Gempa Bot*!\n\n"
        "Silakan pilih menu di bawah untuk mendapatkan informasi seputar gempa bumi.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Handler to manage incoming text messages from custom keyboard buttons
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    if user_text == "🚨 Gempa Terkini":
        # Call service to fetch data from BMKG API
        hasil_gempa = get_gempa_terkini()
        await update.message.reply_text(hasil_gempa, parse_mode="Markdown")

    elif user_text == "📜 Sejarah Gempa Terparah":
        try:
            # Read local historical data from JSON file
            with open("data/sejarah.json", "r", encoding="utf-8") as file:
                data_sejarah = json.load(file)
            
            teks_balasan = "📜 *CATATAN GEMPA TERPARAH DALAM SEJARAH INDONESIA*\n\n"
            
            for item in data_sejarah:
                teks_balasan += (
                    f"🏛️ *{item['nama']}*\n"
                    f"📉 *Kekuatan:* {item['magnitudo']}\n"
                    f"👥 *Dampak Korban:* {item['korban']}\n"
                    f"📝 *Catatan:* {item['dampak']}\n\n"
                    f"-----------------------------------\n\n"
                )
                
            await update.message.reply_text(teks_balasan, parse_mode="Markdown")
        except Exception as e:
            print(f"Error membaca sejarah.json: {e}")
            await update.message.reply_text("❌ Gagal memuat data sejarah gempa.")

    elif user_text == "🗺️ Zona Potensi Bencana":
        try:
            # Read local hazard zone data from JSON file
            with open("data/potensi.json", "r", encoding="utf-8") as file:
                data_potensi = json.load(file)
            
            teks_balasan = "🗺️ *EDUKASI ZONA POTENSI GEMPA DI INDONESIA*\n\n"
            teks_balasan += "Indonesia dikelilingi oleh berbagai zona rawan gempa. Berikut adalah pembagian utamanya:\n\n"
            teks_balasan += "-----------------------------------\n\n"
            
            for item in data_potensi:
                teks_balasan += (
                    f"📌 *{item['kategori']}*\n\n"
                    f"📍 *Wilayah Rawan:* {item['wilayah']}\n\n"
                    f"📖 *Penjelasan:* {item['penjelasan']}\n\n"
                    f"-----------------------------------\n\n"
                )
                
            await update.message.reply_text(teks_balasan, parse_mode="Markdown")
        except Exception as e:
            print(f"Error membaca potensi.json: {e}")
            await update.message.reply_text("❌ Gagal memuat data zona potensi bencana.")
            
    elif user_text == "🔍 Cari Riwayat Gempa":
        await update.message.reply_text(
            "Silakan ketik tanggal gempa yang ingin dicari.\n\n"
            "Format penulisan: *YYYY-MM-DD*\n"
            "Contoh: `2024-01-01`",
            parse_mode="Markdown"
        )

    else:
        # Check if the input string matches the date format pattern (YYYY-MM-DD) using Regex
        if re.match(r"^\d{4}-\d{2}-\d{2}$", user_text):
            await update.message.reply_text("🔄 Sedang mencari data ke database USGS global...")
            
            # Call service to query and filter USGS database
            hasil_pencarian = cari_gempa_usgs(user_text)
            await update.message.reply_text(hasil_pencarian, parse_mode="Markdown")
        else:
            await update.message.reply_text(
                "⚠️ Format tidak dikenali.\n\n"
                "Jika ingin mencari riwayat gempa, silakan ketik tanggal dengan format *YYYY-MM-DD*.\n"
                "Contoh: `2024-01-01`", 
                parse_mode="Markdown"
            )

# Application entry point
def main():
    print("Mencoba membaca token...") 
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN belum diatur!")
        return

    print(f"Token ditemukan: {TOKEN[:10]}... (disamarkan)") 
    print("Menghubungkan ke Telegram...") 

    try:
        # Initialize the Telegram Application
        app = Application.builder().token(TOKEN).build()

        # Register event handlers for commands and text messages
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # Start the bot using Long Polling method
        print("Bot BERHASIL berjalan! Silakan cek Telegram Anda. Tekan Ctrl+C untuk setop.")
        app.run_polling()
        
    except Exception as e:
        print(f"Terjadi ERROR saat menjalankan bot: {e}")

if __name__ == '__main__':
    main()