import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import type { ComplexPrompt, PromptFragment } from '$lib/prompt';
import { isComplexPrompt } from '$lib/prompt';

export const load: PageLoad = async ({
	fetch,
	params
}): Promise<{ prompt: ComplexPrompt; fragments: PromptFragment[] }> => {
	console.log('In load');
	let isNew = params.id === 'new';
	let fragmentsResponse = await fetch('/api/fragments');
	let fragmentsJson = await fragmentsResponse.json();
	if ('fragments'! in fragmentsJson && !Array.isArray(fragmentsJson.fragments)) {
		throw error(500, 'Invalid fragments ' + JSON.stringify(fragmentsJson));
	}
	let fragments = fragmentsJson.fragments as PromptFragment[];
	if (isNew) {
		return { prompt: {}, fragments } as { prompt: ComplexPrompt; fragments: PromptFragment[] };
	}
	let response = await fetch('/api/prompts/' + params.id);

	let prompt = await response.json();
	if (prompt.length === 0) {
		console.log('Prompt not found');
		throw error(404, 'Prompt not found');
	}
	if (Array.isArray(prompt) && prompt.every(isComplexPrompt)) {
		return { prompt: prompt[0], fragments };
	} else {
		throw error(500, 'Invalid prompt ' + JSON.stringify(prompt));
	}
};
