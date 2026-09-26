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
        "subtitle": "Trening poza boiskiem – siła, kondycja, mobilność i prewencja",
        "section1": "1. Dane zawodnika",
        "position": "Pozycja",
        "positions": ["Pitcher (miotacz)", "Catcher (łapacz)", "Infielder (wewnętrzny)", "Outfielder (zapolowy)"],
        "gender": "Płeć",
        "genders": ["Mężczyzna", "Kobieta"],
        "age": "Wiek",
        "height": "Wzrost (cm)",
        "weight": "Waga (kg)",
        "section2": "2. Cel i preferencje treningowe",
        "goal": "Główny cel treningowy",
        "goals": ["Ogólne zdrowie i samopoczucie", "Wzmocnienie mięśni", "Lepsza koordynacja i zwinność",
                  "Poprawa kondycji / wytrzymałości", "Prewencja kontuzji", "Zwiększenie mocy i eksplozywności"],
        "intensity": "Preferowana intensywność treningów",
        "intensities": ["Niska (regeneracyjna / techniczna)", "Średnia (zrównoważona)", "Wysoka (mocna / intensywna)"],
        "time": "Ile minut masz na trening w ciągu całego tygodnia?",
        "days": "W które dni grasz w baseball? (te dni będą lżejsze lub regeneracyjne)",
        "days_list": ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"],
        "equipment": "Dostępny sprzęt (zaznacz wszystko, co masz)",
        "equip_list": ["Resistance bands", "Medicine ball", "Weights / Gym", "Walking / Bike / Running"],
        "arm": "Stan Twojej ręki miotającej / rzucającej",
        "arm_options": ["Zdrowa / bez dolegliwości", "Lekko obolała / zmęczona", "W trakcie regeneracji / kontuzja", "Silne ograniczenia"],
        "button": "Wygeneruj plan treningowy",
        "success": "Twój spersonalizowany plan treningowy",
        "summary": "Podsumowanie",
        "focus": "Główny fokus",
        "weekly": "Propozycja tygodniowego planu",
        "notes": "Dodatkowe wskazówki",
        "disclaimer": "To uproszczony plan. Nie zastępuje konsultacji z trenerem lub fizjoterapeutą.",
        "info": "Wypełnij dane i kliknij przycisk, aby wygenerować plan.",
        "download_pdf": "Pobierz plan w PDF",
        "library": "Słownik ćwiczeń + filmiki (kliknij, żeby rozwinąć)",
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

