
# Use an official node runtime as a parent image
FROM node:10.16.1

WORKDIR /app/frontend

# Install dependencies
COPY package.json package-lock.json /app/frontend/

RUN npm install

# Add rest of the client code
COPY . /app/frontend

