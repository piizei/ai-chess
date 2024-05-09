import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

const FRAGMENTS_BACKEND_URL =
	process.env.FRAGMENTS_BACKEND_URL || 'http://127.0.0.1:8080/prompts/fragments';

export const GET: RequestHandler = async ({ fetch }) => {
	console.log('In GET');
	try {
		let response = await fetch(FRAGMENTS_BACKEND_URL, {
			headers: {
				'Content-Type': 'application/json'
			}
		});
		let fragments = await response.json();
		console.log(fragments); // log the response to the console
		return json({ fragments, success: true });
	} catch (error) {
		console.error(error);
		return json({
			success: false,
			error: JSON.stringify(error, Object.getOwnPropertyNames(error))
		});
	}
};