# -------------------- SŁOWNIK ĆWICZEŃ --------------------
EXERCISES = {
    "Goblet / Front Squat": {
        "pl": "Przysiad z ciężarem trzymanym przy klatce piersiowej. Świetny na nogi i core, bezpieczniejszy dla kręgosłupa.",
        "en": "Squat holding a weight at chest level. Great for legs and core, spine-friendly.",
        "yt": "https://www.youtube.com/watch?v=zBV3ceGyAxw"
    },
    "Romanian Deadlift": {
        "pl": "Martwy ciąg rumuński – skupia się na tylnym łańcuchu (dwugłowe uda + pośladki). Biodra do tyłu, plecy proste.",
        "en": "Hip-hinge movement targeting hamstrings and glutes. Push hips back, keep back flat.",
        "yt": "https://www.youtube.com/watch?v=2SHsk9AzdjA"
    },
    "Bulgarian Split Squat": {
        "pl": "Przysiad bułgarski – jedna noga z tyłu na ławce. Buduje siłę i stabilność jednonóż.",
        "en": "Rear foot elevated split squat. Builds single-leg strength and balance.",
        "yt": "https://www.youtube.com/watch?v=o7yFuIR9XVU"
    },
    "Hip Thrust": {
        "pl": "Wypychanie bioder w górę z górną częścią pleców na ławce. Najlepsze ćwiczenie na pośladki.",
        "en": "Hip extension with upper back on a bench. Best glute builder.",
        "yt": "https://www.youtube.com/watch?v=SEdqd1n0cvg"
    },
    "Bodyweight Squat": {
        "pl": "Klasyczny przysiad z masą ciała. Podstawa siły nóg.",
        "en": "Classic bodyweight squat. Foundation of leg strength.",
        "yt": "https://www.youtube.com/watch?v=aclHkVaku9U"
    },
    "Reverse Lunges": {
        "pl": "Wykroki do tyłu – delikatniejsze dla kolan niż wykroki do przodu.",
        "en": "Step backward into a lunge. Kinder on the knees.",
        "yt": "https://www.youtube.com/watch?v=xr33x6zMQ9Q"
    },
    "Single-leg RDL": {
        "pl": "Martwy ciąg na jednej nodze – równowaga + tylny łańcuch.",
        "en": "Single-leg Romanian deadlift – balance + posterior chain.",
        "yt": "https://www.youtube.com/watch?v=4rE3sLq7Y4k"
    },
    "Glute Bridge": {
        "pl": "Mostek biodrowy – leżąc na plecach wypychasz biodra w górę.",
        "en": "Lying on your back, drive hips up by squeezing glutes.",
        "yt": "https://www.youtube.com/watch?v=OUgsA8XiM_g"
    },
    "Dead Bug": {
        "pl": "Leżąc na plecach naprzemiennie prostujesz przeciwległą rękę i nogę. Świetna stabilizacja core.",
        "en": "Lie on back, extend opposite arm and leg while keeping lower back flat. Excellent core control.",
        "yt": "https://www.youtube.com/watch?v=g_BYB0R-4Ws"
    },
    "Side Plank": {
        "pl": "Deska boczna – utrzymuj ciało w linii prostej na boku.",
        "en": "Hold body in a straight line on one side. Great for obliques.",
        "yt": "https://www.youtube.com/watch?v=XeN4pEZZJNI"
    },
    "Pallof Press": {
        "pl": "Antyrotacyjne ćwiczenie core – wypychasz linkę/bandę przed siebie i opierasz się skręcaniu.",
        "en": "Anti-rotation core exercise. Press band/cable straight out and resist twisting.",
        "yt": "https://www.youtube.com/watch?v=5_8d8vHgZvU"
    },
    "Band Face Pulls": {
        "pl": "Przyciąganie bandy do twarzy – wzmacnia tylne aktony barków i rotatory (prewencja urazów barku).",
        "en": "Pull band toward face. Strengthens rear delts and rotator cuff – key for shoulder health.",
        "yt": "https://www.youtube.com/watch?v=Wq-Td9UXRK8"
    },
    "Band External Rotations": {
        "pl": "Zewnętrzna rotacja barku z bandą – ochrona stożka rotatorów.",
        "en": "External rotation of the shoulder with band – protects the rotator cuff.",
        "yt": "https://www.youtube.com/watch?v=VjFVN0MBDh0"
    },
    "Band Rows": {
        "pl": "Wiosłowanie z bandą – buduje mięśnie pleców i stabilizację łopatki.",
        "en": "Band row – builds upper back and scapular stability.",
        "yt": "https://www.youtube.com/watch?v=GZbfZ0338Zo"
    },
    "Med Ball Rotational Throws": {
        "pl": "Rzuty piłką lekarską w rotacji – rozwija moc rotacyjną (ważne dla baseballu).",
        "en": "Rotational medicine ball throws – develops rotational power crucial for baseball.",
        "yt": "https://www.youtube.com/watch?v=1xqZf1zqZ2k"
    },
    "Med Ball Slams": {
        "pl": "Uderzenia piłką lekarską w podłogę – moc i eksplozywność całego ciała.",
        "en": "Slam the medicine ball into the ground – full-body power.",
        "yt": "https://www.youtube.com/watch?v=2xX4zQ3zqZ0"
    },
    "Dumbbell Shoulder Press": {
        "pl": "Wyciskanie hantli nad głowę – siła barków (ostrożnie przy problemach z ręką).",
        "en": "Overhead press with dumbbells – shoulder strength (careful with arm issues).",
        "yt": "https://www.youtube.com/watch?v=B-aVuyhvLNs"
    },
    "Bent-over Row": {
        "pl": "Wiosłowanie w opadzie – buduje grubość pleców.",
        "en": "Bent-over row – builds back thickness.",
        "yt": "https://www.youtube.com/watch?v=vT2GjY_Umpw"
    },
    "Push-ups": {
        "pl": "Klasyczne pompki – siła klatki, tricepsów i core.",
        "en": "Classic push-ups – chest, triceps and core strength.",
        "yt": "https://www.youtube.com/watch?v=IODxDxX7oi4"
    },
    "Inverted Rows": {
        "pl": "Podciąganie w poziomie (np. pod stołem) – zamiennik podciągania.",
        "en": "Horizontal pulling (under a table/bar) – great pull-up alternative.",
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

    if czas_tyg < 120:
        sesje = 2
    elif czas_tyg < 250:
        sesje = 3
    else:
        sesje = 4
    dlugosc = max(30, czas_tyg // sesje)

    # Fokus
    if lang == "Polski":
        focus = f"{pozycja} | Cel: {cel} | Intensywność: {intensywnosc}"
    else:
        focus = f"{pozycja} | Goal: {cel} | Intensity: {intensywnosc}"

    # Dobór ćwiczeń
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
    else:
        selected += ["Band Face Pulls"] if has_bands else []

    # Intensywność
    if "Niska" in intensywnosc or "Low" in intensywnosc:
        serie_info = "2 sets x 10-15 reps (light)" if lang == "English" else "2 serie x 10-15 powtórzeń (lekko)"
    elif "Wysoka" in intensywnosc or "High" in intensywnosc:
        serie_info = "4 sets x 5-8 reps (heavy)" if lang == "English" else "4 serie x 5-8 powtórzeń (ciężko)"
    else:
        serie_info = "3 sets x 8-12 reps" if lang == "English" else "3 serie x 8-12 powtórzeń"

    # ---------- WYŚWIETLENIE ----------
    st.success(t["success"])

    st.subheader(t["summary"])
    st.markdown(f"""
    - **{t['position']}:** {pozycja}  
    - **{t['age']} / {t['gender']}:** {wiek} / {plec}  
    - **{t['height']} / {t['weight']}:** {wzrost} cm / {waga} kg (BMI {bmi})  
    - **{t['goal']}:** {cel}  
    - **{t['intensity']}:** {intensywnosc}  
    - **Czas:** {czas_tyg} min/tydzień → {sesje} sesje × ~{dlugosc} min  
    - **Dni gry:** {', '.join(dni_gry) if dni_gry else '-'}  
    - **Stan ręki:** {stan_reki}
    """)

    st.subheader(t["focus"])
    st.info(focus)

    st.subheader(t["weekly"])
    all_days = t["days_list"]
    training_days = [d for d in all_days if d not in dni_gry][:sesje]
    if not training_days:
        training_days = all_days[:sesje]

    plan_for_pdf = []
    for i, day in enumerate(training_days):
        st.markdown(f"### {day} (~{dlugosc} min)")
        if i % 2 == 0:
            st.markdown(f"**Strength** – {serie_info}")
            for ex in selected[:6]:
                st.markdown(f"- {ex}")
                plan_for_pdf.append(f"{day}: {ex}")
        else:
            st.markdown("**Conditioning + Mobility**")
            if has_cardio:
                st.markdown("- Easy run / bike / walk 15-25 min")
            st.markdown("- Dynamic mobility + core work")
            plan_for_pdf.append(f"{day}: Conditioning + Mobility")

    if dni_gry:
        st.markdown("---")
        st.markdown(f"**Playing days ({', '.join(dni_gry)}):** only light mobility and recovery.")

    # ---------- SŁOWNIK ĆWICZEŃ ----------
    st.subheader(t["library"])
    for ex in selected:
        if ex in EXERCISES:
            data = EXERCISES[ex]
            with st.expander(f"▶ {ex}"):
                st.write(data["pl"] if lang == "Polski" else data["en"])
                st.markdown(f"[🎬 YouTube Tutorial]({data['yt']})")

    st.subheader(t["notes"])
    st.markdown("- Always warm up 8-12 minutes\n- Listen to your body, especially the arm\n- Sleep + protein = recovery")
    st.warning(t["disclaimer"])

    # ====================== PDF (zawsze po angielsku + ASCII) ======================
    class PDF(FPDF):
        def header(self):
            self.set_font("Helvetica", "B", 16)
            self.cell(0, 10, "Baseball Training Plan", ln=True, align="C")
            self.set_font("Helvetica", "", 10)
            self.cell(0, 8, datetime.now().strftime("%Y-%m-%d"), ln=True, align="C")
            self.ln(4)

        def footer(self):
            self.set_y(-15)
            self.set_font("Helvetica", "I", 8)
            self.cell(0, 10, f"Page {self.page_no()}", align="C")

    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", size=11)

    def clean(text):
        # usuwa polskie znaki żeby nie było błędów
        replacements = str.maketrans("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ", "acelnoszzACELNOSZZ")
        return str(text).translate(replacements)

    pdf.multi_cell(0, 7, clean(f"Position: {pozycja}"))
    pdf.multi_cell(0, 7, clean(f"Age / Gender: {wiek} / {plec}"))
    pdf.multi_cell(0, 7, clean(f"Height / Weight: {wzrost} cm / {waga} kg"))
    pdf.multi_cell(0, 7, clean(f"Goal: {cel}"))
    pdf.multi_cell(0, 7, clean(f"Intensity: {intensywnosc}"))
    pdf.multi_cell(0, 7, clean(f"Weekly time: {czas_tyg} min ({sesje} sessions)"))
    pdf.multi_cell(0, 7, clean(f"Playing days: {', '.join(dni_gry) if dni_gry else '-'}"))
    pdf.multi_cell(0, 7, clean(f"Arm condition: {stan_reki}"))
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.multi_cell(0, 7, "Weekly Plan:")
    pdf.set_font("Helvetica", size=11)
    for line in plan_for_pdf:
        pdf.multi_cell(0, 7, clean(f"- {line}"))
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.multi_cell(0, 7, "Exercises + Video Links:")
    pdf.set_font("Helvetica", size=10)
    for ex in selected:
        if ex in EXERCISES:
            pdf.multi_cell(0, 6, clean(f"{ex}"))
            pdf.multi_cell(0, 6, clean(f"  {EXERCISES[ex]['en']}"))
            pdf.multi_cell(0, 6, clean(f"  Video: {EXERCISES[ex]['yt']}"))
            pdf.ln(2)

    pdf.ln(4)
    pdf.set_font("Helvetica", "I", 9)
    pdf.multi_cell(0, 6, "This is a simplified plan. It does not replace advice from a coach or physiotherapist.")

    pdf_bytes = pdf.output()
    st.download_button(
        label=t["download_pdf"],
        data=pdf_bytes,
        file_name=f"baseball_plan_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

else:
    st.info(t["info"])
