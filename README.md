## BU Course Planner

This project takes input from the user asking for their desired major and career. It assumes that the user is a freshman with no credits coming into college. It outputs a full course plan for the next 4 years at BU that matches with the users career and completes all degree requirements. 

## How to Run

1) Make sure you have Node, npm, and python all installed

2) Run the following commands in the terminal from the root of the project to install the project dependencies
```console
npm install
python -m venv my_env  # Create a virtual environment named 'my_env'
.\my_env\Scripts\activate
.\my_env\Scripts\activate # Activate the virtual environment (on Windows)
# For Linux/Mac: .\my_env\Scripts\activate
pip install -r requirements.txt
```

3) In the server subdirectory, create a .env.local file and add the following line using your own Google Gemini API key
```code
API_KEY="<Insert API Key here>"
```

4) To run the project, in one terminal, run:
```console
npm run dev
```

And in another terminal, run:
```console
cd server
uvicorn server:app --reload --port 8000
```
