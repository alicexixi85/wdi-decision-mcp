FROM python:3.12-slim
LABEL io.modelcontextprotocol.server.name="io.github.alicexixi85/wdi-decision-mcp"
LABEL org.opencontainers.image.source="https://github.com/alicexixi85/wdi-decision-mcp"
WORKDIR /app
COPY server.py mcp_stdio.py ./
ENV PYTHONUNBUFFERED=1
CMD ["python", "server.py"]
