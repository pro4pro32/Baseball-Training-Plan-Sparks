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
        "pl": "Przysiad z ciężarem trzymanym przy klatce. Świetny na nogi i core.",
        "en": "Squat holding weight at chest. Great for legs and core.",
        "yt": "https://www.youtube.com/watch?v=zBV3ceGyAxw"
    },
    "Romanian Deadlift": {
        "pl": "Martwy ciąg rumuński – tylny łańcuch (dwugłowe + pośladki).",
        "en": "Hip-hinge for hamstrings and glutes. Keep back flat.",
        "yt": "https://www.youtube.com/watch?v=2SHsk9AzdjA"
    },
    "Bulgarian Split Squat": {
        "pl": "Przysiad bułgarski – jedna noga z tyłu na ławce.",
        "en": "Rear-foot elevated split squat. Single-leg strength.",
        "yt": "https://www.youtube.com/watch?v=o7yFuIR9XVU"
    },
    "Hip Thrust": {
        "pl": "Wypychanie bioder – najlepsze na pośladki.",
        "en": "Hip extension. Best glute exercise.",
        "yt": "https://www.youtube.com/watch?v=SEdqd1n0cvg"
    },
    "Bodyweight Squat": {
        "pl": "Klasyczny przysiad z masą ciała.",
        "en": "Classic bodyweight squat.",
        "yt": "https://www.youtube.com/watch?v=aclHkVaku9U"
    },
    "Reverse Lunges": {
        "pl": "Wykroki do tyłu – delikatniejsze dla kolan.",
        "en": "Step-back lunges. Knee-friendly.",
        "yt": "https://www.youtube.com/watch?v=xr33x6zMQ9Q"
    },
    "Single-leg RDL": {
        "pl": "Martwy ciąg na jednej nodze.",
        "en": "Single-leg Romanian deadlift.",
        "yt": "https://www.youtube.com/watch?v=4rE3sLq7Y4k"
    },
    "Glute Bridge": {
        "pl": "Mostek biodrowy.",
        "en": "Glute bridge – lie on back and drive hips up.",
        "yt": "https://www.youtube.com/watch?v=OUgsA8XiM_g"
    },
    "Dead Bug": {
        "pl": "Leżąc na plecach naprzemiennie prostujesz rękę i nogę.",
        "en": "Core control: extend opposite arm and leg.",
        "yt": "https://www.youtube.com/watch?v=g_BYB0R-4Ws"
    },
    "Side Plank": {
        "pl": "Deska boczna.",
        "en": "Side plank – hold body in straight line.",
        "yt": "https://www.youtube.com/watch?v=XeN4pEZZJNI"
    },
    "Pallof Press": {
        "pl": "Antyrotacja core – wypychasz bandę/linkę przed siebie.",
        "en": "Anti-rotation core press.",
        "yt": "https://www.youtube.com/watch?v=5_8d8vHgZvU"
    },
    "Band Face Pulls": {
        "pl": "Przyciąganie bandy do twarzy – ochrona barku.",
        "en": "Band face pulls – rear delts + rotator cuff.",
        "yt": "https://www.youtube.com/watch?v=Wq-Td9UXRK8"
    },
    "Band External Rotations": {
        "pl": "Zewnętrzna rotacja barku z bandą.",
        "en": "Band external rotation for shoulder health.",
        "yt": "https://www.youtube.com/watch?v=VjFVN0MBDh0"
    },
    "Band Rows": {
        "pl": "Wiosłowanie z bandą.",
        "en": "Band rows – upper back.",
        "yt": "https://www.youtube.com/watch?v=GZbfZ0338Zo"
    },
    "Med Ball Rotational Throws": {
        "pl": "Rzuty piłką lekarską w rotacji.",
        "en": "Rotational medicine ball throws.",
        "yt": "https://www.youtube.com/watch?v=1xqZf1zqZ2k"
    },
    "Med Ball Slams": {
        "pl": "Uderzenia piłką lekarską w podłogę.",
        "en": "Medicine ball slams.",
        "yt": "https://www.youtube.com/watch?v=2xX4zQ3zqZ0"
    },
    "Dumbbell Shoulder Press": {
        "pl": "Wyciskanie hantli nad głowę.",
        "en": "Dumbbell overhead press.",
        "yt": "https://www.youtube.com/watch?v=B-aVuyhvLNs"
    },
    "Bent-over Row": {
        "pl": "Wiosłowanie w opadzie.",
        "en": "Bent-over row.",
        "yt": "https://www.youtube.com/watch?v=vT2GjY_Umpw"
    },
    "Push-ups": {
        "pl": "Pompki.",
        "en": "Push-ups.",
        "yt": "https://www.youtube.com/watch?v=IODxDxX7oi4"
    },
    "Inverted Rows": {
        "pl": "Podciąganie w poziomie.",
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
            st.markdown("- Dynamic mobility + core")
            plan_for_pdf.append(f"{day}: Conditioning + Mobility")

    if dni_gry:
        st.markdown("---")
        st.markdown(f"**Playing days ({', '.join(dni_gry)}):** only light mobility and recovery.")

    # Słownik
    st.subheader(t["library"])
    for ex in selected:
        if ex in EXERCISES:
            data = EXERCISES[ex]
            with st.expander(f"▶ {ex}"):
                st.write(data["pl"] if lang == "Polski" else data["en"])
                st.markdown(f"[🎬 YouTube]({data['yt']})")

    st.subheader(t["notes"])
    st.markdown("- Always warm up 8-12 min\n- Listen to your arm\n- Sleep + protein")
    st.warning(t["disclaimer"])

    # ====================== PDF – TYLKO ANGIELSKI + STAŁA SZEROKOŚĆ ======================
    class PDF(FPDF):
        def header(self):
            self.set_font("Helvetica", "B", 16)
            self.cell(0, 10, "Baseball Training Plan", align="C", new_x="LMARGIN", new_y="NEXT")
            self.set_font("Helvetica", "", 10)
            self.cell(0, 8, datetime.now().strftime("%Y-%m-%d"), align="C", new_x="LMARGIN", new_y="NEXT")
            self.ln(4)

        def footer(self):
            self.set_y(-15)
            self.set_font("Helvetica", "I", 8)
            self.cell(0, 10, f"Page {self.page_no()}", align="C")

    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", size=11)

    # Mapowanie na czysty angielski (żeby uniknąć jakichkolwiek problemów ze znakami)
    pos_map = {
        "Pitcher (miotacz)": "Pitcher", "Catcher (łapacz)": "Catcher",
        "Infielder (wewnętrzny)": "Infielder", "Outfielder (zapolowy)": "Outfielder",
        "Pitcher": "Pitcher", "Catcher": "Catcher", "Infielder": "Infielder", "Outfielder": "Outfielder"
    }
    gender_map = {"Mężczyzna": "Male", "Kobieta": "Female", "Male": "Male", "Female": "Female"}

    def safe(txt):
        return str(txt).encode("ascii", errors="ignore").decode("ascii")

    W = 190  # stała szerokość – kluczowe przeciwko błędowi

    pdf.multi_cell(W, 7, f"Position: {pos_map.get(pozycja, safe(pozycja))}")
    pdf.multi_cell(W, 7, f"Age / Gender: {wiek} / {gender_map.get(plec, safe(plec))}")
    pdf.multi_cell(W, 7, f"Height / Weight: {wzrost} cm / {waga} kg")
    pdf.multi_cell(W, 7, f"Goal: {safe(cel)}")
    pdf.multi_cell(W, 7, f"Intensity: {safe(intensywnosc)}")
    pdf.multi_cell(W, 7, f"Weekly time: {czas_tyg} min ({sesje} sessions)")
    pdf.multi_cell(W, 7, f"Playing days: {safe(', '.join(dni_gry) if dni_gry else '-')}")
    pdf.multi_cell(W, 7, f"Arm condition: {safe(stan_reki)}")
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 12)
    pdf.multi_cell(W, 7, "Weekly Plan:")
    pdf.set_font("Helvetica", size=11)
    for line in plan_for_pdf:
        pdf.multi_cell(W, 6, f"- {safe(line)}")

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.multi_cell(W, 7, "Exercises + Video Links:")
    pdf.set_font("Helvetica", size=10)
    for ex in selected:
        if ex in EXERCISES:
            pdf.multi_cell(W, 6, f"{ex}")
            pdf.multi_cell(W, 5, f"   {EXERCISES[ex]['en']}")
            pdf.multi_cell(W, 5, f"   Video: {EXERCISES[ex]['yt']}")
            pdf.ln(2)

    pdf.ln(4)
    pdf.set_font("Helvetica", "I", 9)
    pdf.multi_cell(W, 6, "This is a simplified plan. Consult a coach or physiotherapist for personalized advice.")

    pdf_bytes = bytes(pdf.output())

    st.download_button(
        label=t["download_pdf"],
        data=pdf_bytes,
        file_name=f"baseball_plan_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

else:
    st.info(t["info"])
