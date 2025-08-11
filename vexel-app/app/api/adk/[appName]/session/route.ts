// File: app/api/adk/[appName]/session/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { getAuthenticatedUser } from '@/lib/auth';
import { OpenAPI, DefaultService } from '@/lib/adk-client'
import { HashEmail } from "@/lib/model";

const ADK_API_BASE_URL = process.env.ADK_API_BASE_URL || 'http://127.0.0.1:8000';
OpenAPI.BASE = ADK_API_BASE_URL;
OpenAPI.CREDENTIALS = "include"
OpenAPI.TOKEN = "include"

export async function POST(req: NextRequest, { params }: { params: { appName: string } }) : Promise<NextResponse> {
    const { appName } = await params;
    const user = await getAuthenticatedUser(req);
    if (!user) {
        return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
    }
    const userId = HashEmail(user.email);
    const sessionId = `${userId}-${appName}`
    try {
        const resp = await DefaultService.getSessionAppsAppNameUsersUserIdSessionsSessionIdGet(appName, userId, sessionId);
        return NextResponse.json(resp, {status: 200});
    } catch (e) {
        console.warn(`Creating new session: ${e}`)
        const resp = await DefaultService.createSessionWithIdAppsAppNameUsersUserIdSessionsSessionIdPost(appName, userId, sessionId)
        return NextResponse.json(resp, {status: 200});
    }
}
