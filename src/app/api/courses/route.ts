import { NextResponse } from 'next/server';

export async function GET() {
    try {
        const response = await fetch('http://localhost:8000/api/');
        const data = await response.json();
        return NextResponse.json(data);
    } catch (error) {
        console.error('Error fetching course data:', error);
        return NextResponse.json({ error: 'Failed to fetch course data' }, { status: 500 });
    }
}