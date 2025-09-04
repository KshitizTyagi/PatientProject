import streamlit as st
import pandas as pd
import os

DATA_FILE = "patients.csv"

# --- Load data ---
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        # Create dummy CSV if not present
        data = {
            "PatientID": [1, 2, 3, 4],
            "Name": ["John Doe", "Alice Smith", "Bob Johnson", "Mary Brown"],
            "Age": [30, 25, 45, 50],
            "Disease": ["Flu", "Diabetes", "Fracture", "Cancer"],
            "BillAmount": [200, 1500, 3000, 5000],
        }
        df = pd.DataFrame(data)
        df.to_csv(DATA_FILE, index=False)
        return df

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# --- Session state ---
if "patients" not in st.session_state:
    st.session_state["patients"] = load_data()

patients = st.session_state["patients"]

st.title("🏥 Patient Management (CSV Version)")

# --- Search Functionality ---
search_query = st.text_input("🔍 Search Patients (by Name, Disease, ID, etc.)")

if search_query:
    filtered = patients[
        patients.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
    ]
else:
    filtered = patients

st.write("### Patient Records")
st.dataframe(filtered, use_container_width=True)

# --- Editable Bill Amount ---
st.write("### Update Patient Bill Amount")

patient_id = st.number_input("Enter Patient ID", min_value=1, step=1)
new_bill = st.number_input("Enter New Bill Amount", min_value=0, step=100)

if st.button("Update Bill"):
    if patient_id in patients["PatientID"].values:
        patients.loc[patients["PatientID"] == patient_id, "BillAmount"] = new_bill
        save_data(patients)  # save to CSV
        st.success(f"✅ Bill updated for Patient ID {patient_id}")
    else:
        st.error("❌ Patient ID not found.")

# Refresh session
st.session_state["patients"] = load_data()
