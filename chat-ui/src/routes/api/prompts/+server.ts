import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

const PROMPTS_BACKEND_URL = process.env.PROMPTS_BACKEND_URL || 'http://127.0.0.1:8080/prompts';

export const GET: RequestHandler = async ({ fetch }) => {
	console.log('In GET');
	try {
		let response = await fetch(PROMPTS_BACKEND_URL, {
			headers: {
				'Content-Type': 'application/json'
			}
		});
		let prompts = await response.json();
		console.log(prompts); // log the response to the console
		return json({ prompts, success: true });
	} catch (error) {
		console.error(error);
		return json({
			success: false,
			error: JSON.stringify(error, Object.getOwnPropertyNames(error))
		});
	}
};
