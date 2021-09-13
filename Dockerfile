FROM node:14

WORKDIR /usr/src/app

COPY package*.json ./
COPY . .
RUN npm install

EXPOSE 3000
CMD [ "axe", "$HOST_LIST", "--rules color-contrast,html-has-lang","--save output.json" ]