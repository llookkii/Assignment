# Use the official Nginx image
FROM nginx:alpine

# Set the working directory
WORKDIR /usr/share/nginx/html

# Remove the default NGINX static files
RUN rm -rf ./*

# Copy the frontend source code (HTML, CSS, JS)
COPY . .

# Expose the default Nginx port
EXPOSE 80
