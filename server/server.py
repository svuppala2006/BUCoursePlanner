from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from gemini import generate_course_plan

app = FastAPI(docs_url="/api/docs")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your Next.js frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data model for the request
class CourseRequest(BaseModel):
    major: str
    career: str

@app.post("/api/generate")
async def generate_courses(request: CourseRequest):
    try:
        print(f"Received request - Major: {request.major}, Career: {request.career}")
        
        if not request.major or not request.career:
            raise HTTPException(status_code=400, detail="Major and career are required fields")
        
        # Generate course plan using Gemini
        try:
            course_plan = generate_course_plan(request.major, request.career)
        except Exception as e:
            print(f"Error in generate_course_plan: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to generate course plan: {str(e)}")
        
        # Save the generated plan to cs.json
        try:
            with open(os.path.join(os.path.dirname(__file__), 'cs.json'), 'w') as f:
                json.dump(course_plan, f, indent=4)
        except Exception as e:
            print(f"Error saving course plan: {str(e)}")
            # Don't fail the request if save fails, just log it
            pass
        
        return course_plan
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/api/")
async def get_current_plan():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'cs.json')) as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No course plan found")