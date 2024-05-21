import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

const BACKEND_URL = process.env.GAME_SERVICE_URL || 'http://127.0.0.1:8000';
export const POST: RequestHandler = async ({ request }) => {
	const body = await request.json();
	const { message: prompt } = body;
	// GET user from x-ms-client-principal-name header ir just use the string 'user'
	const user = request.headers.get('x-ms-client-principal-name') || request.headers.get('x-client-anon-guid')  || 'user';
	const data = {
		user,
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
