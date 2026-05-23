import requests
from datetime import datetime, timedelta

def cari_gempa_usgs(tanggal_input):
    try:
        # Convert input date string into a Python datetime object
        tanggal_obj = datetime.strptime(tanggal_input, "%Y-%m-%d")
        
        # Expand search range: from 1 day before input to the input date itself to handle UTC shifts
        start_date = (tanggal_obj - timedelta(days=1)).strftime("%Y-%m-%d")
        end_date = tanggal_input
        
        # USGS API URL with bounding box coordinates optimized for Indonesia region
        url = (
            f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson"
            f"&starttime={start_date}T00:00:00&endtime={end_date}T23:59:59"
            f"&minlatitude=-11&maxlatitude=6&minlongitude=95&maxlongitude=141"
            f"&minmagnitude=4.5"
        )
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            features = data.get('features', [])
            
            if not features:
                return f"ℹ️ Tidak ditemukan catatan gempa signifikan (M >= 4.5) murni di wilayah Indonesia pada rentang tanggal tersebut."
            
            teks_balasan = f"🔍 *HASIL PENCARIAN GEMPA INDONESIA (SEKITAR {tanggal_input})*\n"
            teks_balasan += f"Magnitudo M >= 4.5 | Menampilkan maks. 5 gempa terdekat\n"
            teks_balasan += "-----------------------------------\n\n"
            
            jumlah_gempa_indonesia = 0
            
            for item in features:
                prop = item['properties']
                lokasi_mentah = prop['place'].lower()
                
                # Filter out neighboring countries within the bounding box
                if "philippines" in lokasi_mentah or "timor-leste" in lokasi_mentah or "papua new guinea" in lokasi_mentah or "malaysia" in lokasi_mentah:
                    continue 
                
                # Convert USGS epoch time (milliseconds) to local system time (WIB)
                waktu_gempa = datetime.fromtimestamp(prop['time'] / 1000).strftime('%d-%m-%Y %H:%M')
                
                # Clean up and localize English terms from USGS response
                lokasi_rapi = prop['place']
                lokasi_rapi = lokasi_rapi.replace(", Indonesia", "").replace("Indonesia", "")
                lokasi_rapi = lokasi_rapi.replace("offshore", "Lepas Pantai").replace("region", "Wilayah").replace("sea", "Laut")
                lokasi_rapi = lokasi_rapi.strip().rstrip(',')
                
                teks_balasan += (
                    f"📅 *Waktu Lokal (WIB):* {waktu_gempa} WIB\n\n"
                    f"📉 *Magnitudo:* {prop['mag']} Mw\n\n"
                    f"🗺️ *Lokasi:* {lokasi_rapi}, Indonesia\n\n"
                    f"🌐 [Detail Link USGS]({prop['url']})\n\n"
                    f"-----------------------------------\n\n"
                )
                
                jumlah_gempa_indonesia += 1
                if jumlah_gempa_indonesia >= 5:
                    break
            
            if jumlah_gempa_indonesia == 0:
                return f"ℹ️ Tidak ditemukan catatan gempa signifikan murni di Indonesia sekitar tanggal *{tanggal_input}*."
            
            # Add time literacy notice to prevent user confusion regarding UTC vs WIB
            teks_balasan += (
                f"💡 *Catatan Literasi Waktu:*\n"
                f"Waktu di atas sudah dikonversi otomatis oleh bot ke *Waktu Indonesia Barat (WIB)*. "
                f"Jika Anda membuka [Detail Link USGS] yang disediakan, situs web USGS akan menampilkan waktu dalam standar "
                f"*UTC (Waktu Internasional)* yang berselisih *7 jam lebih lambat* dari WIB (WIB = UTC + 7 jam). "
                f"Oleh karena itu, tanggal/jam di web USGS mungkin terlihat bergeser ke hari sebelumnya."
            )
                
            return teks_balasan
        else:
            return "❌ Gagal menghubungi server USGS."
            
    except ValueError:
        return "❌ Format tanggal salah. Gunakan format YYYY-MM-DD."
    except Exception as e:
        print(f"Error filter USGS: {e}")
        return "❌ Terjadi gangguan koneksi saat menyaring data USGS."