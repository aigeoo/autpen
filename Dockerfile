FROM python:3.9

RUN apt-get update \
    && apt-get install -y wget git \
    && wget -q https://golang.org/dl/go1.19.9.linux-amd64.tar.gz \
    && tar -C /usr/local -xzf go1.19.9.linux-amd64.tar.gz \
    && rm go1.19.9.linux-amd64.tar.gz

ENV PATH="/usr/local/go/bin:${PATH}"

WORKDIR /code

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# This keeps Python from buffering stdin/stdout
#ENV PYTHONUNBUFFERED 1

COPY . /code

# RUN go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# RUN go install github.com/tomnomnom/assetfinder@latest

# RUN cd /code/vendor/ && git clone https://github.com/guelfoweb/knock.git && cd knock && python setup.py install

# RUN cd /code/vendor/ && git clone https://github.com/aboul3la/Sublist3r.git && cd Sublist3r && pip install -r requirements.txt

# RUN cd /code/vendor/ && git clone https://github.com/blechschmidt/massdns.git && cd massdns && make && cp bin massdns /usr/bin/

# RUN go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# RUN  cd /code/src/ && uvicorn main:app --host 127.0.0.1 --port 8000

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"]