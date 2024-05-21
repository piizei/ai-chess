import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';


const BACKEND_URL = process.env.GAME_SERVICE_URL || 'http://127.0.0.1:8000';


const handleRequest: (
    method: string,
    {fetch, params}: {fetch: any; params: any}
) => Promise<any> = async (method, {fetch, params}) => {
    try {
        const response = await fetch(BACKEND_URL + '/static/' + params.id, {
            method: method
        });
        return response;
    } catch (error) {
        console.error(error);
        return json({ error });
    }
};

export const GET: RequestHandler = async (context) => handleRequest('GET', context);
