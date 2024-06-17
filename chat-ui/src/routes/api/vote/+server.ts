import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import crypto from 'crypto';

const BACKEND_URL = process.env.GAME_SERVICE_URL || 'http://127.0.0.1:8000';
export const POST: RequestHandler = async ({ request }) => {
	const body = await request.json();
	const { message: prompt } = body;
	const sessionRaw = request.headers.get('cookie') || 'session';
	const session = crypto.createHash('md5').update(sessionRaw).digest('hex');
	const data = {
		user: session,
		message: prompt
	};
	try {
		const response = await fetch(BACKEND_URL + '/vote', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
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
