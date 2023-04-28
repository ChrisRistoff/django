{**
server is the name of the container that will be created
nginx is the image that will be used to create the container
**}

server {

	{* the port that the server is going to listen on *}
	{* $(LISTEN_PORT) will set it as an environment variable *}

	listen $(LISTEN_PORT);
	
	{**
	any url that starts with /static will be served from the static directory
	the static directory is mapped to the vol/static directory
	this is where we will store our static files
	**}

	location /static/ {
		alias vol/static/;
		}
	
	{**
	location / is the root of the website (i.e. http://localhost:8000/)

	the uwsgi_pass directive will pass the request to the uwsgi server

	include /etc/nginx/uwsgi_params will pass the necessary uwsgi parameters

	client_max_body_size 10M will allow files up to 10MB to be uploaded
	**}
	
	location / {
		uwsgi_pass 	$(APP_HOST):$(APP_PORT);
		include 	/etc/nginx/uwsgi_params;
		client_max_body_size 10M;
		}
}
