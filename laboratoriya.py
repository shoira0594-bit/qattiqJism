import streamlit as st
import os
import cv2
import sys
import asyncio
import numpy as np

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

st.set_page_config(page_title="Laboratoriya Ishi Tizimi", page_icon="🔬", layout="centered")

# SAVOLLAR RO'YXATI (AUDIOLAR PAPKASIZ, TO'G'RIDAN-TO'G'RI BOSH SAHIFADA)
questions = [
    {
        "id": 1, 
        "text": "1. Qattiq jismning solishtirma issiqlik sig’imini anixlash laboratoriya ishida tashqi muhit bilan issiqlik almashinuvini kamaytirish uchun qaysi asbobdan foydalaniladi?", 
        "audio": "savol_1.mp3",
        "options": ["A) Voltmetr", "B) Kalorimetr", "C) Termometr", "D) Ampermetr"],
        "correct": "B) Kalorimetr"
    },
    {
        "id": 2, 
        "text": "2. Solishtirma issiqlik sig’imini hisoblash formulasida jism qabul qilgan yoki ajratgan issiqlik miqdori qaysi bosh harf bilan belgilanadi?", 
        "audio": "savol_2.mp3",
        "options": ["A) m", "B) T", "C) c", "D) Q"],
        "correct": "D) Q"
    },
    {
        "id": 3, 
        "text": "3. Xalqaro birliklar sistemasida moddaning solishtirma issiqlik sig’imi birligi qaysi javobda to’g’ri so’zlar bilan ko’rsatilgan?", 
        "audio": "savol_3.mp3",
        "options": ["A) Joul taqsim kilogramm ko'paytirilgan Kelvin", "B) Nyuton taqsim metr", "C) Watt taqsim sekund", "D) Kaloriya taqsim gradus"],
        "correct": "A) Joul taqsim kilogramm ko'paytirilgan Kelvin"
    },
    {
        "id": 4, 
        "text": "4. Laboratoriya ishini bajarishda kalorimetr ichidagi suvga qizdirilgan qattiq jism tashlanganda qanday jarayon yuzaga keladi?", 
        "audio": "savol_4.mp3",
        "options": ["A) Mexanik to'qnashuv", "B) Issiqlik almashinuvi (balansi)", "C) Kimyoviy reaksiya", "D) Modda parchalanishi"],
        "correct": "B) Issiqlik almashinuvi (balansi)"
    },
    {
        "id": 5, 
        "text": "5. Laboratoriya ishida jismning massasini aniqlash uchun qaysi o’lchov asbobidan foydalaniladi?", 
        "audio": "savol_5.mp3",
        "options": ["A) Menzurka", "B) Laboratoriya tarozi", "C) Lineyka", "D) Sekundomer"],
        "correct": "B) Laboratoriya tarozi"
    },
    {
        "id": 6, 
        "text": "6. Laboratoriya ishida tajriba xatoligini kamaytirish va aniqroq natija olish uchun, qizdirilgan jismni qaynoq suvdan olgach kalorimetrga qanday o’tkazish kerak?", 
        "audio": "savol_6.mp3",
        "options": ["A) Sekin, 5 daqiqa kutib", "B) Iloji boricha tez va chaqqonlik bilan", "C) Suvini yaxshilab quritib keyin", "D) Muzlatib keyin"],
        "correct": "B) Iloji boricha tez va chaqqonlik bilan"
    },
    {
        "id": 7, 
        "text": "7. Menzurka yordamida suvning qaysi kattaligi o’lchanadi va keyinchalik zichlik orqali uning massasi hisoblanadi?", 
        "audio": "savol_7.mp3",
        "options": ["A) Temperaturasi", "B) Massasi", "C) Hajmi", "D) Zichligi"],
        "correct": "C) Hajmi"
    },
    {
        "id": 8, 
        "text": "8. Issiqlik balansi tenglamasiga ko’ra, yopiq sistemada issiq jism bergan issiqlik miqdori nimaga teng bo’ladi?", 
        "audio": "savol_8.mp3",
        "options": ["A) Sovuq jism olgan issiqlik miqdoriga", "B) Atrofga yo'qolgan energiyaga", "C) Jismning ichki energiyasiga", "D) Nolga"],
        "correct": "A) Sovuq jism olgan issiqlik miqdoriga"
    },
    {
        "id": 9, 
        "text": "9. Moddaning solishtirma issiqlik sig’imi deb nimaga aytiladi?", 
        "audio": "savol_9.mp3",
        "options": ["A) 1 kg moddani 1 Kelvinga qizdirish uchun kerak bo'lgan issiqlik miqdoriga", "B) Jismni eritish uchun ketadigan energiyaga", "C) Suyuqlikning qaynash temperaturasiga", "D) Moddaning og'irligiga"],
        "correct": "A) 1 kg moddani 1 Kelvinga qizdirish uchun kerak bo'lgan issiqlik miqdoriga"
    },
    {
        "id": 10, 
        "text": "10. Kalorimetr ichidagi suv va unga tashlangan issiq jism o’rtasida issiqlik almashinuvi jarayoni qachongacha davom etadi?", 
        "audio": "savol_10.mp3",
        "options": ["A) Suv qaynab ketguncha", "B) Jism butunlay erib ketguncha", "C) Tizimda issiqlik muvozanati (temperaturalar tenglashguncha) qaror topguncha", "D) 10 daqiqa o'tguncha"],
        "correct": "C) Tizimda issiqlik muvozanati (temperaturalar tenglashguncha) qaror topguncha"
    }
]

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_image" not in st.session_state:
    st.session_state.user_image = None
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# 1-BOSQICH: RO'YXATDAN O'TISH
if not st.session_state.authenticated:
    st.title("🔬 Ro'yxatdan o'tish va Face ID")
    ism = st.text_input("Ismingizni kiriting:")
    familiya = st.text_input("Familiyangizni kiriting:")
    sinf = st.text_input("Sinfingizni kiriting:")
    
    st.write("📸 Shaxsingizni tasdiqlash uchun 'Take Photo' tugmasini bosing:")
    img_file = st.camera_input("Face ID tekshiruvi")
    
    if img_file is not None:
        if ism and familiya and sinf:
            bytes_data = img_file.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            
            st.session_state.authenticated = True
            st.session_state.user_image = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
            st.session_state.student_info = f"{ism} {familiya}, {sinf}-sinf"
            st.success("✅ Face ID muvaffaqiyatli yakunlandi!")
            st.rerun()
        else:
            st.warning("Iltimos, rasmdan oldin ism, familiya va sinfingizni to'ldiring!")

