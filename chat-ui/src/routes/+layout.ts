import type { LayoutLoad } from './$types';

export const load: LayoutLoad = ({ url }: { url: URL }): { currentRoute: string } => {
	const currentRoute: string = url.pathname;

	return {
		currentRoute
	};
};