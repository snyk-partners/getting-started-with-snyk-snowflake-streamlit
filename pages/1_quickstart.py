# Import Python Packages
import streamlit as st
from st_snowauth import snowauth_session


# NOTE: Table and fields names for demo purposes only,
# please refer to documentation and Snowflake for current specifications.

# Initialize or confirm OAuth connection to Snowflake backend using your credentials
session = snowauth_session()

# Load the table as a dataframe using the Snowpark Session.
df_snowpark = session.sql("SELECT o.DISPLAY_NAME,p.NAME,i.PROBLEM_TITLE,i.SCORE,i.ISSUE_SEVERITY,i.ISSUE_STATUS,p.PROJECT_TAGS, p.PROJECT_COLLECTIONS from SNYK.SNYK.ISSUES__V_1_0 i INNER JOIN SNYK.SNYK.PROJECTS__V_1_0 p ON i.PROJECT_PUBLIC_ID = p.PUBLIC_ID INNER JOIN SNYK.SNYK.ORGS__V_1_0 o ON i.ORG_PUBLIC_ID = o.PUBLIC_ID ORDER BY SCORE DESC;")

# Convert the Snowflake dataframe to a Pandas DataFrame
df = df_snowpark.to_pandas()

# Sidebar with options to filter data
with st.sidebar:
    st.title("Snyk Demo Quick Start Dashboard")
    st.write("This is a bit more complicated than the Getting Started page, but still pretty simple. \n\n You can filter the data by organization, project collection, project tags, and risk score. \n\n The data is then displayed in a table and simple bar chart.")

    # Create filter by orgs option
    orgs = df["DISPLAY_NAME"].unique().tolist()
    selected_orgs = st.multiselect("Select Organizations out of " + str(len(orgs)) + " options" , orgs)
    if not selected_orgs:
        selected_orgs = df["DISPLAY_NAME"].unique()

    # Filter by orgs selected
    df = df[df["DISPLAY_NAME"].isin(selected_orgs)]

    # Setting more filter options here by Snyk tags and Snyk project collections
    tags = df["PROJECT_TAGS"].unique().tolist()
    collections = df["PROJECT_COLLECTIONS"].unique().tolist()
    # Create streamlit multi select with options from Project Collections, Tags
    selected_collections = st.multiselect("Select Project Collections out of " + str(len(collections)) + " options" , collections)
    selected_tags = st.multiselect("Select Project Tags out of " + str(len(tags)) + " options" , tags)

    # Can also filter by risk/priority score too
    min_score = 0
    max_score = 1000
    min_col, max_col = st.columns(2)
    with min_col:
        min_score = st.number_input("Minimum Score", 0, max_score, 0)
    with max_col:
        max_score = st.number_input("Maximum Score", min_score, 1000, 1000)
    df = df[(df["SCORE"] >= min_score) & (df["SCORE"] <= max_score)]

    # Filter df with selected collections, tags
    if not selected_collections:
        selected_collections = df["PROJECT_COLLECTIONS"].unique()
    if not selected_tags:
        selected_tags = df["PROJECT_TAGS"].unique()
    df = df[df["PROJECT_COLLECTIONS"].isin(selected_collections) & df["PROJECT_TAGS"].isin(selected_tags)]

# Bar Chart of Open and Resolved Issues
# Count and display the number of open and resolved issues
open_issues = df[df["ISSUE_STATUS"] == "Open"].shape[0]
resolved_issues = df[df["ISSUE_STATUS"] == "Resolved"].shape[0]
values = [open_issues, resolved_issues]
labels = ["Open Issues", "Resolved Issues"]
data = {label: value for label, value in zip(labels, values)}
st.title("Open vs Resolved Issues")
st.bar_chart(data)

# Show first 10 (note: this is not top 10) issues
st.write(df.head(50))
