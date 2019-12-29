FROM debian:latest

ARG work_dir=/tmp/textapi/

RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR ${work_dir}
COPY requirements.txt ${work_dir}

RUN pip3 install "https://github.com/megagonlabs/ginza/releases/download/latest/ginza-latest.tar.gz" && \
    pip3 install "git+https://github.com/boudinfl/pke.git" && \
    python3 -m nltk.downloader stopwords && \
    pip3 install -r requirements.txt

COPY api.py ${work_dir}
COPY secrets.json ${work_dir}
COPY translator ${work_dir}/translator

EXPOSE 8080
ENV FLASK_APP ./api.py
ENV GOOGLE_APPLICATION_CREDENTIALS secrets.json

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]