import streamlit as st
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="Baseball Training Plan", page_icon="⚾", layout="centered")

lang = st.radio("Language / Język", ["Polski", "English"], horizontal=True)

T = {
    "Polski": {
        "title": "⚾ Plan Treningowy dla Baseballistów",
        "subtitle": "Trening poza boiskiem",
        "section1": "1. Dane zawodnika",
        "position": "Pozycja",
        "positions": ["Pitcher (miotacz)", "Catcher (lapacz)", "Infielder (wewnetrzny)", "Outfielder (zapolowy)"],
        "gender": "Plec",
        "genders": ["Mezczyzna", "Kobieta"],
        "age": "Wiek",
        "height": "Wzrost (cm)",
        "weight": "Waga (kg)",
        "section2": "2. Cel i preferencje",
        "goal": "Glowny cel",
        "goals": ["Ogolne zdrowie", "Wzmocnienie miesni", "Lepsza koordynacja", "Poprawa kondycji", "Prewencja kontuzji", "Zwiekszenie mocy"],
        "intensity": "Intensywnosc",
        "intensities": ["Niska", "Srednia", "Wysoka"],
        "time": "Ile minut na trening w tygodniu?",
        "days": "Dni gry w baseball",
        "days_list": ["Poniedzialek", "Wtorek", "Sroda", "Czwartek", "Piatek", "Sobota", "Niedziela"],
        "equipment": "Dostepny sprzet",
        "equip_list": ["Resistance bands", "Medicine ball", "Weights / Gym", "Walking / Bike / Running"],
        "arm": "Stan reki",
        "arm_options": ["Zdrowa", "Lekko obolala", "W regeneracji", "Silne ograniczenia"],
        "button": "Wygeneruj plan",
        "success": "Plan wygenerowany",
        "summary": "Podsumowanie",
        "focus": "Fokus",
        "weekly": "Plan tygodniowy",
        "notes": "Wskazowki",
        "disclaimer": "To uproszczony plan. Skonsultuj z trenerem.",
        "info": "Wypelnij dane i kliknij przycisk.",
        "download_pdf": "Pobierz PDF",
        "library": "Slownik cwiczen + filmiki",
    },
    "English": {
        "title": "⚾ Baseball Off-Field Training Plan",
        "subtitle": "Strength, conditioning, mobility",
        "section1": "1. Player data",
        "position": "Position",
        "positions": ["Pitcher", "Catcher", "Infielder", "Outfielder"],
        "gender": "Gender",
        "genders": ["Male", "Female"],
        "age": "Age",
        "height": "Height (cm)",
        "weight": "Weight (kg)",
        "section2": "2. Goal & preferences",
        "goal": "Main goal",
        "goals": ["General health", "Muscle strengthening", "Better coordination", "Improve conditioning", "Injury prevention", "Increase power"],
        "intensity": "Intensity",
        "intensities": ["Low", "Medium", "High"],
        "time": "Minutes available per week",
        "days": "Baseball playing days",
        "days_list": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "equipment": "Available equipment",
        "equip_list": ["Resistance bands", "Medicine ball", "Weights / Gym", "Walking / Bike / Running"],
        "arm": "Arm condition",
        "arm_options": ["Healthy", "Slightly sore", "Recovering", "Significant limitations"],
        "button": "Generate plan",
        "success": "Plan generated",
        "summary": "Summary",
        "focus": "Focus",
        "weekly": "Weekly plan",
        "notes": "Notes",
        "disclaimer": "Simplified plan. Consult a coach.",
        "info": "Fill the form and click the button.",
        "download_pdf": "Download PDF",
        "library": "Exercise library + videos",
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
    "Goblet / Front Squat": {"pl": "Przysiad z ciezarrem przy klatce.", "en": "Squat holding weight at chest.", "yt": "https://www.youtube.com/watch?v=zBV3ceGyAxw"},
    "Romanian Deadlift": {"pl": "Martwy ciag rumunski.", "en": "Hip-hinge for hamstrings and glutes.", "yt": "https://www.youtube.com/watch?v=2SHsk9AzdjA"},
    "Bulgarian Split Squat": {"pl": "Przysiad bugarski.", "en": "Rear-foot elevated split squat.", "yt": "https://www.youtube.com/watch?v=o7yFuIR9XVU"},
    "Hip Thrust": {"pl": "Wypychanie bioder.", "en": "Hip extension for glutes.", "yt": "https://www.youtube.com/watch?v=SEdqd1n0cvg"},
    "Bodyweight Squat": {"pl": "Przysiad z masa ciala.", "en": "Classic bodyweight squat.", "yt": "https://www.youtube.com/watch?v=aclHkVaku9U"},
    "Reverse Lunges": {"pl": "Wykroki do tylu.", "en": "Step-back lunges.", "yt": "https://www.youtube.com/watch?v=xr33x6zMQ9Q"},
    "Single-leg RDL": {"pl": "Martwy ciag na jednej nodze.", "en": "Single-leg Romanian deadlift.", "yt": "https://www.youtube.com/watch?v=4rE3sLq7Y4k"},
    "Glute Bridge": {"pl": "Mostek biodrowy.", "en": "Glute bridge.", "yt": "https://www.youtube.com/watch?v=OUgsA8XiM_g"},
    "Dead Bug": {"pl": "Cwizenie Dead Bug.", "en": "Core control exercise.", "yt": "https://www.youtube.com/watch?v=g_BYB0R-4Ws"},
    "Side Plank": {"pl": "Deska boczna.", "en": "Side plank.", "yt": "https://www.youtube.com/watch?v=XeN4pEZZJNI"},
    "Pallof Press": {"pl": "Pallof Press.", "en": "Anti-rotation core press.", "yt": "https://www.youtube.com/watch?v=5_8d8vHgZvU"},
    "Band Face Pulls": {"pl": "Face Pulls z banda.", "en": "Band face pulls for shoulders.", "yt": "https://www.youtube.com/watch?v=Wq-Td9UXRK8"},
    "Band External Rotations": {"pl": "Zewnetrzna rotacja z banda.", "en": "Band external rotation.", "yt": "https://www.youtube.com/watch?v=VjFVN0MBDh0"},
    "Band Rows": {"pl": "Wioslowanie z banda.", "en": "Band rows.", "yt": "https://www.youtube.com/watch?v=GZbfZ0338Zo"},
    "Med Ball Rotational Throws": {"pl": "Rzuty med ball w rotacji.", "en": "Rotational med ball throws.", "yt": "https://www.youtube.com/watch?v=1xqZf1zqZ2k"},
    "Med Ball Slams": {"pl": "Uderzenia med ball.", "en": "Medicine ball slams.", "yt": "https://www.youtube.com/watch?v=2xX4zQ3zqZ0"},
    "Dumbbell Shoulder Press": {"pl": "Wyciskanie hantli.", "en": "Dumbbell overhead press.", "yt": "https://www.youtube.com/watch?v=B-aVuyhvLNs"},
    "Bent-over Row": {"pl": "Wioslowanie w opadzie.", "en": "Bent-over row.", "yt": "https://www.youtube.com/watch?v=vT2GjY_Umpw"},
    "Push-ups": {"pl": "Pompki.", "en": "Push-ups.", "yt": "https://www.youtube.com/watch?v=IODxDxX7oi4"},
    "Inverted Rows": {"pl": "Podciaganie w poziomie.", "en": "Inverted rows.", "yt": "https://www.youtube.com/watch?v=TgxS_9M7yEw"},
}

st.title(t["title"])
st.markdown(f"**{t['subtitle']}**")
st.divider()

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
st.header(t["section2"])

cel = st.selectbox(t["goal"], t["goals"])
intensywnosc = st.selectbox(t["intensity"], t["intensities"])
czas_tyg = st.number_input(t["time"], min_value=60, max_value=700, value=180, step=15)
dni_gry = st.multiselect(t["days"], t["days_list"])
sprzet = st.multiselect(t["equipment"], t["equip_list"])
stan_reki = st.selectbox(t["arm"], t["arm_options"])

st.divider()

if st.button(t["button"], type="primary", use_container_width=True):

    has_bands = "Resistance bands" in sprzet
    has_medball = "Medicine ball" in sprzet
    has_weights = "Weights / Gym" in sprzet
    has_cardio = "Walking / Bike / Running" in sprzet

    sesje = 2 if czas_tyg < 120 else (3 if czas_tyg < 250 else 4)
    dlugosc = max(30, czas_tyg // sesje)

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
        serie_info = "2 sets x 10-15 (light)"
    elif "Wysoka" in intensywnosc or "High" in intensywnosc:
        serie_info = "4 sets x 5-8 (heavy)"
    else:
        serie_info = "3 sets x 8-12"

    # --- Wyświetlenie w aplikacji ---
    st.success(t["success"])
    st.subheader(t["summary"])
    st.write(f"Pozycja: {pozycja} | Wiek: {wiek} | Plec: {plec}")
    st.write(f"Wzrost/Waga: {wzrost} cm / {waga} kg")
    st.write(f"Cel: {cel} | Intensywnosc: {intensywnosc}")
    st.write(f"Czas: {czas_tyg} min → {sesje} sesje x ~{dlugosc} min")
    st.write(f"Dni gry: {', '.join(dni_gry) if dni_gry else '-'}")
    st.write(f"Stan reki: {stan_reki}")

    st.subheader(t["weekly"])
    all_days = t["days_list"]
    training_days = [d for d in all_days if d not in dni_gry][:sesje] or all_days[:sesje]

    for i, day in enumerate(training_days):
        st.markdown(f"**{day} (~{dlugosc} min)**")
        if i % 2 == 0:
            st.write(f"Strength - {serie_info}")
            for ex in selected[:6]:
                st.write(f"- {ex}")
        else:
            st.write("Conditioning + Mobility")
            if has_cardio:
                st.write("- Easy run / bike / walk")
            st.write("- Mobility + core")

    st.subheader(t["library"])
    for ex in selected:
        if ex in EXERCISES:
            with st.expander(ex):
                st.write(EXERCISES[ex]["pl"] if lang == "Polski" else EXERCISES[ex]["en"])
                st.markdown(f"[YouTube]({EXERCISES[ex]['yt']})")

    st.warning(t["disclaimer"])

    # ====================== PDF - MAKSYMALNIE STABILNY ======================
    def safe(txt):
        return str(txt).encode("ascii", "ignore").decode("ascii")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(True, margin=15)
    pdf.set_margins(15, 15, 15)
    pdf.set_font("Helvetica", size=11)

    W = 180  # stała szerokość - kluczowe

    def write(txt, bold=False, size=11):
        pdf.set_font("Helvetica", "B" if bold else "", size)
        pdf.set_x(15)
        pdf.multi_cell(W, 7, safe(txt))

    write("BASEBALL TRAINING PLAN", bold=True, size=16)
    write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    write("")

    write("1. PLAYER INFORMATION", bold=True, size=13)
    write(f"Position: {safe(pozycja)}")
    write(f"Age / Gender: {wiek} / {safe(plec)}")
    write(f"Height / Weight: {wzrost} cm / {waga} kg")
    write(f"Goal: {safe(cel)}")
    write(f"Intensity: {safe(intensywnosc)}")
    write(f"Weekly time: {czas_tyg} min ({sesje} sessions)")
    write(f"Playing days: {safe(', '.join(dni_gry)) if dni_gry else 'None'}")
    write(f"Arm condition: {safe(stan_reki)}")
    write("")

    write("2. WEEKLY SCHEDULE", bold=True, size=13)
    for i, day in enumerate(training_days):
        day_en = DAY_MAP.get(day, safe(day))
        write(f"{day_en} (~{dlugosc} min)", bold=True)
        if i % 2 == 0:
            write(f"   Strength - {serie_info}")
            for ex in selected[:6]:
                write(f"   - {safe(ex)}")
        else:
            write("   Conditioning + Mobility")
            if has_cardio:
                write("   - Easy cardio 15-25 min")
            write("   - Mobility + core")
        write("")

    write("3. EXERCISES + VIDEOS", bold=True, size=13)
    for ex in selected:
        if ex in EXERCISES:
            write(safe(ex), bold=True)
            write(f"   {safe(EXERCISES[ex]['en'])}")
            write(f"   Video: {safe(EXERCISES[ex]['yt'])}")
            write("")

    write("4. NOTES", bold=True, size=13)
    write("- Always warm up 8-12 minutes")
    write("- Listen to your throwing arm")
    write("- Sleep and protein for recovery")
    write("- This is a simplified plan")

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
