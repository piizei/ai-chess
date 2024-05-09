
import type { LayoutServerLoad } from './$types';

export const load = (({ request }) => {
	const { headers } = request;
	const username = headers.get('x-ms-client-principal-name') || 'Unknown';
	return {
		username,
	};
}) satisfies LayoutServerLoad;