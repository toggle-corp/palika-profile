FROM node:10.15-alpine

MAINTAINER togglecorp info@togglecorp.com

RUN apk update && apk add git

WORKDIR /code

COPY ./package.json /code/package.json
RUN yarn install --network-concurrency 1

COPY . /code/
