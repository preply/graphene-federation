FROM node:10.16.2-alpine

WORKDIR /project
COPY package.json package-lock.json ./
COPY ./src/ ./src/
ENV NPM_CONFIG_LOGLEVEL warn

RUN npm config set unsafe-perm true && npm ci
RUN apk add curl

EXPOSE 3003
CMD [ "npm", "start"]