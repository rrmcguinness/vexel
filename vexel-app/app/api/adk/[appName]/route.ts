import { NextRequest, NextResponse } from 'next/server';
import { getAuthenticatedUser } from '@/lib/auth';
import { AgentRunRequest, OpenAPI, Content_Input, DefaultService, Part_Output } from '@/lib/adk-client'
import { HashEmail } from "@/lib/model";
import {Content_Output} from "../../../../lib/adk-client";

const ADK_API_BASE_URL = process.env.ADK_API_BASE_URL || 'http://127.0.0.1:8000';
OpenAPI.BASE = ADK_API_BASE_URL;

export async function POST(req: NextRequest, { params }: { params: { appName: string } })  {


    const { appName } = await params;


    const user = await getAuthenticatedUser(req);
    if (!user) {
        return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
    }

    const userId = HashEmail(user.email);

    const { history, sessionId }: { history: any[], sessionId: string } = await req.json();

    if (!history || history.length === 0) {
        return NextResponse.json({ message: 'Chat history is required.' }, { status: 400 });
    }
    if (!sessionId) {
        return NextResponse.json({ message: 'Session ID is required.' }, { status: 400 });
    }

    const lastMessage = history[history.length - 1];

    const newMessage: Content_Input = {
        parts: [{ text: lastMessage.content }]
    };

    const agentRunRequest: AgentRunRequest = {
        appName: appName,
        userId: userId,
        sessionId: sessionId,
        newMessage: newMessage,
        streaming: false,
    };

    const resp = await DefaultService.agentRunSseRunSsePost(agentRunRequest);
    console.log(resp)

    const obj = JSON.parse(resp.substring(5, resp.length - 1))
    console.log(obj.content.parts)
    return NextResponse.json(obj.content.parts, {status: 200});
}

export async function DELETE(req: NextRequest, { params }: { params: { appName: string } }) {
    const { appName } = await params
    try {
        const user = await getAuthenticatedUser(req);
        if (!user) {
            return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
        }
        const userId = user.email;
        const { searchParams } = new URL(req.url);
        const sessionId = searchParams.get('sessionId');

        if (!sessionId) {
            return NextResponse.json({ message: 'Session ID is required.' }, { status: 400 });
        }

        await DefaultService.deleteSessionAppsAppNameUsersUserIdSessionsSessionIdDelete(appName, userId, sessionId);

        return NextResponse.json({ message: 'Session deleted successfully' }, { status: 200 });
    } catch (error: any) {
        console.error(`${params.appName} Agent API Error (DELETE):`, error);
        const errorMessage = error.response?.data?.detail || 'An error occurred while deleting the session.';
        return NextResponse.json({ message: errorMessage }, { status: 500 });
    }
}