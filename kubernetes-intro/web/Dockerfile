FROM caddy:2.6.4-alpine

USER 1001:1001

WORKDIR "/app" 

ARG SERVER_PORT=8000
ENV PORT=${SERVER_PORT}

EXPOSE ${PORT}


CMD [ "sh", "-c", "caddy file-server --listen :${PORT} --root /app" ]

