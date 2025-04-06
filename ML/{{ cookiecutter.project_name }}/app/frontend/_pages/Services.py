import streamlit as st
from {{ cookiecutter.package_slug }}.utils.reader import Reader
import os

def get_file_names_without_extension(folder_path):
    try:
        # List all files and remove extensions
        files = [os.path.splitext(f)[0] for f in os.listdir(folder_path) if not os.path.splitext(f)[0].startswith(".")]
        return files
    except Exception as e:
        return []

PROCESSED_PATH = "../../data/processed"

ANALYSIS_PATH = "../../reports/analysis"
CORRELATION_PATH = ANALYSIS_PATH + "/correlation"
DESCRIPTION_PATH = ANALYSIS_PATH + "/description"
DETECTION_PATH = ANALYSIS_PATH + "/detection"


st.title("Services")
st.write("Here are the services we offer.")

tabs = st.tabs(["Data Analysis", "Data visualization", "Service 3"])


with st.spinner("Loading data..."):
    dataframes = Reader.read_all_files_in_directory(PROCESSED_PATH)
    correlations = Reader.read_all_files_in_directory(CORRELATION_PATH)
    descriptions = Reader.read_all_files_in_directory(DESCRIPTION_PATH)
    detections = Reader.read_all_files_in_directory(DETECTION_PATH)




with tabs[0]:
    st.write("Get your data analysis.")

    st.markdown(
        """
            <div style='color: red; font-weight: bold;'>⚠️ Note: This section need the data of reports meaning you have to launch the analysis first:</div>
            <code style='color: red; font-weight: bold;'>make run_analysis</code>
        """,
        unsafe_allow_html=True
    )

    datas = get_file_names_without_extension(PROCESSED_PATH)
    selection = st.selectbox("Select the data you want to analyze.", datas)
    if selection:
        st.write("Header display of the data.")
        st.dataframe(dataframes[selection].head(), use_container_width=True)

        try:
            if selection in correlations:
                st.title("Correlation:")
                st.dataframe(correlations[selection], use_container_width=True)

            if any([selection+"_number_description" in descriptions, selection+"_string_description" in descriptions]):
                st.title("Description:")
                col1, col2 = st.columns(2)
                with col1:
                    st.write("For Number type:")
                    st.dataframe(descriptions[selection+"_number_description"], use_container_width=True)
                with col2:
                    st.write("For String type:")
                    st.dataframe(descriptions[selection+"_string_description"], use_container_width=True)

            if selection in detections:
                st.title("Mismatch types in data:")
                st.dataframe(detections[selection], use_container_width=True)
        except Exception:
            st.write("No data analysis to display!!!")
            st.markdown(
                """
                    <div style='color: red; font-weight: bold;'>⚠️ Note: This section need the data of reports meaning you have to launch the analysis first:</div>
                    <code style='color: red; font-weight: bold;'>make run_analysis</code>
                """,
                unsafe_allow_html=True
            )


with tabs[1]:
    st.write("Service 2 details here.")


with tabs[2]:
    st.write("Service 3 details here.")