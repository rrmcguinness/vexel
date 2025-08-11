// File: app/api/auth/login/route.ts
import { NextResponse } from 'next/server';
import { OAuth2Client } from 'google-auth-library';

const OAUTH_CLIENT_ID = process.env.OAUTH_CLIENT_ID;
const OAUTH_CLIENT_SECRET = process.env.OAUTH_CLIENT_SECRET;
const REDIRECT_URI = process.env.REDIRECT_URI;

/**
 * This endpoint initiates the Google OAuth 2.0 login flow.
 * It generates the authorization URL and redirects the user to Google's sign-in page.
 */
export async function GET() {
    if (!OAUTH_CLIENT_ID || !OAUTH_CLIENT_SECRET || !REDIRECT_URI) {
        console.error("OAuth environment variables are not configured.");
        return new NextResponse('Server configuration error.', { status: 500 });
    }

    const oAuth2Client = new OAuth2Client(
        OAUTH_CLIENT_ID,
        OAUTH_CLIENT_SECRET,
        REDIRECT_URI
    );

    // Generate the URL that will be used for the consent dialog.
    const authorizeUrl = oAuth2Client.generateAuthUrl({
        access_type: 'offline', // 'offline' requests a refresh token
        scope: [
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile',
            'openid',
            'https://www.googleapis.com/auth/cloud-platform.read-only',
            'https://www.googleapis.com/auth/gmail.send',
            'https://www.googleapis.com/auth/gmail.readonly',
            'https://www.googleapis.com/auth/bigquery',
            'https://www.googleapis.com/auth/gmail.compose',
            'https://www.googleapis.com/auth/calendar.events'

        ],
        prompt: 'consent' // Forces the consent screen to be shown, ensuring a refresh token is issued.
    });

    // Redirect the user to the generated Google sign-in page.
    return NextResponse.redirect(authorizeUrl);
}
