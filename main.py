import streamlit as st  # type: ignore
import mysql.connector  # type: ignore
from mysql.connector import Error  # type: ignore
import google.generativeai as genai #type: ignore
import os


# Title and Input Fields
st.title("Natural Language to SQL Generator")
st.write("## Enter Database Details")

# Verify if API key exists in secrets
if "OpenAi" not in st.secrets or "apiKey" not in st.secrets["OpenAi"]:
    st.error("API key not found. Please add it to your Streamlit secrets.")
else:
    googleApiKey = st.secrets["GoogleGenAI"]["apiKey"]
    genai.configure(api_key=googleApiKey)

    # Input for database connection parameters
    hostName = st.text_input("Enter Host Name:", placeholder="e.g., localhost")
    userName = st.text_input("Enter User Name:", placeholder="e.g., root")
    password = st.text_input("Enter Password:", type="password", placeholder="Your Password")
    dataBaseName = st.text_input("Enter Database Name:", placeholder="e.g., test")

    # Text input and button for query generation
    question = st.text_input("Enter Query in Natural Language:")
    textToSql = st.button("Generate SQL")

    if textToSql:
        # Ensure all inputs are filled
        if not (hostName and userName and dataBaseName and question):
            st.error("Please fill in all required fields.")
        else:
            try:
                # Connect to MySQL database
                conn = mysql.connector.connect(
                    host=hostName,
                    user=userName,
                    password=password,
                    database=dataBaseName
                )

                if conn.is_connected():
                    st.success(f"Connected to the '{dataBaseName}' database successfully!")

                    # Prepare query to get table information
                    cursor = conn.cursor()
                    mainQuery = (
                        f'Given the database "{dataBaseName}" containing the following tables '
                        "and their descriptions:\n"
                    )

                    cursor.execute(f"SHOW TABLES FROM {dataBaseName}")
                    tables = cursor.fetchall()

                    # Iterate over tables and describe their structure
                    for table in tables:
                        tableName = table[0]
                        mainQuery += f'\nTable "{tableName}" contains the following fields:\n'

                        cursor.execute(f"DESCRIBE {tableName}")
                        fields = cursor.fetchall()

                        # Describe each field in the table
                        for field in fields:
                            (
                                fieldName,
                                fieldType,
                                isNull,
                                fieldKey,
                                defaultValue,
                                extra,
                            ) = field
                            fieldDescription = f'- "{fieldName}": Type: {fieldType}'
                            if defaultValue is not None:
                                fieldDescription += f", Default: {defaultValue}"
                            if extra:
                                fieldDescription += f", Extra: {extra}"
                            mainQuery += fieldDescription + "\n"

                    # Add user question to main query
                    mainQuery += f'Find the {question}.'

                    try:
                        model = genai.GenerativeModel("gemini-pro")
                        response = model.generate_content(mainQuery)
                        st.text_area("Generated Natural Language Query:", mainQuery, height=300)
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"Gemini API Error: {str(e)}")
                        

                # Close the connection
                conn.close()

            except Error as e:
                st.error(f"MySQL Error: {str(e)}")
            except Exception as e:
                st.error(f"Unexpected Error: {str(e)}")

                