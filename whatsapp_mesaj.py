import tkinter as tk
from tkinter import messagebox
import pywhatkit
import schedule
import time
from datetime import datetime, timedelta
import threading

def mesaj_gonder():
    try:
        telefon_numarasi = numara_entry.get().strip()
        mesaj = mesaj_entry.get("1.0", tk.END).strip()
        tarih = tarih_entry.get().strip()
        saat = saat_entry.get().strip()
        gonderici = gonderici_entry.get().strip()

        if not telefon_numarasi or not mesaj or not tarih or not saat or not gonderici:
            messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun.")
            return

        # Telefon numarasının formatını kontrol et ve ekle
        if not telefon_numarasi.startswith("+"):
            telefon_numarasi = "+90" + telefon_numarasi

        gonderme_zamani = f"{tarih} {saat}"
        tam_mesaj = f"{mesaj}\n\n-{gonderici}"
        schedule_message(telefon_numarasi, tam_mesaj, gonderme_zamani)
        messagebox.showinfo("Başarılı", "Mesaj gönderme işlemi zamanlandı.")
    except Exception as e:
        messagebox.showerror("Hata", str(e))

def send_whatsapp_message(contact, message, send_time):
    now = datetime.now()
    send_time = datetime.strptime(send_time, "%Y-%m-%d %H:%M")

    # Gönderme zamanını mevcut zamandan en az 1 dakika ileriye ayarlama
    if send_time < now + timedelta(minutes=1):
        send_time = now + timedelta(minutes=1)
    
    hours = send_time.hour
    minutes = send_time.minute

    pywhatkit.sendwhatmsg(contact, message, hours, minutes, wait_time=20, tab_close=True)
    print(f"Mesaj gönderildi: {contact}, {message}")

def schedule_message(contact, message, send_time):
    schedule_time = datetime.strptime(send_time, "%Y-%m-%d %H:%M")
    schedule.every().day.at(schedule_time.strftime("%H:%M")).do(send_whatsapp_message, contact, message, send_time)
    print(f"Mesaj zamanlandı: {contact}, {message}, {send_time}")

# GUI oluşturma
root = tk.Tk()
root.title("WhatsApp Mesaj Gönderici")

tk.Label(root, text="Telefon Numarası:").grid(row=0, column=0, padx=10, pady=5)
numara_entry = tk.Entry(root, width=30)
numara_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Mesaj:").grid(row=1, column=0, padx=10, pady=5)
mesaj_entry = tk.Text(root, width=30, height=5)
mesaj_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Tarih (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5)
tarih_entry = tk.Entry(root, width=30)
tarih_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Saat (HH:MM):").grid(row=3, column=0, padx=10, pady=5)
saat_entry = tk.Entry(root, width=30)
saat_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Gönderici Adı:").grid(row=4, column=0, padx=10, pady=5)
gonderici_entry = tk.Entry(root, width=30)
gonderici_entry.grid(row=4, column=1, padx=10, pady=5)

gonder_button = tk.Button(root, text="Mesajı Zamanla", command=mesaj_gonder)
gonder_button.grid(row=5, column=0, columnspan=2, pady=10)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

schedule_thread = threading.Thread(target=run_schedule)
schedule_thread.daemon = True
schedule_thread.start()

root.mainloop()