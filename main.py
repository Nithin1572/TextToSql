import streamlit as st  # type: ignore
import mysql.connector  # type: ignore
from mysql.connector import Error

# Title and Input Fields
st.write("## Enter Database Details")

# Input for database connection parameters
hostName = st.text_input("Enter Host Name:", placeholder="e.g., localhost")
userName = st.text_input("Enter User Name:", placeholder="e.g., root")
password = st.text_input("Enter Password:", type='password', placeholder="Your Password")
dataBaseName = st.text_input("Enter Database Name:", placeholder="e.g., test")

# Text input and button
question = st.text_input("Enter Query in Natural Language:")
textToSql = st.button("Generate SQL")

if textToSql:
    # Ensure all inputs are filled
    if not (hostName and userName and dataBaseName):
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
                mainQuery = f'Given the database "{dataBaseName}" containing the following tables and their descriptions:\n'
                
                listOfTables = f"SHOW TABLES FROM {dataBaseName}"
                cursor.execute(listOfTables)
                tables = cursor.fetchall()

                # Iterate over tables and describe their structure
                for table in tables:
                    tableName = table[0]
                    mainQuery += f'\nTable "{tableName}" contains the following fields:\n'

                    cursor.execute(f"DESCRIBE {tableName}")
                    fields = cursor.fetchall()

                    # Iterate over fields and describe them
                    for field in fields:
                        fieldName, fieldType, isNull, fieldKey, defaultValue, extra = field
                        fieldDescription = f'- "{fieldName}": Type: {fieldType}'
                        if defaultValue is not None:
                            fieldDescription += f", Default: {defaultValue}"
                        if extra:
                            fieldDescription += f", Extra: {extra}"
                        mainQuery += fieldDescription + "\n"

                # Display the generated query description
                st.text_area("Generated Natural Language Query:", mainQuery, height=300)

            # Close the connection
            conn.close()

        except Error as e:
            st.error(f"Error: {str(e)}")