import asyncio
import json

import pandas as pd
import streamlit as st

from src.workflow import InvestorWorkflow

st.set_page_config(
    page_title="Finance MCP Playground",
    layout="wide",
)

st.markdown(
    """
    <style>

    .stApp {
        background-color: #000000;
        color: #ffffff;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    [data-testid="stSidebar"] {
        background-color: #000000;
        border-right: 1px solid #222222;
    }

    [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }

    .stTextInput input {
        background-color: #0a0a0a !important;
        color: #ffffff !important;
        border: 1px solid #333333 !important;
        border-radius: 6px !important;
    }

    .stButton > button {
        width: 100%;
        background-color: #ffffff;
        color: #000000;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        padding: 0.75rem;
    }

    .stButton > button:hover {
        background-color: #e5e5e5;
    }

    .stDownloadButton > button {
        width: 100%;
        background-color: #ffffff;
        color: #000000;
        border: none;
        border-radius: 6px;
        font-weight: 600;
    }

    h1, h2, h3 {
        color: #ffffff !important;
    }

    .status-card {
        border: 1px solid #222222;
        border-radius: 8px;
        padding: 16px;
        background-color: #050505;
        margin-bottom: 20px;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #222222;
        border-radius: 8px;
        overflow: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <h1 style="text-align:center;">
        Finance MCP Playground
    </h1>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:

    st.markdown("## Parameters")

    company_name = st.text_input(
        "Company Name",
        placeholder="Nestle",
    )

    company_country = st.text_input(
        "Company Country",
        placeholder="India",
    )

    run_button = st.button(
        "Run Workflow",
        use_container_width=True,
    )

st.markdown("### Workflow Status")

workflow_placeholder = st.empty()

links_container = st.container()

if run_button:

    if not company_name or not company_country:

        st.error("Company name and country are required.")

    else:

        workflow = InvestorWorkflow()

        with st.spinner("Running workflow"):

            result = asyncio.run(
                workflow.execute(
                    company_name=company_name,
                    company_country=company_country,
                )
            )
            links = result.get("links", [])

            if links:

                if isinstance(links[0], dict):

                    df = pd.json_normalize(links)

                else:

                    df = pd.DataFrame({"Annual Report Links": links})

            else:

                df = pd.DataFrame(columns=["Annual Report Links"])

            json_data = json.dumps(
                result,
                indent=2,
                ensure_ascii=False,
            )

            csv_data = df.to_csv(index=False)

            with links_container:

                st.markdown("### Links Found")

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                )

                st.markdown("")

                col1, col2 = st.columns(2)

                with col1:

                    st.download_button(
                        label="Download JSON",
                        data=json_data,
                        file_name=f"{company_name}_reports.json",
                        mime="application/json",
                        use_container_width=True,
                    )

                with col2:

                    st.download_button(
                        label="Download CSV",
                        data=csv_data,
                        file_name=f"{company_name}_reports.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )
