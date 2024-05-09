import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

const CHAT_BACKEND_URL = process.env.CHAT_BACKEND_URL || 'http://127.0.0.1:8080/chat';
export const POST: RequestHandler = async ({ request }) => {
    const body = await request.json();
    const { message: prompt } = body;
    const data = {
        query: prompt
    };
    console.log(data);
    try {
        const response = await fetch(`${CHAT_BACKEND_URL}/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        console.log(response.status); // log the response code
        if (response.status > 299) {
            return json({ error: { status: response.status, body: await response.text() } });
        }
        const searchResults: {'sources': [{'id': string, 'title': string, 'location': string, 'caption': string }]} = await response.json();
        console.log(searchResults); // log the response to the console
        // @ts-ignore
        if (searchResults.sources.length!= 0) {
            const formattedResults = searchResults.sources.map(result => {
                return `<sup><a href="${result.location}">${result.title}</a></sup> -  <i>${result.caption}</i><br>`
            }).join('');
            return json({answer: "Ich habe die folgenden Suchergebnisse gefundens:<br>" + formattedResults});
        } else {
            return json({});
        }
    } catch (error) {
        console.error(error);
        return json({ error });
    }
};
