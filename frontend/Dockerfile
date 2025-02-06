# Use Node.js as base image
FROM node:20

# Set the working directory
WORKDIR /app

# Copy package.json first (without package-lock.json)
COPY package.json ./

# Ensure a clean install of dependencies
RUN rm -rf node_modules package-lock.json && npm cache clean --force
RUN npm install --legacy-peer-deps

# Copy the rest of the app
COPY . .

# Expose the Vite development port
EXPOSE 5173

# Start Vite in development mode
CMD ["npm", "run", "dev"]
