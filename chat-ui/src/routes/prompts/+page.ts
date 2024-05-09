import type { PageLoad } from './$types';
import type { ComplexPrompt } from '$lib/prompt';

export const load: PageLoad = async ({
	fetch
}): Promise<{
	error: string | undefined;
	success: boolean;
	prompts: ComplexPrompt[] | undefined;
}> => {
	console.log('In load');
	let response = await fetch('/api/prompts');
	let result = await response.json();
	console.log(result);
	return result;
};
