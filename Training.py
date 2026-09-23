import streamlit as st
from fpdf import FPDF
from datetime import datetime
import io

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
        "pdf_title": "Plan Treningowy Baseball",
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
        "pdf_title": "Baseball Training Plan",
    }
}

t = T[lang]

st.title(t["title"])
st.markdown(f"**{t['subtitle']}**")
st.divider()

# ====================== SEKCJA 1: DANE ZAWODNIKA ======================
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

# ====================== SEKCJA 2: CEL I PREFERENCJE ======================
st.header(t["section2"])

cel = st.selectbox(t["goal"], t["goals"])
intensywnosc = st.selectbox(t["intensity"], t["intensities"])

czas_tyg = st.number_input(t["time"], min_value=60, max_value=700, value=180, step=15)

dni_gry = st.multiselect(t["days"], t["days_list"])

sprzet = st.multiselect(t["equipment"], t["equip_list"])

stan_reki = st.selectbox(t["arm"], t["arm_options"])

st.divider()

# ====================== GENEROWANIE ======================
if st.button(t["button"], type="primary", use_container_width=True):

    bmi = waga / ((wzrost / 100) ** 2)
    has_bands = "Resistance bands" in sprzet
    has_medball = "Medicine ball" in sprzet
    has_weights = "Weights / Gym" in sprzet
    has_cardio = "Walking / Bike / Running" in sprzet

    # Liczba sesji
    if czas_tyg < 120:
        sesje = 2
    elif czas_tyg < 250:
        sesje = 3
    else:
        sesje = 4
    dlugosc = max(30, czas_tyg // sesje)

    # Fokus
    if lang == "Polski":
        pos_focus = {
            "Pitcher (miotacz)": "stabilizacja barku, siła rotacyjna, nogi + core",
            "Catcher (łapacz)": "siła nóg, mobilność bioder, wytrzymałość w przysiadzie",
            "Infielder (wewnętrzny)": "zwinność, eksplozywność, stabilizacja core",
            "Outfielder (zapolowy)": "prędkość, moc rzutowa, kondycja"
        }
        base = pos_focus.get(pozycja, "ogólna sprawność")
        focus = f"{base} | Cel: {cel} | Intensywność: {intensywnosc}"
    else:
        pos_focus = {
            "Pitcher": "shoulder stability, rotational strength, legs + core",
            "Catcher": "leg strength, hip mobility, squat endurance",
            "Infielder": "agility, explosiveness, core stability",
            "Outfielder": "speed, throwing power, conditioning"
        }
        base = pos_focus.get(pozycja, "general fitness")
        focus = f"{base} | Goal: {cel} | Intensity: {intensywnosc}"

    # Ćwiczenia
    arm_bad = stan_reki in t["arm_options"][2:]
    exercises = []

    if has_weights:
        exercises += ["Goblet / Front Squat", "Romanian Deadlift", "Bulgarian Split Squat", "Hip Thrust"]
    else:
        exercises += ["Bodyweight Squat", "Reverse Lunges", "Single-leg RDL", "Glute Bridge"]

    exercises += ["Dead Bug", "Side Plank", "Pallof Press"]

    if not arm_bad:
        if has_weights:
            exercises += ["Dumbbell Shoulder Press", "Bent-over Row"]
        if has_bands:
            exercises += ["Band Face Pulls", "Band External Rotations", "Band Rows"]
        if has_medball:
            exercises += ["Med Ball Rotational Throws", "Med Ball Slams"]
        if not has_weights and not has_bands:
            exercises += ["Push-ups", "Inverted Rows"]
    else:
        exercises += ["Only light shoulder mobility (no loading)" if lang == "English" else "Tylko lekka mobilność barku (bez obciążenia)"]

    # Dostosowanie do intensywności
    if "Niska" in intensywnosc or "Low" in intensywnosc:
        serie_info = "2 serie × 10–15 powtórzeń (lekko)" if lang == "Polski" else "2 sets × 10–15 reps (light)"
    elif "Wysoka" in intensywnosc or "High" in intensywnosc:
        serie_info = "4 serie × 5–8 powtórzeń (ciężko)" if lang == "Polski" else "4 sets × 5–8 reps (heavy)"
    else:
        serie_info = "3 serie × 8–12 powtórzeń" if lang == "Polski" else "3 sets × 8–12 reps"

    # ---------- WYŚWIETLENIE ----------
    st.success(t["success"])

    st.subheader(t["summary"])
    summary_text = f"""
**{t['position']}:** {pozycja}  
**{t['age']} / {t['gender']}:** {wiek} / {plec}  
**{t['height']} / {t['weight']}:** {wzrost} cm / {waga} kg (BMI ≈ {bmi:.1f})  
**{t['goal']}:** {cel}  
**{t['intensity']}:** {intensywnosc}  
**Czas tygodniowy:** {czas_tyg} min → {sesje} sesje × ~{dlugosc} min  
**Dni gry:** {', '.join(dni_gry) if dni_gry else '-'}  
**Stan ręki:** {stan_reki}
"""
    st.markdown(summary_text)

    st.subheader(t["focus"])
    st.info(focus)

    st.subheader(t["weekly"])
    all_days = t["days_list"]
    training_days = [d for d in all_days if d not in dni_gry][:sesje]
    if not training_days:
        training_days = all_days[:sesje]

    plan_lines = []
    for i, day in enumerate(training_days):
        st.markdown(f"### {day} (~{dlugosc} min)")
        if i % 2 == 0:
            st.markdown(f"**Siła / Strength** – {serie_info}")
            for ex in exercises[:6]:
                st.markdown(f"- {ex}")
                plan_lines.append(f"{day} - Strength: {ex}")
        else:
            st.markdown("**Kondycja + mobilność / Conditioning + mobility**")
            if has_cardio:
                st.markdown("- Easy run / bike / walk 15–25 min")
            st.markdown("- Dynamic mobility + core")
            plan_lines.append(f"{day} - Conditioning + mobility")

    if dni_gry:
        st.markdown("---")
        msg = f"**Dni gry ({', '.join(dni_gry)}):** tylko lekka mobilność i regeneracja." if lang == "Polski" else f"**Playing days ({', '.join(dni_gry)}):** only light mobility and recovery."
        st.markdown(msg)

    st.subheader(t["notes"])
    st.markdown("- Zawsze rozgrzewka 8–12 min\n- Słuchaj ciała, szczególnie ręki\n- Regeneracja: sen + białko")
    st.warning(t["disclaimer"])

    # ====================== PDF ======================
    class PDF(FPDF):
        def header(self):
            self.set_font("Helvetica", "B", 16)
            self.cell(0, 10, t["pdf_title"], ln=True, align="C")
            self.set_font("Helvetica", "", 10)
            self.cell(0, 8, datetime.now().strftime("%Y-%m-%d"), ln=True, align="C")
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font("Helvetica", "I", 8)
            self.cell(0, 10, f"Page {self.page_no()}", align="C")

    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", "", 11)

    def add_line(text):
        pdf.multi_cell(0, 7, text)

    add_line(f"Position: {pozycja}")
    add_line(f"Age / Gender: {wiek} / {plec}")
    add_line(f"Height / Weight: {wzrost} cm / {waga} kg")
    add_line(f"Goal: {cel}")
    add_line(f"Intensity: {intensywnosc}")
    add_line(f"Weekly time: {czas_tyg} min ({sesje} sessions)")
    add_line(f"Playing days: {', '.join(dni_gry) if dni_gry else '-'}")
    add_line(f"Arm condition: {stan_reki}")
    add_line("")
    add_line(f"Main focus: {focus}")
    add_line("")
    add_line("Weekly plan:")
    for line in plan_lines:
        add_line(f"- {line}")
    add_line("")
    add_line("Exercises used:")
    for ex in exercises:
        add_line(f"- {ex}")
    add_line("")
    add_line(t["disclaimer"])

    pdf_output = pdf.output()
    st.download_button(
        label=t["download_pdf"],
        data=pdf_output,
        file_name=f"baseball_plan_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

else:
    st.info(t["info"])