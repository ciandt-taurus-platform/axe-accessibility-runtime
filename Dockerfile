FROM node:14

WORKDIR /usr/src/app

# RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
# RUN echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
# RUN apt-get -y update && apt-get -y install google-chrome-stable

COPY package*.json ./
COPY . .
# RUN npm config set unsafe-perm true
# RUN npm install chromedriver@93 -g
# RUN npm install @axe-core/cli@4.2.2-alpha.14 -g

RUN npm install

EXPOSE 3000
CMD [ "axe", "$HOST_LIST", "--rules color-contrast,html-has-lang","--save output.json" ]


#axe --show-errors --verbose --chrome-options="no-sandbox" --chromedriver-path=/usr/src/app/chromedriver https://www.uol.com.br