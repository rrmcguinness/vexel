import { NextResponse } from 'next/server';
import { cookies } from 'next/headers';

const SESSION_COOKIE_NAME = 'auth_session_token';

export async function GET() {
    try {
        // To log the user out, we need to clear the session cookie.
        // The `cookies().set()` method with `maxAge: 0` is the standard way to do this.
        cookies().set(SESSION_COOKIE_NAME, '', { maxAge: 0 });

        return NextResponse.json({ message: 'Logged out successfully' }, { status: 200 });

    } catch (error) {
        console.error('Logout API error:', error);
        return NextResponse.json({ message: 'An error occurred during logout.' }, { status: 500 });
    }
}
