import streamlit as st
from fpdf import FPDF
from datetime import datetime

st.set_page_config(
    page_title="Baseball Training Plan / Plan Treningowy Baseball",
    page_icon="⚾",
    layout="centered"
)

# -------------------- JĘZYK --------------------
lang = st.radio("Language / Język", ["Polski", "English"], horizontal=True)

T = {
    "Polski": {
        "title": "⚾ Plan Treningowy dla Baseballistów",
        "subtitle": "Trening poza boiskiem - sila, kondycja, mobilnosc i prewencja",
        "section1": "1. Dane zawodnika",
        "position": "Pozycja",
        "positions": ["Pitcher (miotacz)", "Catcher (lapacz)", "Infielder (wewnetrzny)", "Outfielder (zapolowy)"],
        "gender": "Plec",
        "genders": ["Mezczyzna", "Kobieta"],
        "age": "Wiek",
        "height": "Wzrost (cm)",
        "weight": "Waga (kg)",
        "section2": "2. Cel i preferencje treningowe",
        "goal": "Glowny cel treningowy",
        "goals": ["Ogolne zdrowie i samopoczucie", "Wzmocnienie miesni", "Lepsza koordynacja i zwinnosc",
                  "Poprawa kondycji / wytrzymalosci", "Prewencja kontuzji", "Zwiekszenie mocy i eksplozywnosci"],
        "intensity": "Preferowana intensywnosc treningow",
        "intensities": ["Niska (regeneracyjna / techniczna)", "Srednia (zrownowazona)", "Wysoka (mocna / intensywna)"],
        "time": "Ile minut masz na trening w ciagu calego tygodnia?",
        "days": "W ktore dni grasz w baseball? (te dni beda lzejsze lub regeneracyjne)",
        "days_list": ["Poniedzialek", "Wtorek", "Sroda", "Czwartek", "Piatek", "Sobota", "Niedziela"],
        "equipment": "Dostepny sprzet (zaznacz wszystko, co masz)",
        "equip_list": ["Resistance bands", "Medicine ball", "Weights / Gym", "Walking / Bike / Running"],
        "arm": "Stan Twojej reki miotajacej / rzucajacej",
        "arm_options": ["Zdrowa / bez dolegliwosci", "Lekko obolala / zmeczona", "W trakcie regeneracji / kontuzja", "Silne ograniczenia"],
        "button": "Wygeneruj plan treningowy",
        "success": "Twoj spersonalizowany plan treningowy",
        "summary": "Podsumowanie",
        "focus": "Glowny fokus",
        "weekly": "Propozycja tygodniowego planu",
        "notes": "Dodatkowe wskazowki",
        "disclaimer": "To uproszczony plan. Nie zastepuje konsultacji z trenerem lub fizjoterapeuta.",
        "info": "Wypelnij dane i kliknij przycisk, aby wygenerowac plan.",
        "download_pdf": "Pobierz plan w PDF",
        "library": "Slownik cwiczen + filmiki (kliknij, zeby rozwinac)",
    },
    "English": {
        "title": "⚾ Baseball Off-Field Training Plan",
        "subtitle": "Strength, conditioning, mobility & injury prevention",
        "section1": "1. Player data",
        "position": "Position",
        "positions": ["Pitcher", "Catcher", "Infielder", "Outfielder"],
        "gender": "Gender",
        "genders": ["Male", "Female"],
        "age": "Age",
        "height": "Height (cm)",
        "weight": "Weight (kg)",
        "section2": "2. Goal & training preferences",
        "goal": "Main training goal",
        "goals": ["General health & well-being", "Muscle strengthening", "Better coordination & agility",
                  "Improve conditioning / endurance", "Injury prevention", "Increase power & explosiveness"],
        "intensity": "Preferred training intensity",
        "intensities": ["Low (recovery / technical)", "Medium (balanced)", "High (hard / intense)"],
        "time": "How many minutes do you have for training per week?",
        "days": "Which days do you play baseball? (these days will be lighter / recovery)",
        "days_list": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "equipment": "Available equipment (select all that apply)",
        "equip_list": ["Resistance bands", "Medicine ball", "Weights / Gym", "Walking / Bike / Running"],
        "arm": "Condition of your throwing arm",
        "arm_options": ["Healthy / no issues", "Slightly sore / fatigued", "Recovering / injury", "Significant limitations"],
        "button": "Generate training plan",
        "success": "Your personalized training plan",
        "summary": "Summary",
        "focus": "Main focus",
        "weekly": "Suggested weekly plan",
        "notes": "Additional notes",
        "disclaimer": "This is a simplified plan. It does not replace advice from a coach or physiotherapist.",
        "info": "Fill in the data and click the button to generate the plan.",
        "download_pdf": "Download plan as PDF",
        "library": "Exercise library + videos (click to expand)",
    }
}

