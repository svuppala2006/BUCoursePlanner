import google.generativeai as genai
import os
import pathlib
import json

# --- 0. Create a dummy CSV file ---
# In a real application, you would just use the path to your existing file.
try:
    csv_path = pathlib.Path("courses.csv")

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
    model = genai.GenerativeModel(model_name="gemini-2.0-flash-lite")

    # The prompt is a list containing text and the File object
    prompt_parts = [
        "Please analyze the attached json file \n",
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