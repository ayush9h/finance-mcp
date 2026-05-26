import asyncio
import json

import pandas as pd
import streamlit as st

from workflow import InvestorWorkflow

st.set_page_config(
    page_title="Finance MCP Demo",
    layout="wide",
)

st.title("Finance MCP Workflow Dashboard")

st.markdown("---")

with st.sidebar:

    st.header("Workflow Input")

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
        width=True,
    )

col1, col2 = st.columns([1, 2])

with col1:

    st.subheader("Workflow Stages")

    workflow_placeholder = st.empty()

    logs_placeholder = st.empty()

with col2:

    st.subheader("Links found in the Website")

    table_placeholder = st.empty()

    download_placeholder = st.empty()

if run_button:

    if not company_name or not company_country:

        st.error("Company name and country are required")

    else:

        workflow = InvestorWorkflow()

        workflow_placeholder.info("Starting workflow...")

        with st.spinner("Executing workflow..."):

            result = asyncio.run(
                workflow.execute(
                    company_name=company_name,
                    company_country=company_country,
                )
            )

        if result["status"] != "success":

            st.error(result["message"])

        else:

            workflow_placeholder.success("Workflow completed successfully")

            logs_placeholder.code(
                "\n".join(result["logs"]),
                language="text",
            )

            df = pd.DataFrame({"Links": result["links"]})

            table_placeholder.dataframe(
                df,
                width=True,
            )

            json_data = json.dumps(
                result,
                indent=2,
                ensure_ascii=False,
            )

            download_placeholder.download_button(
                label="Download JSON",
                data=json_data,
                file_name=f"{company_name}_reports.json",
                mime="application/json",
            )

            csv_data = df.to_csv(index=False)

            download_placeholder.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"{company_name}_reports.csv",
                mime="text/csv",
            )
