# Pidurdusmaa.ee — SvelteKit (adapter-node).
#
# Lehed renderdatakse ehituse ajal ära (5948 aadressi) ja server annab
# need valmiskujul välja. Andmebaasi ega API võtmeid ei ole.
#
# ulimit: 6000 lehe kirjutamine avab korraga palju faile. Kui ehitus
# kukub veaga "EMFILE: too many open files", ehita nii:
#   docker build --ulimit nofile=65535 -t pidurdusmaa .

FROM node:22-alpine AS build
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci --no-audit --no-fund || npm install --no-audit --no-fund
COPY . .
RUN npm run build && npm prune --omit=dev

FROM node:22-alpine
WORKDIR /app
ENV NODE_ENV=production
ENV PORT=3000
ENV BODY_SIZE_LIMIT=1M
# Kontaktikirjad ja kasutuslogi kirjutatakse siia. Coolify's tee sellest
# volume, muidu kaob sisu iga uue versiooniga.
ENV LOG_DIR=/app/data
VOLUME /app/data
COPY --from=build /app/build ./build
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/package.json ./
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s \
  CMD wget -qO- http://127.0.0.1:3000/ >/dev/null || exit 1
CMD ["node", "build"]
