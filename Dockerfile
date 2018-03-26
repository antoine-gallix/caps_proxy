# based on ubuntu
FROM ubuntu

# install python 3
RUN apt-get update && \
	apt-get -y install \
	python3 \
	python3-pip

# copy app code
WORKDIR /usr/src/app
COPY . .

# install requirements
RUN pip3 install -r requirements.txt

# configure locale to use utf8 encoding. required for click module.
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# expose port from the container to the external world
# port 5000 is default port for flask applications
EXPOSE 5000

# run the application
CMD ["invoke", "run", "prod"]
