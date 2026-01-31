import customtkinter as ctk
import pandas as pd
import re
import os
import random
from datetime import datetime
from PIL import Image, ImageTk, ImageSequence
import pygame

# الإعدادات
COLOR_BG = "#FDFCF0"
COLOR_PURPLE = "#5E2361"
COLOR_GOLD = "#C5A059"
COLOR_GREEN = "#006C35"
FONT_MAIN = "Arial"

class KitchenZoneFinal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("تحدي يوم التأسيس - Kitchen Zone")
        self.geometry("900x900")
        self.configure(fg_color=COLOR_BG)
        self.resizable(False, False)
        
        pygame.mixer.init()
        self.play_bg_music()

        self.target_number = 1727
        self.current_value = 1000
        self.is_running = False
        self.active_screen = ""
        self.user_phone = ""
        self.user_attempts = 0
        self.gif_path = "animation.gif"

        self.founding_facts = [
            "تأسست الدولة السعودية الأولى عام 1727م على يد الإمام محمد بن سعود.",
            "الدرعية هي عاصمة الدولة السعودية الأولى ورمز صمودها التاريخي.",
            "يوم التأسيس يرمز إلى العمق التاريخي والحضاري للمملكة.",
            "راية الدولة السعودية الأولى كانت خضراء ومشغولة بالحرير الأبيض.",
            "شعار يوم التأسيس 'يوم بدينا' يحمل رموزاً عريقة كالنخلة والخيل."
        ]

        self.setup_background_pure()
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(expand=True, fill="both", padx=40)
        self.setup_fixed_logos()
        self.bind('<space>', lambda e: self.on_space_pressed())
        self.show_welcome_screen()

    def play_bg_music(self):
        for f in ["day.mp3", "background.mp3"]:
            if os.path.exists(f):
                try:
                    pygame.mixer.music.load(f)
                    pygame.mixer.music.play(-1)
                    break
                except: pass

    def setup_background_pure(self):
        if os.path.exists("images.jpg"):
            img = Image.open("images.jpg")
            self.bg_img = ctk.CTkImage(light_image=img, size=(900, 900))
            self.bg_lbl = ctk.CTkLabel(self, image=self.bg_img, text="")
            self.bg_lbl.place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_lbl.lower()

    def setup_fixed_logos(self):
        if os.path.exists("dow.png"):
            img = Image.open("dow.png")
            self.logo_f = ctk.CTkImage(light_image=img, size=(120, 120))
            ctk.CTkLabel(self, image=self.logo_f, text="", fg_color="transparent").place(x=40, y=30)
        if os.path.exists("KZ.png"):
            img = Image.open("KZ.png")
            self.logo_k = ctk.CTkImage(light_image=img, size=(130, 75))
            ctk.CTkLabel(self, image=self.logo_k, text="", fg_color="transparent").place(x=730, y=45)

    def clear_content(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def show_welcome_screen(self):
        self.clear_content()
        self.active_screen = "welcome"
        self.user_phone = ""
        self.user_attempts = 0
        ctk.CTkLabel(self.main_container, text="تحدي يوم التأسيس", font=(FONT_MAIN, 60, "bold"), text_color=COLOR_PURPLE).pack(pady=(230, 5))
        self.phone_entry = ctk.CTkEntry(self.main_container, placeholder_text="أدخل رقم الجوال", width=400, height=65, font=(FONT_MAIN, 22), justify="center", corner_radius=15)
        self.phone_entry.pack(pady=10)
        self.error_lbl = ctk.CTkLabel(self.main_container, text="", text_color="red", font=(FONT_MAIN, 18))
        self.error_lbl.pack()
        btn = ctk.CTkButton(self.main_container, text="دخول التحدي", command=self.check_user, fg_color=COLOR_GREEN, font=(FONT_MAIN, 24, "bold"), height=65, width=300, corner_radius=35)
        btn.pack(pady=10)
        if os.path.exists(self.gif_path):
            img = Image.open(self.gif_path)
            self.frames = [ctk.CTkImage(light_image=f.copy().convert("RGBA").resize((180, 180)), size=(180, 180)) for f in ImageSequence.Iterator(img)]
            self.gif_label = ctk.CTkLabel(self.main_container, text="")
            self.gif_label.pack(pady=10)
            self.animate_gif(0)

    def animate_gif(self, index):
        if self.active_screen == "welcome" and hasattr(self, 'gif_label'):
            self.gif_label.configure(image=self.frames[index])
            self.after(50, self.animate_gif, (index + 1) % len(self.frames))

    def check_user(self):
        phone = self.phone_entry.get().strip()
        if not re.fullmatch(r"05\d{8}", phone):
            self.error_lbl.configure(text="⚠️ تأكد من رقم الجوال")
            return
        
        tries = 0
        if os.path.exists("log.xlsx"):
            try:
                df = pd.read_excel("log.xlsx")
                tries = len(df[df["الجوال"].astype(str) == str(phone)])
            except: pass
        
        if tries >= 3:
            self.show_final_msg("عذراً، استنفدت جميع محاولاتك!")
            return
            
        self.user_phone = phone
        self.user_attempts = tries
        self.show_fact_screen()

    def show_fact_screen(self):
        self.clear_content()
        self.active_screen = "fact"
        card = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius=30, border_width=2, border_color=COLOR_GOLD)
        card.pack(pady=250, padx=50, fill="both")
        ctk.CTkLabel(card, text="هل تعلم؟", font=(FONT_MAIN, 35, "bold"), text_color=COLOR_GOLD).pack(pady=(30, 10))
        ctk.CTkLabel(card, text=random.choice(self.founding_facts), font=(FONT_MAIN, 24, "bold"), text_color=COLOR_PURPLE, wraplength=500).pack(pady=20, padx=30)
        ctk.CTkButton(card, text="التالي ", command=self.show_tutorial, fg_color=COLOR_PURPLE, font=(FONT_MAIN, 22, "bold"), height=60, width=250, corner_radius=30).pack(pady=30)

    def show_tutorial(self):
        """شاشة التعليمات مع رقم سنة كبير"""
        self.clear_content()
        self.active_screen = "tutorial"
        ctk.CTkLabel(self.main_container, text="كيف تلعب؟", font=(FONT_MAIN, 50, "bold"), text_color=COLOR_PURPLE).pack(pady=(200, 10))
        ctk.CTkLabel(self.main_container, text="أوقف العداد عند تاريخ التأسيس", font=(FONT_MAIN, 30), text_color=COLOR_PURPLE).pack(pady=5)
        ctk.CTkLabel(self.main_container, text="1727", font=(FONT_MAIN, 120, "bold"), text_color=COLOR_GOLD).pack(pady=10)
        ctk.CTkButton(self.main_container, text="توكل على الله وابدأ", command=self.start_next_attempt, fg_color=COLOR_GREEN, font=(FONT_MAIN, 28, "bold"), height=75, width=350, corner_radius=35).pack(pady=30)

    def start_next_attempt(self):
        self.user_attempts += 1
        self.show_game()

    def show_game(self):
        self.clear_content()
        self.active_screen = "game"
        self.current_value = 1000
        ctk.CTkLabel(self.main_container, text=f"المحاولة {self.user_attempts} من 3", font=(FONT_MAIN, 25, "bold"), text_color=COLOR_GOLD).pack(pady=(180, 0))
        self.counter_lbl = ctk.CTkLabel(self.main_container, text="1000", font=(FONT_MAIN, 300, "bold"), text_color=COLOR_GREEN)
        self.counter_lbl.pack(expand=True)
        self.act_btn = ctk.CTkButton(self.main_container, text="ابدأ ", command=self.toggle_counter, width=500, height=110, font=(FONT_MAIN, 45, "bold"), fg_color=COLOR_PURPLE, corner_radius=55)
        self.act_btn.pack(pady=(0, 50))

    def toggle_counter(self):
        if not self.is_running:
            self.is_running = True
            self.act_btn.configure(text="إيقاف!", fg_color="#C0392B")
            self.update_counter()
        else:
            self.is_running = False
            self.process_result()

    def update_counter(self):
        if self.is_running and self.active_screen == "game":
            self.current_value = 1000 if self.current_value >= 3000 else self.current_value + 1
            self.counter_lbl.configure(text=str(self.current_value))
            self.after(7, self.update_counter)

    def process_result(self):
        won = (self.current_value == self.target_number)
        try:
            df_new = pd.DataFrame([{"الجوال": self.user_phone, "الرقم": self.current_value, "فاز": won, "التاريخ": datetime.now()}])
            if os.path.exists("log.xlsx"):
                df = pd.read_excel("log.xlsx")
                pd.concat([df, df_new]).to_excel("log.xlsx", index=False)
            else:
                df_new.to_excel("log.xlsx", index=False)
        except: pass

        if won: self.show_final_msg("✨ مبروك ✨\nلقد فزت معنا!")
        elif self.user_attempts < 3: self.show_retry_screen()
        else: self.show_final_msg("عذراً، استنفدت جميع محاولاتك!\nحظاً أوفر.")

    def show_retry_screen(self):
        self.clear_content()
        self.active_screen = "retry"
        ctk.CTkLabel(self.main_container, text=f"النتيجة: {self.current_value}", font=(FONT_MAIN, 40, "bold"), text_color="red").pack(pady=(300, 20))
        ctk.CTkLabel(self.main_container, text=f"باقي لك {3 - self.user_attempts} محاولة", font=(FONT_MAIN, 30), text_color=COLOR_PURPLE).pack()
        ctk.CTkButton(self.main_container, text="المحاولة التالية ", command=self.start_next_attempt, fg_color=COLOR_GREEN, font=(FONT_MAIN, 30, "bold"), height=80, width=400, corner_radius=40).pack(pady=40)

    def show_final_msg(self, msg):
        self.clear_content()
        self.active_screen = "msg"
        ctk.CTkLabel(self.main_container, text=msg, font=(FONT_MAIN, 45, "bold"), text_color=COLOR_PURPLE, justify="center").pack(pady=400)
        self.after(4000, self.show_welcome_screen)

    def on_space_pressed(self):
        if self.active_screen == "welcome": self.check_user()
        elif self.active_screen == "fact": self.show_tutorial()
        elif self.active_screen == "tutorial": self.start_next_attempt()
        elif self.active_screen == "game": self.toggle_counter()
        elif self.active_screen == "retry": self.start_next_attempt()

if __name__ == "__main__":
    app = KitchenZoneFinal()
    app.mainloop()