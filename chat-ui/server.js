import { handler } from './build/handler.js';
import express from 'express';
import dotenv from 'dotenv';
import appInsights from 'applicationinsights';

dotenv.config();

const app = express();

if (process.env.APPLICATIONINSIGHTS_CONNECTION_STRING) {
	console.log("Using azure monitor");
	appInsights.setup(process.env.APPLICATIONINSIGHTS_CONNECTION_STRING)
		.setDistributedTracingMode(appInsights.DistributedTracingModes.AI_AND_W3C)
		.setAutoDependencyCorrelation(true)
		.setAutoCollectDependencies(true)
		.setAutoCollectConsole(true, true)
		.setAutoCollectExceptions(true)
		.setInternalLogging(true, true)
		.start()
	appInsights.defaultClient.context.tags[appInsights.defaultClient.context.keys.cloudRole] = "BFF";

}

// add a route that lives separately from the SvelteKit app
app.get('/healthz', (req, res) => {
	res.end('ok');
});

app.use((req, res, next) => {
	appInsights.defaultClient.trackRequest({ name: req.method + ' ' + req.url, url: req.url, time: new Date(), duration: 0, resultCode: res.statusCode + "", success: true });
	next();
});
app.use(handler);

app.listen(3000, () => {
	console.log('listening on port 3000');
});
