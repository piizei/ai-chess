FROM node:20-alpine

WORKDIR /app
RUN --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=package-lock.json,target=package-lock.json \
    --mount=type=cache,target=/root/.npm \
    npm ci \
USER node
COPY . .

RUN npm run build

EXPOSE 3000
CMD ["node", "server.js"]
