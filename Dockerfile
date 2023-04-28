#this is the base image we are using to build our image on top of it
FROM python:3.9-alpine3.13

#this is the maintainer of the image (optional)
#maintainer of the image is the person who created the image and is responsible for it
#it is not the person who is running the image in the container
#(optional) it is good practice to add it
LABEL maintainer="krasenhristov"

#tells python to run in unbuffered mode
#which means that the python output is sent directly to the terminal
#allows us to see the output of our application in real time
#this is not recommended for production environment
ENV PYTHONUNBUFFERED 1


#tell docker to copy the requirements.dev.txt to the tmp folder
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./scripts /scripts
#this is the app folder
COPY ./app /app
#tell docker where to run the commands
WORKDIR /app
#tell docker which ports to expose
EXPOSE 8000

#ARG is used to pass arguments to the docker build command
#DEV=false is the default value
ARG DEV=false



#RUN is used to run commands in the container during the build process
#&& is used to chain commands together
RUN python -m venv /py && \
    
    #upgrade pip
    /py/bin/pip install --upgrade pip && \

    #install postgresql client
    apk add --update --no-cache postgresql-client jpeg-dev && \

    #install build-base postgresql-dev musl-dev
    apk add --update --no-cache --virtual .tmp-build-deps \
    
    #build-base = gcc, g++, make
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    
    #install requirements
    /py/bin/pip install -r /tmp/requirements.txt && \
    
    #if dev env is true install dev requirements
    if [ "$DEV" = "true" ] ; then \
		/py/bin/pip install -r /tmp/requirements.dev.txt ; \
	fi && \

    #remove tmp to keep it clean and lightweight
    rm -rf /tmp && \

    #remove build-base postgresql-dev musl-dev
    apk del .tmp-build-deps && \
    
    #create user
    adduser\
    	
	# -D = --disabled-password\
    	--disabled-password\

	# -H = --no-create-home\
	--no-create-home\
	
	#django-user = username can be anything we want even a variable
	django-user && \

    #create media folder and static folder
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \

    #change the owner of the media folder and static folder to django-user
    chown -R django-user:django-user /vol && \

    #change the permissions of the media folder and static folder to 755
    # 755 = read, write, execute
    chmod -R 755 /vol && \

    # make scripts executable
    chmod -R +x /scripts


# specify the PATH to the virtual environment
ENV PATH="/scripts:/py/bin:$PATH"

# specify the user to run as
#container will run as the last user specified
USER django-user 

# CMD is used to specify the default command to run when the container starts
CMD ["run.sh"]
