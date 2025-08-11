import { NextResponse } from 'next/server';
import { OAuth2Client } from 'google-auth-library';
import { cookies } from 'next/headers';
import { SignJWT } from 'jose';

const OAUTH_CLIENT_ID = process.env.OAUTH_CLIENT_ID;
const OAUTH_CLIENT_SECRET = process.env.OAUTH_CLIENT_SECRET;
const REDIRECT_URI = process.env.REDIRECT_URI;

const SESSION_COOKIE_NAME = 'auth_session_token';
const SESSION_COOKIE_OPTIONS = {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    path: '/',
    maxAge: 60 * 60 * 24, // 24 hours
    sameSite: 'lax' as const,
};

export async function GET(request: Request) {
    const url = new URL(request.url);
    const code = url.searchParams.get('code');
    const error = url.searchParams.get('error');

    const loginErrorRedirect = (errorMessage: string) => {
        const url = new URL('/login', request.url);
        url.searchParams.set('error', errorMessage);
        return NextResponse.redirect(url);
    };

    if (error) {
        return loginErrorRedirect(`OAuth Error: ${error}`);
    }

    if (!code) {
        return loginErrorRedirect('Authorization code was not provided.');
    }

    if (!OAUTH_CLIENT_ID || !OAUTH_CLIENT_SECRET || !REDIRECT_URI || !process.env.SESSION_SECRET) {
        console.error("OAuth environment variables are not configured on the server.");
        return loginErrorRedirect('Server configuration error.');
    }

    try {
        const oAuth2Client = new OAuth2Client(
            OAUTH_CLIENT_ID,
            OAUTH_CLIENT_SECRET,
            REDIRECT_URI
        );

        // Exchange the authorization code for an access token and ID token
        const { tokens } = await oAuth2Client.getToken(code);

        // The ID token is a JWT that contains user profile information.
        if (!tokens.id_token) {
            return loginErrorRedirect('Failed to retrieve ID token from Google.');
        }

        // Verify the ID token to ensure its integrity and get the user's profile.
        const loginTicket = await oAuth2Client.verifyIdToken({
            idToken: tokens.id_token,
            audience: OAUTH_CLIENT_ID
        });

        const payload = loginTicket.getPayload();
        if (!payload?.email) {
            return loginErrorRedirect('Could not verify user information from token.');
        }

        // The architectural error was using Google's id_token directly for our session.
        // The fix is to verify the external token, then create our own signed session
        // token. This gives us full control over session contents, expiration, and security,
        // while keeping the cookie small.
        const secret = new TextEncoder().encode(process.env.SESSION_SECRET);
        const sessionToken = await new SignJWT({
            email: payload.email,
            name: payload.name,
            picture: payload.picture,
            sub: payload.sub
        })
            .setProtectedHeader({ alg: 'HS256' })
            .setIssuedAt()
            .setExpirationTime('24h') // Align with cookie's maxAge
            .sign(secret);

        // Redirect to the home page after successful login
        const homeUrl = new URL('/', request.url);
        const response = NextResponse.redirect(homeUrl);

        // Set our own signed session token in a secure, httpOnly cookie.
        response.cookies.set(SESSION_COOKIE_NAME, sessionToken, SESSION_COOKIE_OPTIONS);

        return response;

    } catch (err) {
        console.error('Failed to exchange authorization code or verify token:', err);
        return loginErrorRedirect('Authentication failed. Please try again.');
    }
}
