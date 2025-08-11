// File: app/api/auth/session/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { getAuthenticatedUser } from '@/lib/auth';

export const dynamic = 'force-dynamic';

export async function GET(req: NextRequest) {
    try {
        const user = await getAuthenticatedUser(req);
        return NextResponse.json({ user }, { status: 200 });
    } catch (error) {
        console.error('Session verification error:', error);
        return NextResponse.json({ message: 'An internal error occurred.' }, { status: 500 });
    }
}