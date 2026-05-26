FROM node:20-bullseye-slim as build

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install --legacy-peer-deps

COPY . .
RUN echo "REACT_APP_API_URL=/api" > .env
RUN CI=false DISABLE_ESLINT_PLUGIN=true npm run build

# Production stage with Nginx
FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
