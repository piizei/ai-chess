FROM python:3.11-bookworm

# set work directory
WORKDIR /usr/src/app
ENV PORT=80
# install dependencies
COPY pyproject.toml README.md ./
RUN pip install poetry && \
    poetry config virtualenvs.create false
COPY rag_service/ rag_service/
RUN poetry install
WORKDIR /usr/src/app

EXPOSE 80
ENTRYPOINT ["python", "rag_service/main.py"]
