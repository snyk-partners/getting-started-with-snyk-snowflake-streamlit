import streamlit as st
# import pandas as pd
from st_snowauth import snowauth_session

# Initialize or confirm OAuth connection to Snowflake backend using your credentials
session = snowauth_session()

# NOTE: Table and fields names for demo purposes only,
# please refer to documentation and Snowflake for current specifications.

# Load the table as a dataframe using the Snowpark Session.
df_snowpark = session.sql("SELECT o.DISPLAY_NAME,p.NAME,i.PROBLEM_TITLE,i.SCORE,i.ISSUE_SEVERITY,i.ISSUE_STATUS,p.PROJECT_TAGS,p.PROJECT_COLLECTIONS from SNYK.SNYK.ISSUES__V_1_0 i INNER JOIN SNYK.SNYK.PROJECTS__V_1_0 p ON i.PROJECT_PUBLIC_ID = p.PUBLIC_ID INNER JOIN SNYK.SNYK.ORGS__V_1_0 o ON i.ORG_PUBLIC_ID = o.PUBLIC_ID ORDER BY SCORE DESC;")

# Convert the Snowflake dataframe to a Pandas DataFrame
df = df_snowpark.to_pandas()

with st.sidebar:
    st.title("Getting Started")
    st.write("""
            This is a demo of the Snowflake<>Snyk integration with a few varying levels of complexity.
             Each of the pages above will hopefully show you something new about working with streamlit.
             Feel free to take any of the code snippets and use them in your own projects. \n\n This first page
             is focused just on getting the data from Snowflake and showing a simple representation of the data.
             \n\n With each of these, the code is to serve as starter code. There may be bugs, there may be issues but 
             hopefully it can help you get started with getting value out of Snyk's Snowflake integration quickly :)
            """)

# Bar Chart of Open and Resolved Issues
# Count and display the number of open and resolved issues
open_issues = df[df["ISSUE_STATUS"] == "Open"].shape[0]
resolved_issues = df[df["ISSUE_STATUS"] == "Resolved"].shape[0]
values = [open_issues, resolved_issues]
labels = ["Open Issues", "Resolved Issues"]
data = {label: value for label, value in zip(labels, values)}
st.title("Open vs Resolved Issues")
st.bar_chart(data)

st.write(df.head(50))
