FROM mcr.microsoft.com/mirror/docker/library/node:18-alpine
ENV CHAT_BACKEND_URL=http://localhost:8080/chat

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .

RUN npm run build

EXPOSE 3000
CMD ["node", "server.js"]
