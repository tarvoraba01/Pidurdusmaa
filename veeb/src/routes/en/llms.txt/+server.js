/* /en/llms.txt — vt $lib/server/llms.js. EN/RU: /en/llms.txt, /ru/llms.txt */
import { llmsTekst } from '$lib/server/llms.js';

export const prerender = true;

export function GET() {
	return new Response(llmsTekst('en'), {
		headers: { 'Content-Type': 'text/plain; charset=utf-8', 'Cache-Control': 'public, max-age=3600' }
	});
}
