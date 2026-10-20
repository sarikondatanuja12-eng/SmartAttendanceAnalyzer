import streamlit as st
import pandas as pd
import math
from datetime import date

st.set_page_config(
    page_title="Smart Attendance Analyzer",
    page_icon="📚",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background-color: #f3f7fc;
    color: #172b4d;
}
h1, h2, h3, p, label, .stMarkdown {
    color: #172b4d !important;
}
div[data-testid="stMetric"] {
    background-color: #ffffff;
    border: 1px solid #d4deeb;
    padding: 16px;
    border-radius: 12px;
}
div[data-testid="stMetric"] label,
div[data-testid="stMetricValue"] {
    color: #17365d !important;
}
.stButton button {
    background-color: #176b3a;
    color: white !important;
    border-radius: 8px;
    font-weight: bold;
}
.stDownloadButton button {
    background-color: #17365d;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

st.title("📚 Smart Attendance Analyzer")
st.write("Calculate attendance percentage and check eligibility.")

st.header("👨‍🎓 Student Details")

student_name = st.text_input("Student Name")
roll_number = st.text_input("Roll Number")

department = st.selectbox(
    "Department",
    ["CSE", "IT", "ECE", "EEE", "Civil", "Mechanical", "Other"]
)

academic_year = st.selectbox(
    "Academic Year",
    ["1st Year", "2nd Year", "3rd Year", "4th Year"]
)

report_date = st.date_input("Report Date", value=date.today())

st.header("📊 Attendance Details")

total_classes = st.number_input(
    "Total Classes Conducted",
    min_value=1,
    value=40,
    step=1
)

attended_classes = st.number_input(
    "Classes Attended",
    min_value=0,
    max_value=int(total_classes),
    value=min(32, int(total_classes)),
    step=1
)

required_percentage = st.slider(
    "Minimum Required Attendance (%)",
    min_value=50,
    max_value=100,
    value=75
)

if st.button("Calculate Attendance", use_container_width=True):

    if not student_name.strip() or not roll_number.strip():
        st.warning("Please enter the student name and roll number.")

    else:
        percentage = (
            attended_classes / total_classes
        ) * 100

        eligible = percentage >= required_percentage

        st.header("📋 Attendance Report")

        col1, col2 = st.columns(2)

        col1.metric("Attendance", f"{percentage:.2f}%")
        col2.metric(
            "Classes Attended",
            f"{int(attended_classes)}/{int(total_classes)}"
        )

        if eligible:
            st.success("Eligible: attendance requirement met.")
        else:
            st.error("Not Eligible yet: attendance is below the requirement.")

            if required_percentage < 100:
                needed = math.ceil(
                    (
                        required_percentage * total_classes / 100
                        - attended_classes
                    )
                    / (1 - required_percentage / 100)
                )
                st.info(
                    f"Attend the next {max(0, needed)} classes "
                    "without absence to reach the required percentage."
                )

        report = pd.DataFrame([{
            "Student Name": student_name,
            "Roll Number": roll_number,
            "Department": department,
            "Academic Year": academic_year,
            "Report Date": str(report_date),
            "Total Classes": int(total_classes),
            "Classes Attended": int(attended_classes),
            "Attendance Percentage": round(percentage, 2),
            "Required Percentage": required_percentage,
            "Eligibility": "Eligible" if eligible else "Not Eligible"
        }])

        st.subheader("Complete Report")
        st.dataframe(report, use_container_width=True)

        st.download_button(
            "Download Attendance Report (CSV)",
            data=report.to_csv(index=False).encode("utf-8"),
            file_name="attendance_report.csv",
            mime="text/csv",
            use_container_width=True
        )
