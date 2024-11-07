# TextToSql [Local Machine Setup]

1.	Clone or download this repository.
2.	Install required libraries:
    "pip install -r requirements.txt"
3.	Create a ".streamlit" folder in the project’s base directory.
4.	Create a "secrets.toml" file inside the ".streamlit" folder:
5.	Copy and paste the following code into secrets.toml, replacing YOUR_API_KEY with your actual API key:

    [OpenAiGoogleGenAI]
    apiKey = "YOUR_API_KEY"

6.	Run the application:
    "streamlit run main.py"
7.	(Optional) Start your MySQL database if it’s not already running. Ensure the database details (host, user, password) match those entered in the Streamlit app.