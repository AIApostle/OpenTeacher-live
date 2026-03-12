FROM python:3.13-slim-bookworm

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.6.6 /uv /uvx /bin/

#Set the WORKDIR 
WORKDIR /backend

#Copying your files into the WORKDIR
ADD . .

#  Installing dependencies
RUN uv sync --locked

#Exposing the port
EXPOSE 8000

#  Correct the path to main.py
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]