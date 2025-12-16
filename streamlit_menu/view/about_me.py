import streamlit as st
import re
import requests

#from ../forms/contact import contact_form
WEBHOOK_URL = ""

def is_email_valid(email):
    #Basic regex pattern for email validation
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(email_pattern, email) is not None

def contact_form():
    with st.form("contact_form"):
        name = st.text_input("First Name")
        email = st.text_input("Email Address")
        message = st.text_input("Your Message")
        submit = st.form_submit_button("Submit")

        if submit:
            if not WEBHOOK_URL:
                st.error("Email Service is not set up. Please try again later.", icon = "🆘")
                st.stop()
            if not name:
                st.error("Please provide your first name.")
                st.stop()

            if not email:
                st.error("Please provide your email address.")
                st.stop()

            if not is_email_valid(email):
                st.error("Please enter a valid email address.")
                st.stop()

            if not message:
                st.error("Please provide a message.")
                st.stop()

            #  Prepare the data payload and send it to a specified webhook url
            data = {
                "name": name,
                "email": email,
                "message": message,
            }
            response = requests.post(WEBHOOK_URL, json=data)

            if response.status_code == 200:
                st.success("Your message has been sent successfully! 🎉.", icon="🚀")
            else:
                st.error("Something went wrong. Please try again later.", icon = "😮")

        st.success("Message successfully send")

@st.dialog("Contact Me")
def  show_contact_form():
    #st.title("Contact Me")
    contact_form()

#---Hero Section ---
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.image("streamlit_menu/images/profile_image.jpeg", width=300)
with col2:
    st.title("Paolo Nangue", anchor=False)
    st.write("I’m currently studying Computer Science in my 4th semester at Hochschule Darmstadt. I have hands-on experience with C++ and "
             "Python and enjoy developing efficient and creative software solutions.")
    if st.button("📨 Contact Me"):
        show_contact_form()

# --- EXPERIENCE & QUALIFICATIONS ---
st.write("\n")
st.subheader("Experience & Qualification", anchor=False)
st.write(
    """
    - Working knowledge of Python with hands-on project experience
    - Excellent Team-Player and displaying a strong sense of initiative on tasks
   """
)

# --- SKILLS ---
st.write("\n")
st.subheader("Hard Skills", anchor=False)
st.write(
    """
    - Programming: Python (Scikit-learn, Pandas, Numpy), C++, SQL
    - Data Visualization: MS Excel, Plotly
    - Modeling: Linear Regression, Binary Classification
    - Databases: Postgres, MySQL    
    """
)