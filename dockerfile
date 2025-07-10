FROM node:22 AS css_build
# Set the working directory
WORKDIR /app
# Install Node.js dependencies
ADD package.json .
ADD yarn.lock .
# Install the necessary packages
RUN yarn install 
# Copy the source files
ADD static /app/static
RUN yarn build-css
# Build the CSS files again to ensure they are up-to-date
RUN yarn build-css


FROM ubuntu:jammy
# Install dependencies
RUN apt-get update && \
apt-get install -y python3 python3-pip
# Copy the requirements file and install Python dependencies


WORKDIR /app

ADD requirements.txt .
# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt
# Copy the application code

ADD . .
COPY --from=css_build /app/static/dist /app/static/dist 