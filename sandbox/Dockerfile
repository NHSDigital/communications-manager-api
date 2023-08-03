FROM node:12

COPY . /sandbox

WORKDIR /sandbox

RUN npm install

USER node

EXPOSE 9000

CMD ["npm", "start"]
