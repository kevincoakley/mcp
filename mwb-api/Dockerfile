FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install mcp requests

# Copy server
COPY server.py .

# Expose port
EXPOSE 8080

# Set environment
ENV MCP_HOST=0.0.0.0
ENV MCP_PORT=8080
ENV MCP_TRANSPORT=streamable-http

# Run server
CMD ["python", "server.py"]