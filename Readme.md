Installing prequesites
--------------------------
1/ execute the install.sh with sudo permissions by the way set mysql password.
                                                               
2/ create a database named 'coding' in mysql.
                            

Running the service


1/ cd coding-api

2/ python mysql.py

3/ python app.py

 open an another terminal

1/ cd coding-api

2/ bash run.sh

##Testing the service


1/ create an account with an username and password(username=dilip,password=rebeldilip123)

curl -i -H "Content-Type: application/json" -X POST -d '{"username":"dilip","password":"rebeldilip123"}' http://localhost:5000/todo/api/v1.0/create_account

in my laptop i have already dilip username

HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 64
Server: Werkzeug/0.11.9 Python/2.7.11+
Date: Thu, 12 May 2016 20:42:38 GMT

{
  "task": {
    "message": "choose a different username"
  }
}


2/ post request for snapshots (urls must be given with ';' as a delimiter)

curl -u dilip:rebeldilip123 -i -H "Content-Type: application/json" -X POST -d '{"urls":"https://www.youtube.com/watch?v=Kk-rEmZvBQI;https://www.youtube.com/watch?v=Kk-rEmZvBQI"}' http://localhost:5000/todo/api/v1.0/tasks                                                  ---

HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 196
Server: Werkzeug/0.11.9 Python/2.7.11+
Date: Thu, 12 May 2016 20:46:22 GMT

{
  "task": {
    "id": "7e69892d-0d8e-4426-86a5-f99e690bb08d",
    "urls": "https://www.youtube.com/watch?v=Kk-rEmZvBQI;https://www.youtube.com/watch?v=Kk-rEmZvBQI",
    "username": "dilip"
  }
}


3/ getting info about snapshot requests(Note here status=0 means completed and status=1 means running)

curl -u dilip:rebeldilip123 -i http://localhost:5000/todo/api/v1.0/tasks 
        -------------------
Note here that status=0 means completed and status=1 means running

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 2421
Server: Werkzeug/0.11.9 Python/2.7.11+
Date: Thu, 12 May 2016 20:35:29 GMT

{
  "tasks": [
    {
      "username": "dilip"
    },
    {
      "id": "b56e6c9f-c86b-4644-a16f-a1b864bb0266",
      "status": "0",
      "urls": "http://167.114.85.145/MAAS"
    },
    {
      "id": "53995278-27e4-4591-a648-ab7d6ce24a0f",
      "status": "0",
      "urls": "http://webscraping.com"
    },
    {
      "id": "69130c70-a5cd-4c99-a3ec-195c437d0ba6",
      "status": "0",
      "urls": "http://webscraping.com"
    }
  ]
}



4/for each and every request it requires authentication

curl -i http://localhost:5000/todo/api/v1.0/tasks

HTTP/1.0 401 UNAUTHORIZED
Content-Type: application/json
Content-Length: 36
WWW-Authenticate: Basic realm="Authentication Required"
Server: Werkzeug/0.11.9 Python/2.7.11+
Date: Thu, 12 May 2016 20:37:25 GMT

{
  "error": "Unauthorized access"
}



5/ downloading the snapshots (give id as an parameter as shown below) open it in a browser

http://localhost:5000/todo/api/v1.0/tasks/69130c70-a5cd-4c99-a3ec-195c437d0ba6
                                          ------------------------------------
                                                        id

