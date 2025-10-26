import google.generativeai as genai
import os
import pathlib
import json
from typing import Dict, Any

def generate_course_plan(major: str, career: str) -> Dict[str, Any]:
    try:
        csv_path = pathlib.Path("IS2.csv")
        
        # Initialize Gemini API
        genai.configure(api_key='AIzaSyA1PsU1haI-A3QLzF8YT3WppKnBWDQaRO0')

        # --- 2. Upload the CSV file to the Google Files API ---
        print(f"Uploading file '{csv_path.name}'...")
        # upload_file() returns a File object
        uploaded_file = genai.upload_file(
            path=csv_path,
            display_name="Courses"
        )
        print(f"Uploaded file: {uploaded_file.display_name} (URI: {uploaded_file.uri})")

        # --- 3. Use the file in a prompt ---
        # We must use a model that supports file inputs, like gemini-1.5-pro
        model = genai.GenerativeModel(model_name="gemini-2.5-pro")
        # The prompt is a list containing text and the File object
        example_json = '''{
    "degree": "BA in Computer Science",
    "college": "College of Arts & Sciences",
    "total_credits": 132,
    "total_courses": 33,
    "disclaimer": "This information is for informational purposes only and should be verified with official BU sources.",
    "note": "Courses marked with is_major_requirement=true count toward the 15 required CS major courses. Additional courses fulfill CAS general education (BU Hub), language requirement, and elective requirements.",
    "schedule": [
        {
            "year": 1,
            "semester": "Fall",
            "courses": [
                {
                    "courseID": "CAS CS 111",
                    "name": "Introduction to Computer Science 1",
                    "credit_hours": 4,
                    "hub_credits": [
                        "Quantitative Reasoning II",
                        "Creativity/Innovation",
                        "Critical Thinking"
                    ],
                    "is_major_requirement": true,
                    "major_group": "Group A - Required"
                }
            ],
            "semester_credits": 16
        }
    ],
    "summary": {
        "total_bu_hub_requirements": 26,
        "total_credits_breakdown": {
            "major_credits": 60,
            "hub_requirements": 36,
            "electives": 32,
            "total": 128
        }
    }
}'''
        
        prompt_text = f'''Given that I am a freshman at Boston University majoring in {major} with a desired career of becoming a {career}, webscrape the requirements for the major from the BU degree's website. Using that information, parse through the CSV and create a full 4 year course catalog. 

This should be returned in a json format following EXACTLY the structure of this example, but using information for my major and selected career. The response must contain 8 semesters (4 years) worth of courses:

{example_json}

Important:
1. Maintain the exact same JSON structure
2. Include all 8 semesters (4 years)
3. Each course should have all the same fields as shown in the example
4. All credit calculations should be accurate
5. Return valid JSON only'''

        prompt_parts = [
            prompt_text,
            uploaded_file]

        print("\nSending prompt to Gemini...")
        
        # --- 4. Print the output ---
        response = model.generate_content(contents=prompt_parts, generation_config={
            "response_mime_type": "application/json"
        })
        
        print("\n--- Gemini Response ---")
        print("-----------------------")
        return json.loads(response.text)

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please ensure your API key is correct and has File API permissions.")

    finally:
    #     # --- 5. (Optional) Clean up ---
        
        # Delete the file from the server
        if 'uploaded_file' in locals() and uploaded_file:
            print(f"\nDeleting server file: {uploaded_file.display_name}")
            genai.delete_file(uploaded_file.name)
        
#     # Delete the local dummy file
#     if csv_path.exists():
#         print(f"Deleting local file: {csv_path.name}")
#         csv_path.unlink()