# Getting Started with Snyk, Snowflake, and Streamlit

This is a demo of how to get started with Snyk's Snowflake integration. More info on this integration can be found in our docs [here](https://docs.snyk.io/manage-risk/reporting/reporting-and-bi-integrations-snowflake-data-share).

This repo has four example files with varying levels of complexity.
- get_started: how to retrieve data from snowflake and display it in a bar chart or as a table
- quickstart: a bit more complex, showing various ways to create filters
- sla dashboard: a more realistic example of a type of dashboard a customer may need
- pr checks: an example of incorporating GitHub data with Snyk data to show pr checks configured for Snyk known projects

In any case, this repo is to serve for **demo purposes only**. The SLA dashboard in particular is not endorsed by Snyk and is not necessarily how Snyk's own SLA dashboard calculates SLAs etc. Some of the code likely does have bugs but hopefully it can serve as inspiration for how you may work with Snyk's Snowflake integration if you wish to build on top of Streamlit

For full Streamlit documentation, see [here](https://docs.streamlit.io/)

> **Note:**  Table and fields names for demo purposes only, please refer to documentation and Snowflake for current specifications.

## Getting Started

To get started with this project, you'll need to follow these steps:

1. Create a folder named `.streamlit` with a file `secrets.toml` from the root directory of this project. The full file path from the root should then be `.streamlit/secrets.toml`
2. Use the instructions found at https://medium.com/snowflake/snowflake-oauth-for-streamlit-e95e4cb3de6c to create a Snowflake OAuth Security Integration.
3. Define your Snowflake secrets in the `secrets.toml` file. Make sure to include the necessary credentials and connection details as detailed from Step 2.

    It should look like this:
    ```    
    [snowauth]
    account = "my-snowflake-account-name"
    authorization_endpoint = "my-snowflake-authorization-endpoint"
    token_endpoint = "my-snowflake-token-endpoint"
    client_id = "my-snowflake-client-id"
    client_secret = "my-snowflake-client-secret"
    redirect_uri = "http://localhost:8501"
    role = "DATA_SHARE_ROLE"
    ```

    Also add your GH Secret to a `.env` file in the root directory if you are using the PR Check dashboard. NOTE: You need a token with fine grained access for the PR Check dashboard. See `GH_Permissions.png` for permissions required for the token.

    ```
    GH_TOKEN=
    ```
    Note: if you run the pr checks report repeatedly for a large set of GH repos, you may encounter an API request limit from GitHub.

4. You will need a virtual environment for python that allows you to run python 3.8.20 used by the snowauth library. I used pyenv
    ```shell
    pyenv install 3.8.20
    pyenv vitrualenv 3.8.20 streamlit 
    pyenv activate streamlit
    ```

5. Once `pyenv` is installed, navigate to the project directory and run the following command to install the project dependencies:

    ```shell
    pip install streamlit
    xcode-select --install
    pip install watchdog
    pip install snowflake-connector-python
    pip install git+https://github.com/sfc-gh-bhess/st_snowauth.git@v1.3
    pip install dotenv
    pip install ghapi
    ```
6. After installing the prereq packages, run the streamlit app locally. Specify the dashboard you want to run. Example below:

    ```shell
    streamlit run 0_Get_Started.py
    ```
