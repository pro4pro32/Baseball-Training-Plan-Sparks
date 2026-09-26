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
        "positions": ["Pitcher (miotacz)", "Catcher (łapacz)", "Infielder (wewnętrzny)", "Outfielder (zapolowy)"],
        "gender": "Płeć",
        "genders": ["Mężczyzna", "Kobieta"],
        "age": "Wiek",
        "height": "Wzrost (cm)",
        "weight": "Waga (kg)",
        "section2": "2. Cel i preferencje",
        "goal": "Główny cel",
        "goals": ["Ogólne zdrowie", "Wzmocnienie mięśni", "Lepsza koordynacja", "Poprawa kondycji", "Prewencja kontuzji", "Zwiększenie mocy"],
        "intensity": "Intensywność",
        "intensities": ["Niska", "Średnia", "Wysoka"],
        "time": "Ile minut na trening w tygodniu?",
        "days": "Dni gry w baseball",
        "days_list": ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"],
        "equipment": "Dostępny sprzęt",
        "equip_list": ["Gumy oporowe (Resistance bands)", "Piłka lekarska (Medicine ball)", "Ciężary / Siłownia", "Chodzenie / Rower / Bieganie"],
        "arm": "Stan ręki",
        "arm_options": ["Zdrowa", "Lekko obolała", "W regeneracji", "Silne ograniczenia"],
        "button": "Wygeneruj plan",
        "success": "Plan wygenerowany",
        "summary": "Podsumowanie",
        "weekly": "Plan tygodniowy",
        "library": "Słownik ćwiczeń + filmiki",
        "disclaimer": "To uproszczony plan. Skonsultuj z trenerem.",
        "info": "Wypełnij dane i kliknij przycisk.",
        "download_pdf": "Pobierz PDF",
        "playing_days_label": "Dni gry",
        "arm_label": "Stan ręki",
        "time_label": "Czas",
        "sessions": "sesje",
        "strength": "Siła",
        "conditioning": "Kondycja + Mobilność",
        "easy_cardio": "Lekki bieg / rower / spacer",
        "mobility_core": "Mobilność + core",
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
        "weekly": "Weekly plan",
        "library": "Exercise library + videos",
        "disclaimer": "Simplified plan. Consult a coach.",
        "info": "Fill the form and click the button.",
        "download_pdf": "Download PDF",
        "playing_days_label": "Playing days",
        "arm_label": "Arm condition",
        "time_label": "Time",
        "sessions": "sessions",
        "strength": "Strength",
        "conditioning": "Conditioning + Mobility",
        "easy_cardio": "Easy run / bike / walk",
        "mobility_core": "Mobility + core",
    }
}

t = T[lang]

DAY_MAP = {
    "Poniedziałek": "Monday", "Wtorek": "Tuesday", "Środa": "Wednesday",
    "Czwartek": "Thursday", "Piątek": "Friday", "Sobota": "Saturday", "Niedziela": "Sunday",
    "Monday": "Monday", "Tuesday": "Tuesday", "Wednesday": "Wednesday",
    "Thursday": "Thursday", "Friday": "Friday", "Saturday": "Saturday", "Sunday": "Sunday"
}

