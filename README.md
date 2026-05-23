# 🚨 Ingfo Gempa Bot - Telegram Bot

**Ingfo Gempa Bot** is a Telegram chatbot built using Python. This bot is designed to provide real-time information and educational data regarding seismic activities (earthquakes) in Indonesia by integrating third-party public APIs and managing local structured data.

This project serves as an excellent portfolio piece to demonstrate backend development skills, API integration, data cleansing, and asynchronous programming in Python.

---

## 🚀 Key Features

* **🚨 Latest Earthquake (Gempa Terkini):** Fetches real-time data for the most recent earthquake ($M \ge 5.0$) directly from the **Official BMKG JSON API**, complete with the official shake map (*shakemap*) URL.
* **🔍 Search Earthquake History:** Allows users to query historical earthquake data by entering a specific date (Format: `YYYY-MM-DD`). This feature consumes data globally from the **USGS (United States Geological Survey) API**, filters it specifically for Indonesia's coordinates, and automatically converts the timestamps from UTC to Western Indonesian Time (WIB) to prevent time-zone confusion.
* **📜 Worst Historical Earthquakes:** Displays a curated list of the most destructive earthquakes in Indonesia's history, powered by a fast local **JSON** data file.
* **🗺️ Hazard Zone Education:** An educational menu detailing major fault lines and seismic hazard zones in Indonesia (e.g., *Megathrust* zones and active land faults) utilizing structured local **JSON** storage.

---

## 🛠️ Tech Stack & Libraries

* **Language:** Python 3.13+
* **Bot Framework:** `python-telegram-bot` (Asynchronous v20.x+)
* **HTTP Client:** `requests` (For consuming third-party REST APIs)
* **Environment Management:** `python-dotenv` & `Virtual Environment (venv)`
* **Data Parsing:** JSON & Regex (Regular Expressions for date input validation)

---

## 📦 Project Architecture

```text
├── data/
│   ├── potensi.json         # Static JSON data for seismic hazard zones
│   └── sejarah.json         # Static JSON data for historical earthquakes
├── services/
│   ├── bmkg.py              # Business logic for BMKG API integration
│   └── usgs.py              # Business logic for USGS API integration & filtering
├── .env                     # Local bot token configuration (Git-ignored)
├── .gitignore               # Directives for files excluded from Git tracking
├── main.py                  # Core application entry point
└── README.md                # Project documentation