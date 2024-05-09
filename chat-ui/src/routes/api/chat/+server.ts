import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import crypto from 'crypto';

const CHAT_BACKEND_URL = process.env.CHAT_BACKEND_URL || 'http://127.0.0.1:8080/chat';
export const POST: RequestHandler = async ({ request }) => {
	const body = await request.json();
	const { message: prompt } = body;
	// GET user from x-ms-client-principal-name header ir just use the string 'user'
	const user = request.headers.get('x-ms-client-principal-name') || 'user';
	// make the session to be a md5 has over the value of the cookie header or call it session
	const sessionRaw = request.headers.get('cookie') || 'session';
	const session = crypto.createHash('md5').update(sessionRaw).digest('hex');
	const data = {
		prompt,
		user,
		session
	};
	console.log(data);
	console.log(CHAT_BACKEND_URL);
	try {
		const response = await fetch(CHAT_BACKEND_URL, {
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
