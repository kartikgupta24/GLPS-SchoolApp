from datetime import datetime

import streamlit as st
#import pyodbc
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv
# Load .env file
load_dotenv(dotenv_path="config/.env")

print(os.getenv('DB_HOST'))
print(os.getenv('DB_NAME'))
print(os.getenv('DB_USER'))
print(os.getenv('DB_PASSWORD'))
print(os.getenv('DB_PORT'))
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT')
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
    # try:
    #     conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    #     return conn
    # except Exception as e:
    #     print(f"Error connecting to the database: {e}")
    #     return None
    # conn = pyodbc.connect(
    #     "DRIVER={ODBC Driver 17 for SQL Server};"
    #     f"SERVER={os.getenv('DB_SERVER')};"
    #     f"DATABASE={os.getenv('DB_NAME')};"
    #     f"UID={os.getenv('DB_USER')};"
    #     f"PWD={os.getenv('DB_PWD')}"
    #     #"Trusted_Connection=yes;"
    # )
    # return conn


# --- Dummy login credentials ---
USER_CREDENTIALS = {
    os.getenv("DB_USER_admin"): os.getenv("DB_PWD_admin"),
    os.getenv("DB_USER_teacher"): os.getenv("DB_PWD_teacher")
}


# Function for user authentication
def login():
    st.sidebar.markdown("""<h2 style ='text-align: left;'>🌿 Green Leaf Public School, Saharanpur</h2>""",
                        unsafe_allow_html=True)
    st.sidebar.title("🔑 Login")
    username = st.sidebar.text_input("Username", key="username")
    password = st.sidebar.text_input("Password", type="password", key="password")
    login_btn = st.sidebar.button("Login")

    if login_btn:
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state["authenticated"] = True
            st.session_state["user"] = username
            st.sidebar.success(f"✅ Logged in as {username}")
            st.rerun()
        else:
            st.sidebar.error("❌ Incorrect username or password")


# Logout function
def logout():
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    st.sidebar.warning("🔒 Logged out. Please login again.")


# Initialize session state for login
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["user"] = None

# Check authentication
if not st.session_state["authenticated"]:
    login()
