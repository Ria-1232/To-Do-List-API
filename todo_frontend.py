import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"  # Change this if hosted online

st.set_page_config(page_title="📝 To-Do App", layout="centered")
st.title("📝 To-Do List Web App")

# Fetch existing tasks
def get_tasks():
    response = requests.get(f"{API_URL}/todos/")
    return response.json()

# Add new task
def create_task(title, description):
    response = requests.post(f"{API_URL}/todos/", params={"title": title, "description": description})
    return response.json()

# Delete task
def delete_task(task_id):
    response = requests.delete(f"{API_URL}/todos/{task_id}")
    return response.ok

# Add new task form
st.subheader("➕ Add New Task")
with st.form(key="add_task_form"):
    title = st.text_input("Task Title")
    description = st.text_area("Task Description")
    submit_button = st.form_submit_button("Add Task")

    if submit_button and title:
        result = create_task(title, description)
        st.success(f"Task '{result['title']}' added!")

# Display tasks
st.subheader("📋 Your Tasks")
tasks = get_tasks()

if tasks:
    for task in tasks:
        st.write(f"**{task['title']}** – {task['description']}")
        if st.button(f"❌ Delete", key=f"delete_{task['id']}"):
            if delete_task(task['id']):
                st.success("Task deleted!")
                st.experimental_rerun()
else:
    st.info("No tasks found. Add one above.")