EXERCISES = {
    "Goblet / Front Squat": {
        "pl_name": "Goblet Squat / Przysiad z ciężarem",
        "en_name": "Goblet / Front Squat",
        "pl": "Przysiad z ciężarem trzymanym przy klatce.",
        "en": "Squat holding weight at chest.",
        "yt": "https://www.youtube.com/watch?v=zBV3ceGyAxw"
    },
    "Romanian Deadlift": {
        "pl_name": "Martwy ciąg rumuński",
        "en_name": "Romanian Deadlift",
        "pl": "Martwy ciąg rumuński – tylny łańcuch.",
        "en": "Hip-hinge for hamstrings and glutes.",
        "yt": "https://www.youtube.com/watch?v=2SHsk9AzdjA"
    },
    "Bulgarian Split Squat": {
        "pl_name": "Przysiad bułgarski",
        "en_name": "Bulgarian Split Squat",
        "pl": "Przysiad bułgarski – jedna noga z tyłu.",
        "en": "Rear-foot elevated split squat.",
        "yt": "https://www.youtube.com/watch?v=o7yFuIR9XVU"
    },
    "Hip Thrust": {
        "pl_name": "Hip Thrust / Wypychanie bioder",
        "en_name": "Hip Thrust",
        "pl": "Wypychanie bioder – świetne na pośladki.",
        "en": "Hip extension for glutes.",
        "yt": "https://www.youtube.com/watch?v=SEdqd1n0cvg"
    },
    "Bodyweight Squat": {
        "pl_name": "Przysiad z masą ciała",
        "en_name": "Bodyweight Squat",
        "pl": "Klasyczny przysiad bez obciążenia.",
        "en": "Classic bodyweight squat.",
        "yt": "https://www.youtube.com/watch?v=aclHkVaku9U"
    },
    "Reverse Lunges": {
        "pl_name": "Wykroki do tyłu",
        "en_name": "Reverse Lunges",
        "pl": "Wykroki do tyłu – delikatniejsze dla kolan.",
        "en": "Step-back lunges.",
        "yt": "https://www.youtube.com/watch?v=xr33x6zMQ9Q"
    },
    "Single-leg RDL": {
        "pl_name": "Martwy ciąg na jednej nodze",
        "en_name": "Single-leg RDL",
        "pl": "Martwy ciąg na jednej nodze.",
        "en": "Single-leg Romanian deadlift.",
        "yt": "https://www.youtube.com/watch?v=4rE3sLq7Y4k"
    },
    "Glute Bridge": {
        "pl_name": "Mostek biodrowy",
        "en_name": "Glute Bridge",
        "pl": "Mostek biodrowy.",
        "en": "Glute bridge.",
        "yt": "https://www.youtube.com/watch?v=OUgsA8XiM_g"
    },
    "Dead Bug": {
        "pl_name": "Dead Bug",
        "en_name": "Dead Bug",
        "pl": "Ćwiczenie stabilizujące core.",
        "en": "Core control exercise.",
        "yt": "https://www.youtube.com/watch?v=g_BYB0R-4Ws"
    },
    "Side Plank": {
        "pl_name": "Deska boczna",
        "en_name": "Side Plank",
        "pl": "Deska boczna.",
        "en": "Side plank.",
        "yt": "https://www.youtube.com/watch?v=XeN4pEZZJNI"
    },
    "Pallof Press": {
        "pl_name": "Pallof Press",
        "en_name": "Pallof Press",
        "pl": "Antyrotacyjne ćwiczenie core.",
        "en": "Anti-rotation core press.",
        "yt": "https://www.youtube.com/watch?v=5_8d8vHgZvU"
    },
    "Band Face Pulls": {
        "pl_name": "Face Pulls z gumą",
        "en_name": "Band Face Pulls",
        "pl": "Face Pulls z gumą – ochrona barku.",
        "en": "Band face pulls for shoulders.",
        "yt": "https://www.youtube.com/watch?v=Wq-Td9UXRK8"
    },
    "Band External Rotations": {
        "pl_name": "Zewnętrzna rotacja z gumą",
        "en_name": "Band External Rotations",
        "pl": "Zewnętrzna rotacja barku z gumą.",
        "en": "Band external rotation.",
        "yt": "https://www.youtube.com/watch?v=VjFVN0MBDh0"
    },
    "Band Rows": {
        "pl_name": "Wiosłowanie z gumą",
        "en_name": "Band Rows",
        "pl": "Wiosłowanie z gumą.",
        "en": "Band rows.",
        "yt": "https://www.youtube.com/watch?v=GZbfZ0338Zo"
    },
    "Med Ball Rotational Throws": {
        "pl_name": "Rzuty piłką lekarską w rotacji",
        "en_name": "Med Ball Rotational Throws",
        "pl": "Rzuty piłką lekarską w rotacji.",
        "en": "Rotational med ball throws.",
        "yt": "https://www.youtube.com/watch?v=1xqZf1zqZ2k"
    },
    "Med Ball Slams": {
        "pl_name": "Uderzenia piłką lekarską",
        "en_name": "Med Ball Slams",
        "pl": "Uderzenia piłką lekarską o podłogę.",
        "en": "Medicine ball slams.",
        "yt": "https://www.youtube.com/watch?v=2xX4zQ3zqZ0"
    },
    "Dumbbell Shoulder Press": {
        "pl_name": "Wyciskanie hantli nad głowę",
        "en_name": "Dumbbell Shoulder Press",
        "pl": "Wyciskanie hantli nad głowę.",
        "en": "Dumbbell overhead press.",
        "yt": "https://www.youtube.com/watch?v=B-aVuyhvLNs"
    },
    "Bent-over Row": {
        "pl_name": "Wiosłowanie w opadzie",
        "en_name": "Bent-over Row",
        "pl": "Wiosłowanie w opadzie.",
        "en": "Bent-over row.",
        "yt": "https://www.youtube.com/watch?v=vT2GjY_Umpw"
    },
    "Push-ups": {
        "pl_name": "Pompki",
        "en_name": "Push-ups",
        "pl": "Klasyczne pompki.",
        "en": "Push-ups.",
        "yt": "https://www.youtube.com/watch?v=IODxDxX7oi4"
    },
    "Inverted Rows": {
        "pl_name": "Podciąganie w poziomie",
        "en_name": "Inverted Rows",
        "pl": "Podciąganie w poziomie.",
        "en": "Inverted rows.",
        "yt": "https://www.youtube.com/watch?v=TgxS_9M7yEw"
    },
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

    has_bands = any("band" in s.lower() or "gumy" in s.lower() for s in sprzet)
    has_medball = any("medicine" in s.lower() or "lekarska" in s.lower() for s in sprzet)
    has_weights = any("weights" in s.lower() or "siłownia" in s.lower() or "ciężary" in s.lower() for s in sprzet)
    has_cardio = any("walking" in s.lower() or "bike" in s.lower() or "running" in s.lower() or "chodzenie" in s.lower() or "rower" in s.lower() or "bieganie" in s.lower() for s in sprzet)

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

    if lang == "Polski":
        if intensywnosc == "Niska":
            serie_info = "2 serie × 10-15 (lekko)"
        elif intensywnosc == "Wysoka":
            serie_info = "4 serie × 5-8 (ciężko)"
        else:
            serie_info = "3 serie × 8-12"
    else:
        if intensywnosc == "Low":
            serie_info = "2 sets × 10-15 (light)"
        elif intensywnosc == "High":
            serie_info = "4 sets × 5-8 (heavy)"
        else:
            serie_info = "3 sets × 8-12"

    st.success(t["success"])

    st.subheader(t["summary"])
    st.markdown(f"""
**{t['position']}:** {pozycja}  
**{t['age']} / {t['gender']}:** {wiek} / {plec}  
**{t['height']} / {t['weight']}:** {wzrost} cm / {waga} kg  
**{t['goal']}:** {cel}  
**{t['intensity']}:** {intensywnosc}  
**{t['time_label']}:** {czas_tyg} min → {sesje} {t['sessions']} × ~{dlugosc} min  
**{t['playing_days_label']}:** {', '.join(dni_gry) if dni_gry else '-'}  
**{t['arm_label']}:** {stan_reki}
""")

    st.subheader(t["weekly"])
    all_days = t["days_list"]
    training_days = [d for d in all_days if d not in dni_gry][:sesje] or all_days[:sesje]

    for i, day in enumerate(training_days):
        st.markdown(f"**{day} (~{dlugosc} min)**")
        if i % 2 == 0:
            st.write(f"{t['strength']} - {serie_info}")
            for ex in selected[:6]:
                name = EXERCISES[ex]["pl_name"] if lang == "Polski" else EXERCISES[ex]["en_name"]
                st.write(f"- {name}")
        else:
            st.write(t["conditioning"])
            if has_cardio:
                st.write(f"- {t['easy_cardio']}")
            st.write(f"- {t['mobility_core']}")

    st.subheader(t["library"])
    for ex in selected:
        if ex in EXERCISES:
            name = EXERCISES[ex]["pl_name"] if lang == "Polski" else EXERCISES[ex]["en_name"]
            with st.expander(name):
                st.write(EXERCISES[ex]["pl"] if lang == "Polski" else EXERCISES[ex]["en"])
                st.markdown(f"[YouTube]({EXERCISES[ex]['yt']})")

    st.warning(t["disclaimer"])

    # PDF
    def safe(txt):
        return str(txt).encode("ascii", "ignore").decode("ascii")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(True, margin=15)
    pdf.set_margins(15, 15, 15)
    pdf.set_font("Helvetica", size=11)
    W = 180

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
                write(f"   - {safe(EXERCISES[ex]['en_name'])}")
        else:
            write("   Conditioning + Mobility")
            if has_cardio:
                write("   - Easy cardio")
            write("   - Mobility + core")
        write("")
    write("3. EXERCISES + VIDEOS", bold=True, size=13)
    for ex in selected:
        write(safe(EXERCISES[ex]["en_name"]), bold=True)
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