t = T[lang]

DAY_MAP = {
    "Poniedzialek": "Monday", "Wtorek": "Tuesday", "Sroda": "Wednesday",
    "Czwartek": "Thursday", "Piatek": "Friday", "Sobota": "Saturday", "Niedziela": "Sunday",
    "Monday": "Monday", "Tuesday": "Tuesday", "Wednesday": "Wednesday",
    "Thursday": "Thursday", "Friday": "Friday", "Saturday": "Saturday", "Sunday": "Sunday"
}

EXERCISES = {
    "Goblet / Front Squat": {
        "pl": "Przysiad z ciezarrem trzymanym przy klatce. Swietny na nogi i core.",
        "en": "Squat holding weight at chest. Great for legs and core.",
        "yt": "https://www.youtube.com/watch?v=zBV3ceGyAxw"
    },
    "Romanian Deadlift": {
        "pl": "Martwy ciag rumunski - tylny lancuch (dwuglowe + posladki).",
        "en": "Hip-hinge for hamstrings and glutes. Keep back flat.",
        "yt": "https://www.youtube.com/watch?v=2SHsk9AzdjA"
    },
    "Bulgarian Split Squat": {
        "pl": "Przysiad bugarski - jedna noga z tylu na lawce.",
        "en": "Rear-foot elevated split squat. Single-leg strength.",
        "yt": "https://www.youtube.com/watch?v=o7yFuIR9XVU"
    },
    "Hip Thrust": {
        "pl": "Wypychanie bioder - najlepsze na posladki.",
        "en": "Hip extension. Best glute exercise.",
        "yt": "https://www.youtube.com/watch?v=SEdqd1n0cvg"
    },
    "Bodyweight Squat": {
        "pl": "Klasyczny przysiad z masa ciala.",
        "en": "Classic bodyweight squat.",
        "yt": "https://www.youtube.com/watch?v=aclHkVaku9U"
    },
    "Reverse Lunges": {
        "pl": "Wykroki do tylu - delikatniejsze dla kolan.",
        "en": "Step-back lunges. Knee-friendly.",
        "yt": "https://www.youtube.com/watch?v=xr33x6zMQ9Q"
    },
    "Single-leg RDL": {
        "pl": "Martwy ciag na jednej nodze.",
        "en": "Single-leg Romanian deadlift.",
        "yt": "https://www.youtube.com/watch?v=4rE3sLq7Y4k"
    },
    "Glute Bridge": {
        "pl": "Mostek biodrowy.",
        "en": "Glute bridge - lie on back and drive hips up.",
        "yt": "https://www.youtube.com/watch?v=OUgsA8XiM_g"
    },
    "Dead Bug": {
        "pl": "Lezac na plecach naprzemiennie prostujesz reke i noge.",
        "en": "Core control: extend opposite arm and leg.",
        "yt": "https://www.youtube.com/watch?v=g_BYB0R-4Ws"
    },
    "Side Plank": {
        "pl": "Deska boczna.",
        "en": "Side plank - hold body in straight line.",
        "yt": "https://www.youtube.com/watch?v=XeN4pEZZJNI"
    },
    "Pallof Press": {
        "pl": "Antyrotacja core - wypychasz bande/linke przed siebie.",
        "en": "Anti-rotation core press.",
        "yt": "https://www.youtube.com/watch?v=5_8d8vHgZvU"
    },
    "Band Face Pulls": {
        "pl": "Przyciaganie bandy do twarzy - ochrona barku.",
        "en": "Band face pulls - rear delts + rotator cuff.",
        "yt": "https://www.youtube.com/watch?v=Wq-Td9UXRK8"
    },
    "Band External Rotations": {
        "pl": "Zewnetrzna rotacja barku z banda.",
        "en": "Band external rotation for shoulder health.",
        "yt": "https://www.youtube.com/watch?v=VjFVN0MBDh0"
    },
    "Band Rows": {
        "pl": "Wioslowanie z banda.",
        "en": "Band rows - upper back.",
        "yt": "https://www.youtube.com/watch?v=GZbfZ0338Zo"
    },
    "Med Ball Rotational Throws": {
        "pl": "Rzuty pilka lekarska w rotacji.",
        "en": "Rotational medicine ball throws.",
        "yt": "https://www.youtube.com/watch?v=1xqZf1zqZ2k"
    },
    "Med Ball Slams": {
        "pl": "Uderzenia pilka lekarska w podloge.",
        "en": "Medicine ball slams.",
        "yt": "https://www.youtube.com/watch?v=2xX4zQ3zqZ0"
    },
    "Dumbbell Shoulder Press": {
        "pl": "Wyciskanie hantli nad glowe.",
        "en": "Dumbbell overhead press.",
        "yt": "https://www.youtube.com/watch?v=B-aVuyhvLNs"
    },
    "Bent-over Row": {
        "pl": "Wioslowanie w opadzie.",
        "en": "Bent-over row.",
        "yt": "https://www.youtube.com/watch?v=vT2GjY_Umpw"
    },
    "Push-ups": {
        "pl": "Pompki.",
        "en": "Push-ups.",
        "yt": "https://www.youtube.com/watch?v=IODxDxX7oi4"
    },
    "Inverted Rows": {
        "pl": "Podciaganie w poziomie.",
        "en": "Inverted rows.",
        "yt": "https://www.youtube.com/watch?v=TgxS_9M7yEw"
    },
}

