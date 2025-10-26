import google.generativeai as genai
import os
import pathlib
import json

# --- 0. Create a dummy CSV file ---
# In a real application, you would just use the path to your existing file.
try:
    csv_path = pathlib.Path("IS2.csv")

    # with open('output_courses.json', 'r') as file:
    #     data = json.load(file)
    
    # --- 1. Initialize the Gemini API ---
    genai.configure(api_key='AIzaSyBRI0YMwGPOgzqqJCttsM0EMWr9SQbEou0')

    # --- 2. Upload the CSV file to the Google Files API ---
    print(f"Uploading file '{csv_path.name}'...")
    # upload_file() returns a File object
    uploaded_file = genai.upload_file(
        path=csv_path,
        display_name="Courses",
        mime_type="text/csv"
    )
    print(f"Uploaded file: {uploaded_file.display_name} (URI: {uploaded_file.uri})")

    # --- 3. Use the file in a prompt ---
    # We must use a model that supports file inputs, like gemini-1.5-pro
    model = genai.GenerativeModel(model_name="gemini-2.5-pro")

    # The prompt is a list containing text and the File object
    major = "Biology"
    career = "Microbiologist"
    prompt_parts = [
        '''Given that I am a freshman at Boston University majoring in {major} with a desired career of becoming a {career} webscrape the requirement for the major from the BU degree's website. Using that information, parse through the CSV and create a full 4 year course catalog. This should be returned in a json format with the similar format as the following example but should use information for my major and selected career, but should contain 8 semesters or 4 years worth of courses:

{
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
                },
                {
                    "courseID": "CAS MA 123",
                    "name": "Calculus I",
                    "credit_hours": 4,
                    "hub_credits": [
                        "Quantitative Reasoning I"
                    ],
                    "is_major_requirement": false,
                    "notes": "Related requirement for CS major"
                },
                {
                    "courseID": "CAS WR 120",
                    "name": "Writing Seminar",
                    "credit_hours": 4,
                    "hub_credits": [
                        "First-Year Writing Seminar"
                    ],
                    "is_major_requirement": false,
                    "notes": "Required for all CAS students"
                },
                {
                    "courseID": "CAS AN 211",
                    "name": "Philosophical/Aesthetic/Historical Interpretation",
                    "credit_hours": 4,
                    "hub_credits": [
                        "Philosophical Inquiry and Life's Meanings OR Aesthetic Exploration OR Historical Consciousness"
                    ],
                    "is_major_requirement": false,
                    "notes": "Choose from available Hub courses"
                }
            ],
            "semester_credits": 16
        }
],
    "summary": {
        "total_cs_major_courses": 15,
        "group_a_required": 5,
        "group_b_required_minimum": 2,
        "group_c_required_minimum": 2,
        "group_d_electives_minimum": 3,
        "total_bu_hub_requirements": 26,
        "total_credits_breakdown": {
            "cs_major": 60,
            "related_requirements": 16,
            "hub_requirements": 36,
            "unrestricted_electives": 8,
            "language_requirement": 8,
            "total": 128
        }
    },
    "important_notes": [
        "All 15 CS major courses must be completed with a grade of C or higher",
        "Group C courses (CS 320, CS 411, others) MUST be taken at BU - cannot be transferred",
        "BU Hub requirements total 26 for first-year entering students",
        "Language requirement must be completed through intermediate (4th term) level",
        "This schedule assumes Fall/Spring only, no summer courses"
    ]
}  ''',
        uploaded_file # Pass the File object directly
    ]

    print("\nSending prompt to Gemini...")
    
    # --- 4. Print the output ---
    response = model.generate_content(contents=prompt_parts)
    
    print("\n--- Gemini Response ---")
    print(response.text)
    print("-----------------------")

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