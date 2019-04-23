# Ubuntu Linux as the base imag
FROM ubuntu:16.04

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

WORKDIR /app

ADD requirements.txt /app

# Install packages 
RUN apt-get -y update && \
    apt-get -y upgrade && \
	apt-get -y install ant python3-pip python3-dev openjdk-8-jdk && \
	pip3 install -r requirements.txt && \
        python3 -m spacy download en_core_web_lg && \
        python3 -m spacy download en && \
        python3 -c "import nltk; nltk.download(\"wordnet\"); nltk.download(\"punkt\")"

WORKDIR /app
ADD . /app

CMD ["chmod", "777", "ask"]
CMD ["chmod", "777", "answer"]
ENTRYPOINT ["/bin/bash", "-c"]
