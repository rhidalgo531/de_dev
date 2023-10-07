import streamlit as st
import requests
import altair as alt
import pandas as pd

# Tableau Server configuration
TABLEAU_SERVER = 'https://your-tableau-server-url.com'
TABLEAU_API_VERSION = '3.12'
TABLEAU_SITE_ID = 'your-site-id'
TABLEAU_AUTH_TOKEN = 'your-auth-token'

# API endpoints
TABLEAU_API_BASE_URL = f"{TABLEAU_SERVER}/api/{TABLEAU_API_VERSION}"
TABLEAU_SITES_URL = f"{TABLEAU_API_BASE_URL}/sites/{TABLEAU_SITE_ID}"

# Set the Tableau REST API auth token in the request headers
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'X-Tableau-Auth': TABLEAU_AUTH_TOKEN
}

# Define admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin@123'


def get_users():
    url = f"{TABLEAU_SITES_URL}/users"
    response = requests.get(url, headers=headers)
    return response.json()['users']['user']


def add_user(username, fullname, site_role):
    url = f"{TABLEAU_SITES_URL}/users"
    payload = {
        "user": {
            "name": username,
            "fullName": fullname,
            "siteRole": {
                "name": site_role
            }
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    return response


def delete_user(user_id):
    url = f"{TABLEAU_SITES_URL}/users/{user_id}"
    response = requests.delete(url, headers=headers)
    return response


# Streamlit app
def main():
    st.title("Tableau Admin Operations")

    # User login
    st.sidebar.header("Admin Login")
    username_input = st.sidebar.text_input("Username")
    password_input = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if username_input == ADMIN_USERNAME and password_input == ADMIN_PASSWORD:
            st.sidebar.success("Logged in as admin")
            show_admin_interface()
        else:
            st.sidebar.error("Invalid credentials")


def show_admin_interface():
    # Add a left navigation sidebar
    st.sidebar.header("Navigation")
    nav_selection = st.sidebar.selectbox("Select Operation", ["List Users", "Add User", "Delete User", "User Count",
                                                              "License Type"])

    if nav_selection == "List Users":
        st.header("Users")
        users = get_users()
        for user in users:
            st.write(f"Username: {user['name']}, Full Name: {user['fullName']}, Role: {user['siteRole']['name']}")

    elif nav_selection == "Add User":
        st.header("Add User")
        username = st.text_input("Username")
        fullname = st.text_input("Full Name")
        site_role = st.selectbox("Site Role", ["Viewer", "Explorer", "Creator"])
        if st.button("Add User"):
            response = add_user(username, fullname, site_role)
            if response.status_code == 200:
                st.success("User added successfully!")
            else:
                st.error("Failed to add user.")

    elif nav_selection == "Delete User":
        st.header("Delete User")
        user_id = st.text_input("User ID")
        if st.button("Delete User"):
            response = delete_user(user_id)
            if response.status_code == 204:
                st.success("User deleted successfully!")
            else:
                st.error("Failed to delete user.")

    elif nav_selection == "User Count":
        st.header("User Count")
        users = get_users()
        user_counts = {}
        for user in users:
            license_type = user['siteRole']['name']
            if license_type in user_counts:
                user_counts[license_type] += 1
            else:
                user_counts[license_type] = 1

        # Create a DataFrame from user_counts
        df_user_counts = pd.DataFrame.from_dict(user_counts, orient='index', columns=['Count'])
        df_user_counts.reset_index(inplace=True)
        df_user_counts.rename(columns={'index': 'License Type'}, inplace=True)

        # Create an Altair bar chart
        chart = alt.Chart(df_user_counts).mark_bar().encode(
            x='License Type',
            y='Count'
        ).properties(
            width=600,
            height=400
        )

        # Display the chart using Streamlit
        st.altair_chart(chart, use_container_width=True)


if __name__ == '__main__':
    main()
