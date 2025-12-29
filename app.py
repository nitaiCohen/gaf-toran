import streamlit as st

DAYS = ["ראשון", "שני", "שלישי", "רביעי", "חמישי"]
SHIFTS = ["בוקר", "צהריים", "ערב"]
SHIFT_DIFFICULTY = {"בוקר": 1, "צהריים": 2, "ערב": 1}

st.set_page_config(page_title="סידור העמדות", layout="wide")
st.title("📋 מערכת סידור העמדות לגף")

st.markdown("הכנס את רשימת הקורסים (שורה או פסיקים), וסמן אילו ימים כל קורס לא זמין להעמדה.")

# הזנת קורסים
raw_input = st.text_area("הכנס קורסים (שורה או פסיקים):", height=100)
course_list = []
if raw_input:
    for line in raw_input.splitlines():
        for part in line.split(","):
            name = part.strip()
            if name:
                course_list.append(name)
    course_list = list(dict.fromkeys(course_list))  # הסרת כפילויות

# הזנת ימים לא זמינים
unavailable = {}
if course_list:
    st.subheader("📆 הגדרת ימים לא זמינים לכל קורס")
    for course in course_list:
        days = st.multiselect(f"{course} לא זמין ב:", DAYS, key=course)
        unavailable[course] = set(days)

# כפתור יצירת סידור
if st.button("🚀 צור סידור"):
    usage = {c: 0 for c in course_list}
    used_today = {c: set() for c in course_list}
    schedule = []

    for day in DAYS:
        row = [day]
        for shift in SHIFTS:
            candidates = [c for c in course_list if day not in unavailable.get(c, set()) and day not in used_today[c]]
            if not candidates:
                row.append("אין מועמד")
                continue
            candidates.sort(key=lambda c: usage[c] + SHIFT_DIFFICULTY[shift])
            chosen = candidates[0]
            usage[chosen] += SHIFT_DIFFICULTY[shift]
            used_today[chosen].add(day)
            row.append(chosen)
        schedule.append(row)

    st.success("✅ סידור נוצר בהצלחה!")
    st.write("### 🗓️ טבלת סידור שבועית")
    st.table(schedule)