import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

const BACKEND_URL = process.env.GAME_SERVICE_URL || 'http://127.0.0.1:8000';
export const GET: RequestHandler = async () => {
    try {
        const response = await fetch(BACKEND_URL + '/status', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        console.log(response.status); // log the response code
        if (response.status > 299) {
            return json({ error: { status: response.status, body: await response.text() } });
        }
        const answer = await response.json();
        console.log(answer); // log the response to the console

        return json({ ...answer });
    } catch (error) {
        console.error(error);
        return json({ error });
    }
};
