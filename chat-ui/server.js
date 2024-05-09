import { handler } from './build/handler.js';
import express from 'express';
import { useAzureMonitor } from '@azure/monitor-opentelemetry';
import dotenv from 'dotenv';
dotenv.config();

if (process.env.APPLICATIONINSIGHTS_CONNECTION_STRING) {
	useAzureMonitor()
}
const app = express();

// add a route that lives separately from the SvelteKit app
app.get('/healthz', (req, res) => {
	res.end('ok');
});

app.use(handler);

app.listen(3000, () => {
	console.log('listening on port 3000');
});