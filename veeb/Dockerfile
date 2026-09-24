# Pidurdusmaa.ee — staatiline sait.
#
# Ehitus: SvelteKit kirjutab iga aadressi päris HTML-failiks (5948 lehte),
# sealhulgas sitemap.xml. Käitamisel PHP-d, andmebaasi ega võtmeid ei ole —
# nginx serveerib valmis faile. Ükski keskkonnamuutuja ei ole kohustuslik.

FROM node:22-alpine AS build
WORKDIR /app
# ulimit: 6000 lehe kirjutamine avab korraga palju faile
COPY package.json package-lock.json* ./
RUN npm ci --no-audit --no-fund || npm install --no-audit --no-fund
COPY . .
RUN npm run build

FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://127.0.0.1/ >/dev/null || exit 1
