import streamlit as st
import pandas as pd
from db_fxns import *  # Ensure this module contains the necessary database functions
import streamlit.components.v1 as stc
import plotly.express as px

# HTML Banner
HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">ToDo App</h1>
    <p style="color:white;text-align:center;">Built with Streamlit</p>
    </div>
"""

def main():
    stc.html(HTML_BANNER)
    menu = ["Create", "Read", "Update", "Delete", "About"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    create_table()  # Ensure the database table exists
    
    if choice == "Create":
        st.subheader("Add Task")
        col1, col2 = st.columns(2)
        with col1:
            task = st.text_area("Task To Do")
        with col2:
            task_status = st.selectbox("Status", ["ToDo", "Doing", "Done"])
            task_due_date = st.date_input("Due Date")
        
        if st.button("Add Task"):
            try:
                add_data(task, task_status, task_due_date)
                st.success(f"Added Task: {task}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
    elif choice == "Read":
        st.subheader("View Tasks")
        
        with st.expander("All Tasks"):
            result = view_all_data()
            clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
            st.dataframe(clean_df)
        
        with st.expander("Task Status Distribution"):
            if not clean_df.empty:
                task_df = clean_df['Status'].value_counts().reset_index()
                task_df.columns = ['Status', 'Count']
                st.dataframe(task_df)
                p1 = px.pie(task_df, names='Status', values='Count', title="Task Status Distribution")
                st.plotly_chart(p1, use_container_width=True)
            else:
                st.warning("No data available to display the chart.")
    
    elif choice == "Update":
        st.subheader("Edit Task")
        
        with st.expander("Current Data"):
            result = view_all_data()
            clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
            st.dataframe(clean_df)
        
        list_of_tasks = [i[0] for i in view_all_task_names()]
        selected_task = st.selectbox("Select Task", list_of_tasks)
        task_result = get_task(selected_task)
        
        if task_result:
            task, task_status, task_due_date = task_result[0]
            col1, col2 = st.columns(2)
            with col1:
                new_task = st.text_area("Task To Do", task)
            with col2:
                new_task_status = st.selectbox("Status", ["ToDo", "Doing", "Done"], index=["ToDo", "Doing", "Done"].index(task_status))
                new_task_due_date = st.date_input("Due Date", task_due_date)
            
            if st.button("Update Task"):
                try:
                    edit_task_data(new_task, new_task_status, new_task_due_date, task, task_status, task_due_date)
                    st.success(f"Updated Task: {task} -> {new_task}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
    
    elif choice == "Delete":
        st.subheader("Delete Task")
        
        with st.expander("View Data"):
            result = view_all_data()
            clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
            st.dataframe(clean_df)
        
        unique_list = [i[0] for i in view_all_task_names()]
        delete_by_task_name = st.selectbox("Select Task", unique_list)
        
        if st.button("Delete"):
            try:
                delete_data(delete_by_task_name)
                st.warning(f"Deleted Task: {delete_by_task_name}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
    else:
        st.subheader("About ToDo List App")
        st.info("Manage your daily tasks easily with this To-Do app!")
        st.text("Created by Maroof Husain")

if __name__ == '__main__':
    main()
