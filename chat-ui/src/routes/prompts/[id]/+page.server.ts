import type { Actions } from './$types';
import { formDataToJson } from '$lib/form';
import { redirect } from '@sveltejs/kit';
const PROMPTS_BACKEND_URL = process.env.PROMPTS_BACKEND_URL || 'http://127.0.0.1:8080/prompts';
export const actions = {
	delete: async ({ fetch, params }) => {
		let url_with_id = PROMPTS_BACKEND_URL + '/' + params.id;
		try {
			let response = await fetch(url_with_id, {
				method: 'DELETE',
				headers: {
					'Content-Type': 'application/json'
				}
			});
			let result = await response.json();
			console.log(result); // log the response to the console
		} catch (error) {
			console.error(error);
			return { success: false, error: JSON.stringify(error, Object.getOwnPropertyNames(error)) };
		}
		throw redirect(302, '/prompts');
	},
	save: async ({ fetch, request }) => {
		let prompt = formDataToJson(await request.formData());
		let result;
		try {
			let response = await fetch(PROMPTS_BACKEND_URL, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(prompt)
			});
			if (response.status > 299) {
				console.log('Error: ' + response.status);
				let message = await response.text();
				return { success: false, error: `Error (${response.status}): ${message}` };
			}
			let responseJson = await response.json();

			result = { success: true, prompt: responseJson };
		} catch (error) {
			console.error(error);
			result = { success: false, error: JSON.stringify(error, Object.getOwnPropertyNames(error)) };
		}
		if (result.success) {
			throw redirect(302, '/prompts/' + result.prompt.id);
		}
		return result;
	}
	// delete: async ({ fetch, params }) => {}
} satisfies Actions;
