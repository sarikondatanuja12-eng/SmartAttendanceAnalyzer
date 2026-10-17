import streamlit as st
import pandas as pd
import math
from datetime import date

st.set_page_config(
    page_title="Smart Attendance Analyzer",
    page_icon="📚",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #f2f6fc;
}
h1 {
    color: #17365d;
}
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #dce5f0;
    padding: 18px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.title("📚 Smart Attendance Analyzer")
st.write("A simple tool to calculate student attendance and eligibility.")
st.divider()

# Attendance settings
st.sidebar.header("⚙️ Settings")
required_percentage = st.sidebar.slider(
    "Required Attendance (%)",
    min_value=50,
    max_value=100,
    value=75
)

# Student details
st.header("👩‍🎓 Student Details")

col1, col2 = st.columns(2)

with col1:
    student_name = st.text_input("Student Name")
    roll_number = st.text_input("Roll Number")
    department = st.selectbox(
        "Department",
        ["CSE", "IT", "ECE", "EEE", "Mechanical", "Civil", "Other"]
    )

with col2:
    academic_year = st.selectbox(
        "Academic Year",
        ["1st Year", "2nd Year", "3rd Year", "4th Year"]
    )
    report_date = st.date_input("Report Date", value=date.today())

st.divider()

# Attendance inputs
st.header("📊 Attendance Details")

col3, col4 = st.columns(2)

with col3:
    total_classes = st.number_input(
        "Total Classes Conducted",
        min_value=1,
        max_value=10000,
        value=40,
        step=1
    )

with col4:
    attended_classes = st.number_input(
        "Classes Attended",
        min_value=0,
        max_value=10000,
        value=32,
        step=1
    )

# Calculate attendance
if st.button("Calculate Attendance", type="primary", use_container_width=True):

    if not student_name.strip():
        st.error("Please enter the student name.")

    elif attended_classes > total_classes:
        st.error("Classes attended cannot exceed total classes conducted.")

    else:
        percentage = (attended_classes / total_classes) * 100
        missed_classes = total_classes - attended_classes

        st.divider()
        st.header("📋 Attendance Report")

        st.write(f"**Student Name:** {student_name}")
        st.write(f"**Roll Number:** {roll_number or 'Not provided'}")
        st.write(f"**Department:** {department}")
        st.write(f"**Academic Year:** {academic_year}")
        st.write(f"**Report Date:** {report_date}")

        m1, m2, m3 = st.columns(3)

        m1.metric("Attendance", f"{percentage:.2f}%")
        m2.metric("Classes Attended", f"{attended_classes}/{total_classes}")
        m3.metric("Classes Missed", str(missed_classes))

        st.progress(min(percentage / 100, 1.0))

        if percentage >= required_percentage:
            st.success(
                f"✅ Eligible! Attendance is at least {required_percentage}%."
            )
            st.balloons()

            classes_needed = 0

        else:
            st.warning(
                f"⚠️ Attendance is below {required_percentage}%."
            )

            if required_percentage == 100:
                classes_needed = total_classes - attended_classes
            else:
                needed = (
                    required_percentage * total_classes
                    - 100 * attended_classes
                ) / (100 - required_percentage)

                classes_needed = max(0, math.ceil(needed - 1e-10))

            st.info(
                f"Attend the next {classes_needed} classes consecutively "
                f"to reach {required_percentage}% attendance."
            )

        # Create downloadable report
        report = {
            "Student Name": student_name.strip(),
            "Roll Number": roll_number or "Not provided",
            "Department": department,
            "Academic Year": academic_year,
            "Report Date": str(report_date),
            "Total Classes": int(total_classes),
            "Classes Attended": int(attended_classes),
            "Classes Missed": int(missed_classes),
            "Attendance Percentage": round(percentage, 2),
            "Required Percentage": required_percentage,
            "Eligibility": (
                "Eligible"
                if percentage >= required_percentage
                else "Below Required Attendance"
            ),
            "Additional Classes Needed": int(classes_needed)
        }

        st.subheader("📁 Download Report")

        report_df = pd.DataFrame([report])

        st.download_button(
            label="⬇️ Download Attendance Report (CSV)",
            data=report_df.to_csv(index=False).encode("utf-8-sig"),
            file_name="attendance_report.csv",
            mime="text/csv",
            use_container_width=True
        )

        with st.expander("View Complete Report"):
            st.dataframe(report_df, use_container_width=True)

else:
    st.info(
        "Enter the student details and attendance information, "
        "then click Calculate Attendance."
    )

st.divider()
st.caption("Smart Attendance Analyzer | Student Project")