else:
    # --- MAIN DASHBOARD AFTER LOGIN ---
    st.sidebar.markdown("""<h2 style ='text-align: left;'>🌿 Green Leaf Public School, Saharanpur</h2>""",
                        unsafe_allow_html=True)
    # st.sidebar.divider()
    st.sidebar.button("Logout", on_click=logout)
    # Custom CSS for styling
    st.markdown("""
        <style>
            /* Background Color */
            .stApp {
                background-color: #f5f7fa;
            }

            /* Title Style */
            .title {
                font-size: 36px;
                font-weight: bold;
                color: #2C3E50;
                text-align: center;
                font-family: 'Arial', sans-serif;
                padding: 15px;
                border-radius: 10px;
                background: linear-gradient(to right, #3498db, #2c3e50);
                color: white;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
            }

            /* Sidebar Styling */
            .stSidebar {
                background-color: #1B93B8;
            }

            /* Text and Button Customization */
            .stButton>button {
                background: #3498db;
                color: white;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
            }

            .stButton>button:hover {
                background: #2C3E50;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)

    # Display Title
    st.markdown("""
        <style>
        .stApp {
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        </style>
    """, unsafe_allow_html=True)

    # Add heading text on top
    st.markdown(
        """<h4 style='text-align: left; color: white; background-color: #e6f7e6;
        color: #006400;
        padding: 10px;
        border-radius: 8px;'>🌿 Green Leaf Public School - Growing Minds, Growing Futures</h4>""",
        unsafe_allow_html=True
    )
    # st.divider()
    st.markdown('<div class="title">🏫 School Fee Management System</div>', unsafe_allow_html=True)
    # st.title("🏫 School Fee Management System")
    st.divider()
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to",
                            ["Dashboard", "Add New Student", "Add Fee Payment Details", "Submit Pending Fees",
                             "View Pending Fees Summary"])

    if page == "Dashboard":
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
        except Exception as e:
            st.error(f"Error: {e}")

        cursor.execute("Select COUNT(*) from students")
        total_students = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM fees WHERE \"Balance_Due_Status\" IN ('Pending', 'Partially Paid')")
        students_with_fees_due = cursor.fetchone()[0]

        st.markdown("## 📊 Dashboard Overview")
        st.markdown("---")

        # Create Dashboard Cards
        col1, col2 = st.columns(2)

        with col1:
            st.metric(label="🎓 Total Students", value=total_students)

        with col2:
            st.metric(label="📌 Students with Pending Fees", value=students_with_fees_due)

        conn.close()

    if page == "Add New Student":
        st.header("Add New Student")
        with st.form("Student Form"):
            student_name = st.text_input("Student Name")
            student_gender = st.text_input("Gender")
            student_class = st.text_input("Class")
            father_name = st.text_input("Father Name")
            mother_name = st.text_input("Mother Name")
            contact_number = st.text_input("Contact Number")
            student_address = st.text_input("Address Of Student")
            # New input for Annual Fees
            Annual_Fees = st.number_input("Enter Annual Fees", min_value=0.0, step=1.0)
            Annual_Fees_Paid = st.number_input("Enter Annual Fees Amount Paid", step=1.0)
            # Calculate new balance
            pending_annual_fees = Annual_Fees - Annual_Fees_Paid
            st.write(f"### **Annual Fees Due: Rs. {pending_annual_fees:.2f}**")
            # Payment method
            payment_method = st.selectbox("Payment Method", ["Cash", "UPI", "Bank Transfer"])
            Admission_Date = st.date_input("Enter Student Admission Date")
            admission_month = Admission_Date.strftime("%b")
            if Annual_Fees_Paid:
                annual_fees_payment_date = Admission_Date
            else:
                annual_fees_payment_date = None
            submit_button = st.form_submit_button("Save")
            if submit_button:
                #New code entered
                if pending_annual_fees > 0:
                    bal_due_status = "Pending"
                elif pending_annual_fees == 0:
                    bal_due_status = "Not Pending"
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                    INSERT INTO students (student_name, gender, class, father_name, mother_name, contact, student_address, addmission_date)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
                    RETURNING student_id;
                    """, (student_name, student_gender, student_class, father_name, mother_name, contact_number,
                          student_address, Admission_Date)
                                   )

                    student_id = cursor.fetchone()[0]  # Get the inserted student_id

                    if student_id:
                        print(f"Student ID Retrieved: {student_id}")
                    else:
                        print("Error: Student ID is NULL")
                    cursor.execute("""INSERT INTO fees (student_id, student_name, "Father_name", student_class, month, year, total_fees, amount_paid, balance_due, payment_method, payment_date, "Fee_type", admission_date,"Balance_Due_Status")
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (
                        student_id, student_name, father_name, student_class, admission_month, Admission_Date.year,
                        Annual_Fees, Annual_Fees_Paid, pending_annual_fees, payment_method, annual_fees_payment_date,
                        "Annual Charges", Admission_Date,bal_due_status))
                    conn.commit()
                    st.success("Student Details Saved Successfully")
                except Exception as e:
                    st.error(f"Error: {e}")
                finally:
                    if 'conn' in locals():
                        conn.close()
    if page == "Add Fee Payment Details":
        st.header("Add Fee Payment")
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
        except Exception as e:
            st.error(f"Error: {e}")

        # Fetch class names first
        cursor.execute("SELECT DISTINCT class_name FROM classes ")
        classes = [c[0] for c in cursor.fetchall()]

        # Select Class First (Use session state to retain selection)
        if "selected_class" not in st.session_state:
            st.session_state.selected_class = classes[0] if classes else None
        # Select Class First
        selected_class = st.selectbox("Select Class", classes, index=None, placeholder="Choose a class")

        # Step 2: Fetch Students for Selected Class
        if selected_class:
            cursor.execute("SELECT student_id, student_name FROM students WHERE class = %s", (selected_class,))
            students = cursor.fetchall()

            student_options = {str(s[0]): s[1] for s in students}

            if students:
                selected_student_id = st.selectbox("Select Student", options=student_options.keys(),
                                                   format_func=lambda x: student_options[x],
                                                   index=None, placeholder="Choose a student")
                selected_student_name = student_options[selected_student_id] if selected_student_id else None
            else:
                st.warning("No students found in this class! Please add students first.")
                selected_student_id = None
                selected_student_name = None
        else:
            selected_student_id = None
            selected_student_name = None
        # Step 3: Fetch Father Names for Selected Student
        if selected_student_name:
            cursor.execute("SELECT DISTINCT father_name FROM students WHERE student_name = %s AND class = %s",
                           (selected_student_name, selected_class))
            father_names = [row[0] for row in cursor.fetchall()]

            if father_names:
                selected_father_name = st.selectbox("Select Father Name", options=father_names, index=None,
                                                    placeholder="Choose a father name")

                # Step 4: Identify Student Using Student Name + Father Name + Class
                if selected_father_name:
                    cursor.execute(
                        "SELECT student_id FROM students WHERE student_name = %s AND father_name = %s AND class = %s",
                        (selected_student_name, selected_father_name, selected_class))
                    student_record = cursor.fetchone()

                    if student_record:
                        selected_student_id = student_record[0]
                        st.success(f"✅ Student Identified: {selected_student_name} (ID: {selected_student_id})")
                    else:
                        st.error("❌ No student found with the selected name and father name.")
            else:
                st.warning("⚠ No father names found for this student.")
        else:
            selected_father_name = None
        # Step 3: Enter Fee Details (Only Show If Student Is Selected)

        if selected_student_id:
            fees_type = st.selectbox("Choose Fees Type",
                                     ["Monthly Fees", "Annual Fees", "Exam-Quarterly Fees", "Exam-Half Yearly Fees",
                                      "Exam-Annual Fees"])
            #selected_student_admission_date = 
            cursor.execute(
                """SELECT addmission_date from students where student_id = %s""", (selected_student_id,))
            selected_student_admission_date = cursor.fetchone()    
            with st.form("Fee Detail Form", clear_on_submit=False):
                if fees_type == "Monthly Fees":
                    month = st.selectbox("Month",
                                         ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov",
                                          "Dec"])
                    year = st.number_input("Year", min_value=2000, max_value=2050, step=1)
                elif fees_type == "Exam-Quarterly Fees":
                    month = st.selectbox("Month", ["Sep"])
                    year = st.number_input("Year", min_value=2000, max_value=2050, step=1)
                elif fees_type == "Exam-Half Yearly Fees":
                    month = st.selectbox("Month", ["Dec"])
                    year = st.number_input("Year", min_value=2000, max_value=2050, step=1)
                elif fees_type == "Exam-Annual Fees":
                    month = st.selectbox("Month", ["Mar"])
                    year = st.number_input("Year", min_value=2000, max_value=2050, step=1)
                elif fees_type == "Annual Fees":
                    month = st.selectbox("Admission Month", [
                        datetime.strptime(selected_student_admission_date[0], "%Y-%m-%d").strftime("%b")])
                    year = st.selectbox("Admission Year",
                                        [datetime.strptime(selected_student_admission_date[0], "%Y-%m-%d").year])
                else:
                    month = st.selectbox("Month",
                                         ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov",
                                          "Dec"])
                    year = st.number_input("Year", min_value=2000, max_value=2050, step=1)

                total_fees = st.number_input("Enter Total Fees", min_value=0.0, step=1.0)

                # Fetch last pending balance
                # cursor.execute("""
                #    SELECT TOP 1 balance_due FROM fees WHERE student_id = ? AND month = ? AND year = ?
                #    ORDER BY student_id DESC
                # """, (selected_student_id, month, year))
                # last_pending_fees = cursor.fetchone()
                # last_pending_fees = last_pending_fees[0] if last_pending_fees else 0

                # st.write(f"**Previous Pending Fees for {month} {year}: Rs. {last_pending_fees:.2f}**")
                # max_payable = max(total_fees + last_pending_fees, 0.01)  # Avoid zero max_value
                # Enter Amount Paid
                amount_paid = st.number_input("Enter Amount Paid", step=1.0)

                # Calculate new balance
                new_balance = total_fees - amount_paid
                if new_balance == 0:
                    bal_due_status = "Not Pending"
                elif new_balance > 0:
                    bal_due_status = "Pending"
                st.write(f"### **New Balance Due: Rs. {new_balance:.2f}**")
                # Payment method
                payment_method = st.selectbox("Payment Method", ["Cash", "UPI", "Bank Transfer"])
                payment_date = st.date_input("Payment Date", datetime.today().date())

                submit_button = st.form_submit_button("Save Payment")

                if submit_button:
                    try:
                        if not selected_father_name:
                            st.error("Please Select Father Name ")

                        else:
                            cursor.execute("""
                            INSERT INTO fees (student_id, student_name, "Father_name", student_class, month, year, total_fees, amount_paid, balance_due, payment_method, payment_date, "Fee_type", admission_date, "Balance_Due_Status")
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        """, (selected_student_id, selected_student_name, selected_father_name, selected_class, month,
                              year, total_fees, amount_paid, new_balance,
                              payment_method, payment_date, fees_type, selected_student_admission_date[0],
                              bal_due_status))
                            conn.commit()
                            st.success(
                                f"Payment of Rs. {amount_paid:.2f} recorded for {month} {year}! New balance: Rs. {new_balance:.2f}")
                    except Exception as e:
                        st.error(f"Error: {e}")
                    finally:
                        conn.close()
    if page == "Submit Pending Fees":
        st.header("Pending Fees Payment")
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
        except Exception as e:
            st.error(f"Error: {e}")

        # Fetch class names first
        cursor.execute("SELECT DISTINCT class_name FROM classes ")
        classes = [c[0] for c in cursor.fetchall()]

        # Select Class First (Use session state to retain selection)
        if "selected_class" not in st.session_state:
            st.session_state.selected_class = classes[0] if classes else None
        # Select Class First
        selected_class = st.selectbox("Select Class", classes, index=None, placeholder="Choose a class")

        # Step 2: Fetch Students for Selected Class
        if selected_class:
            cursor.execute("SELECT student_id, student_name FROM students WHERE class = %s", (selected_class,))
            students = cursor.fetchall()

            student_options = {str(s[0]): s[1] for s in students}

            if students:
                selected_student_id = st.selectbox("Select Student", options=student_options.keys(),
                                                   format_func=lambda x: student_options[x],
                                                   index=None, placeholder="Choose a student")
                selected_student_name = student_options[selected_student_id] if selected_student_id else None
            else:
                st.warning("No students found in this class! Please add students first.")
                selected_student_id = None
                selected_student_name = None
        else:
            selected_student_id = None
            selected_student_name = None
        # Step 3: Fetch Father Names for Selected Student
        if selected_student_name:
            cursor.execute("SELECT DISTINCT father_name FROM students WHERE student_name = %s AND class = %s",
                           (selected_student_name, selected_class))
            father_names = [row[0] for row in cursor.fetchall()]

            if father_names:
                selected_father_name = st.selectbox("Select Father Name", options=father_names, index=None,
                                                    placeholder="Choose a father name")

                # Step 4: Identify Student Using Student Name + Father Name + Class
                if selected_father_name:
                    cursor.execute(
                        "SELECT student_id FROM students WHERE student_name = %s AND father_name = %s AND class = %s",
                        (selected_student_name, selected_father_name, selected_class))
                    student_record = cursor.fetchone()

                    if student_record:
                        selected_student_id = student_record[0]
                        st.success(f"✅ Student Identified: {selected_student_name} (ID: {selected_student_id})")
                    else:
                        st.error("❌ No student found with the selected name and father name.")
            else:
                st.warning("⚠ No father names found for this student.")
        else:
            selected_father_name = None
        if selected_student_id:
            fees_type = st.selectbox("Choose Pending Fees Type",
                                     ["Monthly Fees", "Annual Fees", "Exam-Quarterly Fees", "Exam-Half Yearly Fees",
                                      "Exam-Annual Fees"])
            #selected_student_admission_date = 
            cursor.execute(
                """SELECT addmission_date from students where student_id = %s""", (selected_student_id,))
            selected_student_admission_date = cursor.fetchone()
            if fees_type == "Monthly Fees":
                month = st.selectbox("Month",
                                     ["All", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct",
                                      "Nov",
                                      "Dec"])
                year = st.number_input("Year", min_value=2000, max_value=2050, step=1)
            elif fees_type == "Exam-Quarterly Fees":
                month = st.selectbox("Month", ["Sep"])
                year = st.number_input("Year", min_value=2000, max_value=2050, step=1)
            elif fees_type == "Exam-Half Yearly Fees":
                month = st.selectbox("Month", ["Dec"])
                year = st.number_input("Year", min_value=2000, max_value=2050, step=1)
            elif fees_type == "Exam-Annual Fees":
                month = st.selectbox("Month", ["Mar"])
                year = st.number_input("Year", min_value=2000, max_value=2050, step=1)
            elif fees_type == "Annual Fees":
                month = st.selectbox("Admission Month", [
                    datetime.strptime(selected_student_admission_date[0], "%Y-%m-%d").strftime("%b")])
                year = st.selectbox("Admission Year",
                                    [datetime.strptime(selected_student_admission_date[0], "%Y-%m-%d").year])
            else:
                month = st.selectbox("Month",
                                     ["All", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct",
                                      "Nov",
                                      "Dec"])
                year = st.number_input("Year", min_value=2000, max_value=2050, step=1)

            if month != "All":
                # cursor.execute(
                # """SELECT SUM(balance_due) from Fees where class = ? AND student_id = ? AND father_name = ? AND month = ? AND year = ? AND fee_type = ? AND Balance_Due_Status = ?""",
                # (selected_class, selected_student_id, selected_father_name, month, year, fees_type, 'Pending'))
                cursor.execute(
                    """
                                    WITH LatestBalance AS (
            SELECT 
                student_id, 
                new_balance
            FROM pending_fees_balance_tbl
            WHERE pending_id = (
                SELECT MAX(pending_id) 
                FROM pending_fees_balance_tbl pf 
                WHERE pf.student_id = pending_fees_balance_tbl.student_id
            )
        )
        SELECT COALESCE(SUM(
            CASE 
                WHEN f."Balance_Due_Status" = 'Pending' THEN f.balance_due
                WHEN f."Balance_Due_Status" = 'Partially Paid' THEN COALESCE(lb.new_balance, f.balance_due)
                ELSE 0
            END
        ), 0)
        FROM Fees f
        LEFT JOIN LatestBalance lb ON f.student_id = lb.student_id
        WHERE f.student_class = %s AND f.student_id = %s AND f."Father_name" = %s 
              AND f.month = %s AND f.year = %s AND f."Fee_type" = %s 
              AND f."Balance_Due_Status" IN ('Pending', 'Partially Paid')
                    """,
                    (selected_class, selected_student_id, selected_father_name, month, year, fees_type)
                )
                result = cursor.fetchone()
                total_pending_fees = result[0] if result and result[0] is not None else 0

                st.number_input("Total Pending Fees", value=total_pending_fees, key="pending_fees", disabled=True)
            else:
                # cursor.execute(
                # """SELECT SUM(balance_due) from Fees where class = ? AND student_id = ? AND father_name = ? AND year = ? AND  fee_type = ? AND Balance_Due_Status = ?""",
                # (selected_class, selected_student_id, selected_father_name, year, fees_type, 'Pending'))
                cursor.execute(
                    """
                                        WITH LatestBalance AS (
                SELECT 
                    student_id, 
                    new_balance
                FROM pending_fees_balance_tbl
                WHERE pending_id = (
                    SELECT MAX(pending_id) 
                    FROM pending_fees_balance_tbl pf 
                    WHERE pf.student_id = pending_fees_balance_tbl.student_id
                )
            )
            SELECT COALESCE(SUM(
                CASE 
                    WHEN f."Balance_Due_Status" = 'Pending' THEN f.balance_due
                    WHEN f."Balance_Due_Status" = 'Partially Paid' THEN COALESCE(lb.new_balance, f.balance_due)
                    ELSE 0
                END
            ), 0)
            FROM Fees f
            LEFT JOIN LatestBalance lb ON f.student_id = lb.student_id
            WHERE f.student_class = %s AND f.student_id = %s AND f."Father_name" = %s 
                   AND f.year = %s AND f."Fee_type" = %s 
                  AND f."Balance_Due_Status" IN ('Pending', 'Partially Paid')
                    """,
                    (selected_class, selected_student_id, selected_father_name, year, fees_type)
                )
                result = cursor.fetchone()
                total_pending_fees = result[0] if result and result[0] is not None else 0

                st.number_input("Total Pending Fees", value=total_pending_fees, key="pending_fees", disabled=True)
            pending_amount_paid = st.number_input("Enter Amount Paid", step=1.0)
            new_balance = total_pending_fees - pending_amount_paid
            payment_method = st.selectbox("Payment Method", ["Cash", "UPI", "Bank Transfer"])
            payment_date = st.date_input("Payment Date", datetime.today().date())
            if new_balance == 0:
                bal_due_status = "Cleared"
            elif new_balance > 0:
                bal_due_status = "Partially Paid"
            if st.button("Save Payment"):
                cursor.execute(
                    "SELECT \"Fee_id\" from Fees where student_class = %s AND student_id = %s AND father_name = %s AND fee_type = %s AND month = %s AND year = %s",
                    (selected_class, selected_student_id, selected_father_name, fees_type, month, year,))
                result = cursor.fetchone()
                fee_id = result[0] if result and result[0] is not None else 0

                cursor.execute("""INSERT INTO pending_fees_balance_tbl(student_id,student_name,student_class,father_name,fee_type,pending_fees,pending_fees_amount_paid,new_balance,payment_method,payment_date,month,year,admission_date)
                                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                               (selected_student_id, selected_student_name, selected_class, selected_father_name,
                                fees_type, total_pending_fees, pending_amount_paid, new_balance, payment_method,
                                payment_date, month, year, selected_student_admission_date[0]))
                conn.commit()
                st.success(
                    f"Pending Payment of Rs. {pending_amount_paid:.2f} recorded for {month} {year}! New balance: Rs. {new_balance:.2f}")
                cursor.execute("UPDATE Fees SET Balance_due_Status = ? Where Fee_id = ?", (bal_due_status, fee_id))
                conn.commit()

                # st.write("Payment saved successfully!")

    if page == "View Pending Fees Summary":
        st.header("📌 View Pending Fees Summary")
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
        except Exception as e:
            st.error(f"Error: {e}")

        # Fetch Overall Total Balance Due Before Applying Filters
        # cursor.execute("SELECT COALESCE(SUM(balance_due), 0) FROM fees WHERE balance_due > 0 AND Balance_Due_Status = ?", ("Pending"))
        cursor.execute("""
                                    WITH LatestBalance AS (
            SELECT 
                student_id, 
                new_balance
            FROM pending_fees_balance_tbl
            WHERE pending_id = (
                SELECT MAX(pending_id) 
                FROM pending_fees_balance_tbl pf 
                WHERE pf.student_id = pending_fees_balance_tbl.student_id
            )
        )
        SELECT COALESCE(SUM(
                CASE 
                    WHEN f."Balance_Due_Status" = 'Pending' THEN f.balance_due
                    WHEN f."Balance_Due_Status" = 'Partially Paid' THEN COALESCE(lb.new_balance, f.balance_due)
                    ELSE 0
                END
            ), 0) AS total_balance_due_overall
        FROM fees f
        LEFT JOIN LatestBalance lb ON f.student_id = lb.student_id
        WHERE f."Balance_Due_Status" IN ('Pending', 'Partially Paid')
            """)
        total_balance_due_overall = cursor.fetchone()[0]

        # Fetch Available Classes from `class` Table
        cursor.execute("SELECT DISTINCT class_name FROM classes")
        classes = [row[0] for row in cursor.fetchall()]
        selected_class = st.selectbox("Select Class", ["All"] + classes)

        # Fetch Students Based on Selected Class
        if selected_class != "All":
            cursor.execute("SELECT student_id, student_name FROM students WHERE class = %s", (selected_class,))
        else:
            cursor.execute("SELECT student_id, student_name FROM students")

        students = cursor.fetchall()
        # print(students)
        if students:
            # Create a dictionary mapping "ID - Name" to student_id
            student_options = {f"{s[0]} - {s[1]}": s[0] for s in students}

            # Create a list for the dropdown (with "All" as the first option)
            student_names = ["All"] + list(student_options.keys())

            # Select Student
            selected_student = st.selectbox("Select Student", student_names)

            # Extract Student ID (Handling "All" case properly)
            selected_student_id = student_options.get(selected_student) if selected_student != "All" else None
            selected_student_name = selected_student.split(" - ")[1] if selected_student != "All" else None
        else:
            st.warning("No students in this class.")
            selected_student = None
            selected_student_id = None
            selected_student_name = None

        # Fetch Father Names if Student is Selected
        selected_father = "All"
        if selected_student_id:
            cursor.execute("SELECT DISTINCT father_name FROM students WHERE student_name = %s and class = %s",
                           (selected_student_name, selected_class,))
            father_names = [row[0] for row in cursor.fetchall()]
            if father_names:
                selected_father = st.selectbox("Select Father Name", ["All"] + father_names)
        # print(selected_father)
        # Fetch Years from Fees Table
        years = [str(year) for year in range(2000, 2051)]
        selected_year = st.selectbox("Select Year", years, index=years.index("2025"))

        # Base Query
        # query = """
        #    SELECT f.student_id, s.student_name, s.father_name, s.class,
        #         COALESCE(SUM(f.balance_due),0) AS total_balance_due,
        #         COALESCE(MAX(f.payment_date),'N/A') AS last_payment_date
        #  FROM fees f
        #  JOIN students s ON f.student_id = s.student_id
        #  WHERE f.balance_due > 0 AND Balance_Due_Status = 'Pending'
        # """

        query = """
                        WITH latest_balance AS (
            SELECT student_id, new_balance, payment_date
            FROM (
                SELECT student_id, new_balance, payment_date, pending_id,
                       ROW_NUMBER() OVER (PARTITION BY student_id ORDER BY payment_date DESC, pending_id DESC) AS rn
                FROM pending_fees_balance_tbl
            ) t
            WHERE rn = 1  -- Pick the latest record per student
        )
        SELECT 
            f.student_id, 
            s.student_name, 
            s.father_name, 
            s.class, 
            COALESCE(SUM(
                CASE 
                    WHEN f."Balance_Due_Status" = 'Pending' THEN f.balance_due
                    WHEN f."Balance_Due_Status" = 'Partially Paid' THEN COALESCE(lb.new_balance, 0)
                    ELSE 0
                END
            ), 0) AS total_balance_due,
            COALESCE(MAX(CASE 
            WHEN f."Balance_Due_Status" = 'Pending' THEN f.payment_date  
            WHEN f."Balance_Due_Status" = 'Partially Paid' THEN lb.payment_date  
            ELSE NULL
        END), 'N/A') AS last_payment_date  
        FROM fees f 
        JOIN students s ON f.student_id = s.student_id
        LEFT JOIN latest_balance lb ON f.student_id = lb.student_id
        WHERE f.balance_due > 0 
        AND f."Balance_Due_Status" IN ('Pending', 'Partially Paid')
            """
        params = []
        # Apply Filters Carefully
        filter_conditions = []
        # Apply Filters
        if selected_class != "All":
            filter_conditions.append("s.class = %s")
            params.append(selected_class)

        if selected_student and selected_student != "All":
            # student_id = selected_student.split(" - ")[0]  # Extract student_id
            selected_student_name = selected_student.split(" - ")[1]  # Extract student name
            filter_conditions.append("s.student_name = %s")
            params.append(selected_student_name)

        if selected_father != "All":
            filter_conditions.append("s.father_name = %s")
            params.append(selected_father)

        if selected_year != "All":
            filter_conditions.append("f.year = %s")
            params.append(selected_year)

        # Append filters correctly
        if filter_conditions:
            query += " AND " + " AND ".join(filter_conditions)

        query += " GROUP BY f.student_id, s.student_name, s.father_name, s.class"

        cursor.execute(query, params)
        summary_fees = cursor.fetchall()
        # print(summary_fees)
        # Convert to DataFrame
        summary_columns = ["Student ID", "Student Name", "Father Name", "Class", "Total Balance Due",
                           "Last Fee Paid Date"]
        df_summary = pd.DataFrame([tuple(row) for row in summary_fees],
                                  columns=summary_columns) if summary_fees else pd.DataFrame(columns=summary_columns)
        view_options = st.radio("Select View: ", ["Current Pending Fees", "Pending Fees Payment History"])
        if view_options == "Current Pending Fees":
            # 📌 Display Summary
            if df_summary.empty:
                st.success("✅ No pending fees found!")

            else:
                # Display Total Balance Due
                st.subheader(f"💰 Total Pending Fees Of All Students: ₹{total_balance_due_overall:,}")
                if selected_student == "All":
                    st.subheader("📌 Summary of All Students with Pending Fees")
                    st.dataframe(df_summary, use_container_width=True)
                else:
                    st.subheader(f"📌 Pending Fees Overview for {selected_student}")
                    st.table(df_summary)  # Show only the selected student's summary

                    # Fetch Month-wise Pending Fees
                    st.subheader(f"📆 Month-wise Pending Fees for {selected_student}")
                    # query = """
                    # SELECT f.student_id, s.student_name, s.father_name, s.class, f.fee_type, f.month, f.year,
                    #         f.total_fees, f.amount_paid, f.balance_due
                    #  FROM fees f
                    # JOIN students s ON f.student_id = s.student_id
                    # WHERE f.balance_due > 0 AND s.student_name = ?
                    # """
                    query = """
                                           query = """
                    # SELECT f.student_id, s.student_name, s.father_name, s.class, f.fee_type, f.month, f.year,
                    #         f.total_fees, f.amount_paid, f.balance_due
                    #  FROM fees f
                    # JOIN students s ON f.student_id = s.student_id
                    # WHERE f.balance_due > 0 AND s.student_name = ?
                    # """
                    query = """
                                           WITH latest_balance AS (
                SELECT student_id, month, year, new_balance
                FROM (
                    SELECT student_id, month, year, new_balance, payment_date, pending_id,
                           ROW_NUMBER() OVER (PARTITION BY student_id, month, year ORDER BY payment_date DESC, pending_id DESC) AS rn
                    FROM pending_fees_balance_tbl
                ) t
                WHERE rn = 1  -- Get the latest pending balance per student, month, and year
            )
            SELECT 
                f.student_id, 
                s.student_name, 
                s.father_name, 
                s.class, 
                f."Fee_type", 
                f.month, 
                f.year, 
                f.total_fees, 
                f.amount_paid,
                CASE 
                    WHEN f."Balance_Due_Status" = 'Pending' THEN f.balance_due
                    WHEN f."Balance_Due_Status" = 'Partially Paid' THEN COALESCE(lb.new_balance, 0)
                    ELSE 0
                END AS balance_due
            FROM fees f 
            JOIN students s ON f.student_id = s.student_id
            LEFT JOIN latest_balance lb 
                ON f.student_id = lb.student_id 
                AND f.month = lb.month 
                AND f.year = lb.year::integer
            WHERE f.balance_due > 0 
            AND s.student_name = %s
                                    """
                    params = [selected_student_name]

                    # Apply father name filter only if a specific father is selected
                    if selected_father != "All":
                        query += " AND s.father_name = %s"
                        params.append(selected_father)

                    cursor.execute(query, params)
                    detailed_fees = cursor.fetchall()
                    # Convert to DataFrame
                    detail_columns = ["Student ID", "Student Name", "Father Name", "Class", "Fee Type", "Month", "Year",
                                      "Total Fees", "Amount Paid", "Balance Due"]
                    df_detail = pd.DataFrame([tuple(row) for row in detailed_fees],
                                             columns=detail_columns) if detailed_fees else pd.DataFrame(
                        columns=detail_columns)

                    # Show Month-wise Breakdown
                    if df_detail.empty:
                        st.success("✅ No pending fees for this student!")
                    else:
                        st.dataframe(df_detail, use_container_width=True)
        elif view_options == "Pending Fees Payment History":
            st.subheader("📜 Payment History of Cleared/Partially Paid Fees")
            history_query = """
                    SELECT pfb.student_id, s.student_name, s.father_name, s.class, pfb."Fee_type", pfb.month, pfb.year,
                           pfb.pending_fees, pfb.pending_fees_amount_paid, pfb.new_balance, pfb.payment_method, pfb.payment_date
                    FROM pending_fees_balance_tbl pfb 
                    JOIN students s ON pfb.student_id = s.student_id
                    WHERE s.student_name = %s AND s.class = %s AND s.father_name = %s AND pfb.year = %s
                """
            history_params = [selected_student_name, selected_class, selected_father, selected_year]

            cursor.execute(history_query, history_params)
            history_fees = cursor.fetchall()

            history_columns = ["Student ID", "Student Name", "Father Name", "Class", "Fees Type", "Month", "Year",
                               "Old Balance", "Amount Paid",
                               "New Balance", "Payment Method", "Payment Date"]
            df_history = pd.DataFrame([tuple(row) for row in history_fees],
                                      columns=history_columns) if history_fees else pd.DataFrame(
                columns=history_columns)

            if df_history.empty:
                st.success("✅ No payment history found!")
            else:
                st.dataframe(df_history, use_container_width=True)
        conn.close()
