import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import crypto from 'crypto';

const CHAT_BACKEND_URL = process.env.CHAT_BACKEND_URL || 'http://127.0.0.1:8001/chat';
export const POST: RequestHandler = async ({ request }) => {
    const sessionRaw = request.headers.get('cookie') || 'session';
    const session = crypto.createHash('md5').update(sessionRaw).digest('hex');
    try {
        const response = await fetch(`${CHAT_BACKEND_URL}/session/${session}`, {
            method: 'DELETE',
        });
        console.log(response.status); // log the response code
        if (response.status > 299) {
            return json({ error: { status: response.status, body: await response.text() } });
        }
        const answer = await response.json();
        console.log(answer);
        return json({ answer });
    } catch (error) {
        console.error(error);
        return json({ error });
    }
};
