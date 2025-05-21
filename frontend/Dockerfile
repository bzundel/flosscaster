FROM node:23

WORKDIR /app

COPY package*.json /app/
RUN npm install
RUN npm install -g serve

COPY . .

RUN npm run build

CMD ["serve", "-s", "build", "-l", "3000"]
