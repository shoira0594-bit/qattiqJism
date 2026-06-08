import streamlit as st
import os
import cv2
import sys
import asyncio
import numpy as np

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

st.set_page_config(page_title="Laboratoriya Ishi ", page_icon="🔬", layout="centered")

# SIZ YUBORGAN YANGI 10 TA SAVOL VA TO'G'RI JAVOBLAR KALITI
questions = [
    {
        "id": 1, 
        "text": "1. Qattiq jismning solishtirma issiqlik sig’imini aniqlash laboratoriya ishida tashqi muhit bilan issiqlik almashinuvini kamaytirish uchun qaysi asbobdan foydalaniladi?", 
        "audio": "audio_files/savol_1.mp3",
        "options": ["A) Menzurka", "B) Kalorimetr", "D) Termometr"],
        "correct": "B) Kalorimetr"
    },
    {
        "id": 2, 
        "text": "2. Solishtirma issiqlik sig’imini hisoblash formulasida jism qabul qilgan yoki ajratgan issiqlik miqdori qaysi bosh harf bilan belgilanadi?", 
        "audio": "audio_files/savol_2.mp3",
        "options": ["A) Katta Q (Qyu) harfi bilan", "B) Katta T (Te) harfi bilan", "D) Kichik c (es) harfi bilan"],
        "correct": "A) Katta Q (Qyu) harfi bilan"
    },
    {
        "id": 3, 
        "text": "3. Xalqaro birliklar sistemasida moddaning solishtirma issiqlik sig’imi birligi qaysi javobda to’g’ri so’zlar bilan ko’rsatilgan?", 
        "audio": "audio_files/savol_3.mp3",
        "options": ["A) Joul bo’lingan kilogramm", "B) Nyuton ko’paytirilgan metr", "D) Joul bo’lingan kilogramm ko’paytirilgan gradus Selsiy"],
        "correct": "D) Joul bo’lingan kilogramm ko’paytirilgan gradus Selsiy"
    },
    {
        "id": 4, 
        "text": "4. Laboratoriya ishini bajarishda kalorimetr ichidagi suvga qizdirilgan qattiq jism tashlanganda qanday jarayon yuzaga keladi?", 
        "audio": "audio_files/savol_4.mp3",
        "options": ["A) Issiqlik muvozanati qaror topadi", "B) Suvning massasi kamayadi", "D) Jismning massasi ortadi", "E) Suv birdaniga qaynaydi"],
        "correct": "A) Issiqlik muvozanati qaror topadi"
    },
    {
        "id": 5, 
        "text": "5. Laboratoriya ishida jismning massasini aniqlash uchun qaysi o’lchov asbobidan foydalaniladi?", 
        "audio": "audio_files/savol_5.mp3",
        "options": ["A) Termometr", "B) Menzurka", "D) Laboratoriya tarozisi", "E) Chizg'ich"],
        "correct": "D) Laboratoriya tarozisi"
    },
    {
        "id": 6, 
        "text": "6. Laboratoriya ishida tajriba xatoligini kamaytirish va aniqroq natija olish uchun, qizdirilgan jismni qaynoq suvdan olgach kalorimetrga qanday o’tkazish kerak?", 
        "audio": "audio_files/savol_6.mp3",
        "options": ["A) Sekin va ehtiyotkorlik bilan o’tkazish kerak", "B) Juda tez, issiqlik yo’qolishiga ulgurmasdan o’tkazish kerak", "D) Jismni bir oz sovutib, keyin o’tkazish kerak"],
        "correct": "B) Juda tez, issiqlik yo’qolishiga ulgurmasdan o’tkazish kerak"
    },
    {
        "id": 7, 
        "text": "7. Menzurka yordamida suvning qaysi kattaligi o’lchanadi va keyinchalik zichlik orqali uning massasi hisoblanadi?", 
        "audio": "audio_files/savol_7.mp3",
        "options": ["A) Suvning temperaturasi", "B) Suvning hajmi", "D) Suvning og’irligi"],
        "correct": "B) Suvning hajmi"
    },
    {
        "id": 8, 
        "text": "8. Issiqlik balansi tenglamasiga ko’ra, yopiq sistemada issiq jism bergan issiqlik miqdori nimaga teng bo’ladi?", 
        "audio": "audio_files/savol_8.mp3",
        "options": ["A) Tashqi muhitga yo’qolgan energiyaga", "B) Sovuq suv va kalorimetr qabul qilgan issiqlik miqdoriga", "D) Jismning boshlang’ich temperaturasiga"],
        "correct": "B) Sovuq suv va kalorimetr qabul qilgan issiqlik miqdoriga"
    },
    {
        "id": 9, 
        "text": "9. Moddaning solishtirma issiqlik sig’imi deb nimaga aytiladi?", 
        "audio": "audio_files/savol_9.mp3",
        "options": ["A) Bir kilogramm moddani bir gradus Selsiyga qizdirish uchun zarur bo’lgan issiqlik miqdoriga", "B) Jismning to’liq erishi uchun ketadigan issiqlik miqdoriga", "D) Suyuqlikning bug’ga aylanishi uchun zarur bo’lgan energiyaga"],
        "correct": "A) Bir kilogramm moddani bir gradus Selsiyga qizdirish uchun zarur bo’lgan issiqlik miqdoriga"
    },
    {
        "id": 10, 
        "text": "10. Kalorimetr ichidagi suv va unga tashlangan issiq jism o’rtasida issiqlik almashinuvi jarayoni qachongacha davom etadi?", 
        "audio": "audio_files/savol_10.mp3",
        "options": ["A) Suv butunlay bug’lanib ketguncha davom etadi", "B) Jismning temperaturasi nol gradusga tushguncha davom etadi", "D) Suv va jismning temperaturalari tenglashib, issiqlik muvozanati qaror topguncha davom etadi"],
        "correct": "D) Suv va jismning temperaturalari tenglashib, issiqlik muvozanati qaror topguncha davom etadi"
    }
]

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_image" not in st.session_state:
    st.session_state.user_image = None
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# 1
