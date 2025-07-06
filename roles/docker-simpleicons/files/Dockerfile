FROM node:latest AS builder

WORKDIR /app
COPY package*.json ./

RUN npm install

FROM node:latest

WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY server.js .

EXPOSE 3000

CMD ["node", "server.js"]
