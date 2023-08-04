FROM node:12

COPY . /sandbox

WORKDIR /sandbox

RUN npm install --ignore-scripts

USER node

EXPOSE 9000

CMD ["npm", "start"]
