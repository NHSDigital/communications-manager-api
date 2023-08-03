FROM node:12

USER node

COPY . /sandbox

WORKDIR /sandbox

RUN npm install

EXPOSE 9000

CMD ["npm", "start"]
