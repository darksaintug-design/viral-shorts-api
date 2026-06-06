# Build static assets and serve with nginx
FROM node:18-alpine AS build
WORKDIR /app
COPY package.json package-lock.json* ./
COPY . .
RUN npm install --silent
RUN npm run build

FROM nginx:stable-alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
