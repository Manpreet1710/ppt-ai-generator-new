import { NextRequest, NextResponse } from "next/server";

export async function GET() {
  try {
    const response = await fetch("http://localhost:8000/api/v1/user-config", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error("Error fetching user config:", error);
    return NextResponse.json(
      { error: "Failed to fetch user config" },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const response = await fetch("http://localhost:8000/api/v1/user-config", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const errorData = await response.json();
      return NextResponse.json(
        { error: errorData.detail || "Failed to save user config" },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error("Error saving user config:", error);
    return NextResponse.json(
      { error: "Failed to save user config" },
      { status: 500 }
    );
  }
}
