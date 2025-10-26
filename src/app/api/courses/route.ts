import { NextResponse } from 'next/server';

export async function POST(request: Request) {
    try {
        const body = await request.json();
        
        // Validate request body
        if (!body.major || !body.career) {
            return NextResponse.json(
                { error: 'Major and career are required fields' },
                { status: 400 }
            );
        }

        // Send to FastAPI to generate course plan
        const response = await fetch('http://localhost:8000/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => null);
            const errorMessage = errorData?.detail || `HTTP error! status: ${response.status}`;
            console.error('Server error:', errorMessage);
            return NextResponse.json(
                { error: errorMessage },
                { status: response.status }
            );
        }

        const data = await response.json();
        return NextResponse.json(data);
    } catch (error) {
        console.error('Error generating course data:', error);
        return NextResponse.json(
            { error: 'Failed to generate course data' },
            { status: 500 }
        );
    }
}

export async function GET() {
    try {
        const response = await fetch('http://localhost:8000/api/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return NextResponse.json(data);
    } catch (error) {
        console.error('Error fetching course data:', error);
        return NextResponse.json({ error: 'Failed to fetch course data' }, { status: 500 });
    }
}