FROM python:3.11 as build
WORKDIR /app
RUN git clone https://github.com/go-skynet/LocalAI
WORKDIR /app/LocalAI
RUN apt-get update && apt-get install -y golang cmake
RUN make build
FROM python:3.11 as deploy
COPY --from=build /app/LocalAI/local-ai /app/LocalAI/local-ai
WORKDIR /app/LocalAI
EXPOSE 8080
CMD ./local-ai