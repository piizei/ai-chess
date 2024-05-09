
import type { PageServerLoad } from './$types';

export const load = (({ cookies, request }) => {
	const { headers:headerObj } = request;
	// convert headers to a plain object
	const headers: Record<string, string>[] = [];
	for (const [key, value] of headerObj.entries()) {
		headers.push({key, value});
	}
    const allCookies = cookies.getAll();

	return {
		headers,
        cookies: allCookies
	};
}) satisfies PageServerLoad;