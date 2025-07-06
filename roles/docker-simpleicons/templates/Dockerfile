# ---- Builder Stage ----
FROM node:latest AS builder

WORKDIR /app
# Nur package.json und package-lock.json kopieren für schnellere Caching-Layers
COPY package*.json ./

# simple-icons installieren
RUN npm install

# ---- Runtime Stage ----
FROM node:latest

WORKDIR /app
# Nur node_modules aus dem Builder übernehmen
COPY --from=builder /app/node_modules ./node_modules
# Kopiere den Server-Code
COPY server.js .

# Port, auf dem der Server lauscht
ENV PORT=3000
EXPOSE 3000

# Startbefehl
CMD ["node", "server.js"]