# 2-BOSQICH: NAZORAT SAVOLLARI
else:
    st.title("📝 Laboratoriya Ishi: Nazorat Savollari")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.info(f"👤 O'quvchi: {st.session_state.student_info}")
    with col2:
        if st.session_state.user_image is not None:
            st.image(st.session_state.user_image, caption="Face ID rasmi", use_container_width=True)
            
    st.markdown("---")
    
    for q in questions:
        st.markdown(f"### {q['text']}")
        if os.path.exists(q["audio"]):
            st.audio(q["audio"])
        else:
            st.warning(f"⚠️ Audio topilmadi: {q['audio']}")
        
        if not st.session_state.submitted:
            st.radio("To'g'ri javobni belgilang:", q["options"], key=f"q_{q['id']}")
        else:
            selected = st.session_state.get(f"q_{q['id']}", "Belgilanmagan")
            st.write(f"Sizning javobingiz: **{selected}**")
            if selected == q["correct"]:
                st.success("🟢 Barakalla! To'g'ri javob berdingiz.")
            else:
                st.error(f"🔴 Noto'g'ri. To'g'ri javob: **{q['correct']}**")
        st.markdown("---")
        
    if not st.session_state.submitted:
        if st.button("Natijalarni yakunlash va yuborish", type="primary"):
            st.session_state.submitted = True
            st.rerun()
    else:
        correct_count = 0
        for q in questions:
            ans = st.session_state.get(f"q_{q['id']}", "")
            if ans == q["correct"]:
                correct_count += 1
                
        st.sidebar.title("📊 Umumiy Natija")
        st.sidebar.metric(label="To'g'ri javoblar", value=f"{correct_count} / {len(questions)}")
        foiz = (correct_count / len(questions)) * 100
        st.sidebar.metric(label="Ko'rsatkich", value=f"{int(foiz)}%")
        
        if foiz >= 80:
            st.sidebar.balloons()
            st.sidebar.success("Ajoyib natija! 🌟")
        else:
            st.sidebar.warning("Yana biroz harakat qilish kerak! 📚")

        if st.sidebar.button("Qaytadan urinish"):
            st.session_state.submitted = False
            st.rerun()
