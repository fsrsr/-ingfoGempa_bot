import requests

def get_gempa_terkini():
    # URL API JSON resmi dari BMKG untuk 1 gempa terbaru M >= 5.0
    url = "https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json"
    
    try:
        # Menembak API BMKG dengan batas waktu tunggu (timeout) 10 detik
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            gempa = data['Infogempa']['gempa']
            
            # Mengambil URL peta guncangan dari BMKG
            peta_url = f"https://data.bmkg.go.id/DataMKG/TEWS/{gempa['Shakemap']}"
            
            # Menyusun teks balasan dengan format Markdown (tanda * untuk cetak tebal)
            # Ubah penyusunan teks_balasan di dalam file services/bmkg.py menjadi seperti ini:

            teks_balasan = (
                f"🚨 *INFORMASI GEMPA TERKINI BMKG* 🚨\n\n"
                f"📅 *Waktu:* {gempa['Tanggal']} | {gempa['Jam']}\n\n"
                f"📈 *Magnitudo:* {gempa['Magnitude']} SR\n\n"
                f"↕️ *Kedalaman:* {gempa['Kedalaman']}\n\n"
                f"📍 *Koordinat:* {gempa['Coordinates']}\n\n"
                f"🗺️ *Lokasi:* {gempa['Wilayah']}\n\n"
                f"⚠️ *Potensi:* {gempa['Potensi']}\n\n"
                f"👥 *Dirasakan:* {gempa['Dirasakan']}\n\n"
                f"🖼️ [Lihat Peta Guncangan BMKG]({peta_url})"
            )
            return teks_balasan
        else:
            return "❌ Gagal mengambil data dari server BMKG (Status code bukan 200)."
            
    except Exception as e:
        print(f"Error saat mengambil data BMKG: {e}")
        return "❌ Terjadi gangguan koneksi saat menghubungi server BMKG."