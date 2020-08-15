FROM python:slim
WORKDIR /root

COPY ./ ./

RUN pip3 install --no-cache-dir -r requirements.txt
RUN apt-get update -yy -q && apt-get install curl -qq
RUN curl -sSL https://sjtu-plus.github.io/bXWNVWzbX1/verify/ > templates/index.html

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000"]
