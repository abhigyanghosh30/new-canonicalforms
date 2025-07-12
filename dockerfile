FROM node:22 AS css_build
# Set the working directory
WORKDIR /srv
# Install Node.js dependencies
ADD . .
# Install the necessary packages
RUN yarn install 
# Copy the source files
ADD static static
RUN yarn build-css



FROM ubuntu:noble
# Install dependencies
RUN apt-get update && apt-get install --no-install-recommends --yes \
  python3 python3-pip python3-venv ca-certificates
# Copy the requirements file and install Python dependencies


WORKDIR /srv

RUN python3 -m venv /venv
ENV PATH="/venv/bin:${PATH}"

ADD requirements.txt .
RUN pip3 config set global.disable-pip-version-check true
RUN python3 -m venv /venv
ENV PATH="/venv/bin:${PATH}"
RUN --mount=type=cache,target=/root/.cache/pip pip3 install -r requirements.txt

ADD . .
# Copy the compiles CSS
COPY --from=css_build /srv/dist dist