st.title(t["title"])
st.markdown(f"**{t['subtitle']}**")
st.divider()

# ====================== SEKCJA 1 ======================
st.header(t["section1"])

col1, col2 = st.columns(2)
with col1:
    pozycja = st.selectbox(t["position"], t["positions"])
    plec = st.selectbox(t["gender"], t["genders"])
    wiek = st.number_input(t["age"], min_value=12, max_value=55, value=20)

with col2:
    wzrost = st.number_input(t["height"], min_value=140, max_value=220, value=180)
    waga = st.number_input(t["weight"], min_value=40, max_value=150, value=75)

st.divider()

# ====================== SEKCJA 2 ======================
st.header(t["section2"])

cel = st.selectbox(t["goal"], t["goals"])
intensywnosc = st.selectbox(t["intensity"], t["intensities"])
czas_tyg = st.number_input(t["time"], min_value=60, max_value=700, value=180, step=15)
dni_gry = st.multiselect(t["days"], t["days_list"])
sprzet = st.multiselect(t["equipment"], t["equip_list"])
stan_reki = st.selectbox(t["arm"], t["arm_options"])

st.divider()

if st.button(t["button"], type="primary", use_container_width=True):

    bmi = round(waga / ((wzrost / 100) ** 2), 1)
    has_bands = "Resistance bands" in sprzet
    has_medball = "Medicine ball" in sprzet
    has_weights = "Weights / Gym" in sprzet
    has_cardio = "Walking / Bike / Running" in sprzet

    sesje = 2 if czas_tyg < 120 else (3 if czas_tyg < 250 else 4)
    dlugosc = max(30, czas_tyg // sesje)

    focus = f"{pozycja} | {cel} | {intensywnosc}"

    arm_bad = stan_reki in t["arm_options"][2:]
    selected = []

    if has_weights:
        selected += ["Goblet / Front Squat", "Romanian Deadlift", "Bulgarian Split Squat", "Hip Thrust"]
    else:
        selected += ["Bodyweight Squat", "Reverse Lunges", "Single-leg RDL", "Glute Bridge"]

    selected += ["Dead Bug", "Side Plank", "Pallof Press"]

    if not arm_bad:
        if has_weights:
            selected += ["Dumbbell Shoulder Press", "Bent-over Row"]
        if has_bands:
            selected += ["Band Face Pulls", "Band External Rotations", "Band Rows"]
        if has_medball:
            selected += ["Med Ball Rotational Throws", "Med Ball Slams"]
        if not has_weights and not has_bands:
            selected += ["Push-ups", "Inverted Rows"]
    elif has_bands:
        selected += ["Band Face Pulls", "Band External Rotations"]

    if "Niska" in intensywnosc or "Low" in intensywnosc:
        serie_info = "2 sets x 10-15 reps (light)"
    elif "Wysoka" in intensywnosc or "High" in intensywnosc:
        serie_info = "4 sets x 5-8 reps (heavy)"
    else:
        serie_info = "3 sets x 8-12 reps"

    # ---------- WYŚWIETLENIE ----------
    st.success(t["success"])

    st.subheader(t["summary"])
    st.markdown(f"""
    - **{t['position']}:** {pozycja}  
    - **{t['age']} / {t['gender']}:** {wiek} / {plec}  
    - **{t['height']} / {t['weight']}:** {wzrost} cm / {waga} kg (BMI {bmi})  
    - **{t['goal']}:** {cel}  
    - **{t['intensity']}:** {intensywnosc}  
    - **Czas:** {czas_tyg} min → {sesje} sesje × ~{dlugosc} min  
    - **Dni gry:** {', '.join(dni_gry) if dni_gry else '-'}  
    - **Stan ręki:** {stan_reki}
    """)

    st.subheader(t["focus"])
    st.info(focus)

    st.subheader(t["weekly"])
    all_days = t["days_list"]
    training_days = [d for d in all_days if d not in dni_gry][:sesje] or all_days[:sesje]

    for i, day in enumerate(training_days):
        st.markdown(f"### {day} (~{dlugosc} min)")
        if i % 2 == 0:
            st.markdown(f"**Strength** - {serie_info}")
            for ex in selected[:6]:
                st.markdown(f"- {ex}")
        else:
            st.markdown("**Conditioning + Mobility**")
            if has_cardio:
                st.markdown("- Easy run / bike / walk 15-25 min")
            st.markdown("- Dynamic mobility + core")

    if dni_gry:
        st.markdown("---")
        st.markdown(f"**Playing days ({', '.join(dni_gry)}):** only light mobility and recovery.")

    st.subheader(t["library"])
    for ex in selected:
        if ex in EXERCISES:
            data = EXERCISES[ex]
            with st.expander(f"▶ {ex}"):
                st.write(data["pl"] if lang == "Polski" else data["en"])
                st.markdown(f"[YouTube Tutorial]({data['yt']})")

    st.subheader(t["notes"])
    st.markdown("- Always warm up 8-12 min\n- Listen to your arm\n- Sleep + protein")
    st.warning(t["disclaimer"])

    # ====================== PDF ======================
    def safe(text):
        # Usuwa wszystko poza podstawowymi znakami ASCII
        text = str(text)
        text = text.replace("–", "-").replace("—", "-").replace("„", '"').replace("”", '"')
        return text.encode("ascii", errors="ignore").decode("ascii")

    class PDF(FPDF):
        def header(self):
            self.set_font("Helvetica", "B", 18)
            self.cell(0, 12, "Baseball Training Plan", align="C", new_x="LMARGIN", new_y="NEXT")
            self.set_font("Helvetica", "", 10)
            self.cell(0, 8, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", align="C", new_x="LMARGIN", new_y="NEXT")
            self.ln(4)
            self.set_draw_color(160, 160, 160)
            self.line(12, self.get_y(), 198, self.get_y())
            self.ln(8)

        def footer(self):
            self.set_y(-15)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(110, 110, 110)
            self.cell(0, 10, f"Page {self.page_no()}/{{nb}} | Amateur Baseball Club", align="C")

        def section_title(self, title):
            self.set_font("Helvetica", "B", 13)
            self.cell(0, 9, title, new_x="LMARGIN", new_y="NEXT")
            self.set_draw_color(50, 50, 50)
            self.line(12, self.get_y(), 75, self.get_y())
            self.ln(5)

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()
    pdf.set_margins(12, 12, 12)

    # 1. PLAYER INFO
    pdf.section_title("1. PLAYER INFORMATION")

    pos_en = {
        "Pitcher (miotacz)": "Pitcher", "Catcher (lapacz)": "Catcher",
        "Infielder (wewnetrzny)": "Infielder", "Outfielder (zapolowy)": "Outfielder",
        "Pitcher": "Pitcher", "Catcher": "Catcher", "Infielder": "Infielder", "Outfielder": "Outfielder"
    }.get(pozycja, "Player")

    gender_en = {"Mezczyzna": "Male", "Kobieta": "Female", "Male": "Male", "Female": "Female"}.get(plec, "Male")

    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 7, f"Position:          {pos_en}")
    pdf.multi_cell(0, 7, f"Age / Gender:      {wiek} / {gender_en}")
    pdf.multi_cell(0, 7, f"Height / Weight:   {wzrost} cm / {waga} kg")
    pdf.multi_cell(0, 7, f"Main Goal:         {safe(cel)}")
    pdf.multi_cell(0, 7, f"Intensity:         {safe(intensywnosc)}")
    pdf.multi_cell(0, 7, f"Weekly Time:       {czas_tyg} min ({sesje} sessions)")
    days_en = ", ".join([DAY_MAP.get(d, safe(d)) for d in dni_gry]) if dni_gry else "None"
    pdf.multi_cell(0, 7, f"Playing Days:      {days_en}")
    pdf.multi_cell(0, 7, f"Arm Condition:     {safe(stan_reki)}")
    pdf.ln(4)

    # 2. FOCUS
    pdf.section_title("2. TRAINING FOCUS")
    pdf.multi_cell(0, 7, safe(focus))
    pdf.ln(3)

    # 3. WEEKLY SCHEDULE
    pdf.section_title("3. WEEKLY SCHEDULE")

    for i, day in enumerate(training_days):
        day_en = DAY_MAP.get(day, safe(day))
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 8, f"{day_en}  (~{dlugosc} min)", new_x="LMARGIN", new_y="NEXT")

        pdf.set_font("Helvetica", size=10)
        if i % 2 == 0:
            pdf.multi_cell(0, 6, f"   Type: Strength  |  {serie_info}")
            for ex in selected[:6]:
                pdf.multi_cell(0, 5.5, f"   - {safe(ex)}")
        else:
            pdf.multi_cell(0, 6, "   Type: Conditioning + Mobility")
            if has_cardio:
                pdf.multi_cell(0, 5.5, "   - Easy run / bike / walk 15-25 min")
            pdf.multi_cell(0, 5.5, "   - Dynamic mobility + core work")
        pdf.ln(3)

    if dni_gry:
        pdf.set_font("Helvetica", "I", 10)
        pdf.multi_cell(0, 6, f"Note: On playing days ({days_en}) do only light mobility and recovery.")
        pdf.ln(3)

    # 4. EXERCISES
    pdf.section_title("4. EXERCISE LIBRARY + VIDEO LINKS")

    for ex in selected:
        if ex in EXERCISES:
            pdf.set_font("Helvetica", "B", 10)
            pdf.multi_cell(0, 6, safe(ex))
            pdf.set_font("Helvetica", size=9)
            pdf.multi_cell(0, 5, f"   {safe(EXERCISES[ex]['en'])}")
            pdf.set_text_color(0, 70, 160)
            pdf.multi_cell(0, 5, f"   Video: {safe(EXERCISES[ex]['yt'])}")
            pdf.set_text_color(0, 0, 0)
            pdf.ln(2)

    pdf.ln(3)

    # 5. NOTES
    pdf.section_title("5. IMPORTANT NOTES")
    pdf.set_font("Helvetica", size=10)
    pdf.multi_cell(0, 6, "- Always perform 8-12 minutes of dynamic warm-up.")
    pdf.multi_cell(0, 6, "- Listen carefully to your throwing arm.")
    pdf.multi_cell(0, 6, "- Prioritize sleep and protein for recovery.")
    pdf.multi_cell(0, 6, "- This is a general plan. Consult a coach or physiotherapist when needed.")

    pdf_bytes = bytes(pdf.output())

    st.download_button(
        label=t["download_pdf"],
        data=pdf_bytes,
        file_name=f"baseball_plan_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

else:
    st.info(t["info"])
