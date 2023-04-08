FROM python:3.9-alpine3.13
LABEL maintainer="krasenhristov"

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY ./requirements.txt /tmp/requirements.txt
#linter etc
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    
    #upgrade pip
    /py/bin/pip install --upgrade pip && \
    
    #install requirements
    /py/bin/pip install -r /tmp/requirements.txt && \
    
    #if dev env is true install dev requirements
    if [ "$DEV" = "true" ] ; then \
		/py/bin/pip install -r /tmp/requirements.dev.txt ; \
	fi && \

    #remove tmp to keep it clean and lightweight (optional when not on chromebook)
    rm -rf /tmp && \
    
    #create user
    adduser\
    	
	# -D = --disabled-password\
    	--disabled-password\

	# -H = --no-create-home\
	--no-create-home\
	
	#django-user = username can be anything we want even a variable
	django-user

# specify the PATH to the virtual environment
ENV PATH="/py/bin:$PATH"

# specify the user to run as
#container will run as the last user specified
USER django-user 
