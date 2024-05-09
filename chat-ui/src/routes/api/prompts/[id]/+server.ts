import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

const PROMPTS_BACKEND_URL = process.env.PROMPTS_BACKEND_URL || 'http://127.0.0.1:8080/prompts';
const handleRequest: (
	method: string,
	{ fetch, params }: { fetch: any; params: any }
) => Promise<any> = async (method, { fetch, params }) => {
	console.log(`In ${method}`);
	let url_with_id = PROMPTS_BACKEND_URL + '/' + params.id;
	try {
		let response = await fetch(url_with_id, {
			method: method,
			headers: {
				'Content-Type': 'application/json'
			}
		});
		let result = await response.json();
		console.log(result); // log the response to the console
		return json(result);
	} catch (error) {
		console.error(error);
		return json({
			success: false,
			error: JSON.stringify(error, Object.getOwnPropertyNames(error))
		});
	}
};

export const DELETE: RequestHandler = async (context) => handleRequest('DELETE', context);
export const GET: RequestHandler = async (context) => handleRequest('GET', context);
