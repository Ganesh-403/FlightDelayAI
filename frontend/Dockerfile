# Stage 1: Build the React application
FROM node:20-alpine as build-stage

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Serve the application with Nginx
FROM nginx:stable-alpine as production-stage

# Copy the build output to Nginx's html directory
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copy a custom Nginx config if needed, otherwise default is fine
# EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
