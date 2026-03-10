# to initate requirements file enter the following in the CMD
#pip freeze > requirements.txt

#install a version
From python:3.11-slim
#define working directory
WORKDIR /app
#copy requirements files
COPY requirements.txt .
#install requirements
RUN pip install --no-cache-dir -r requirements.txt
#copy rest file
COPY . .
#define port
EXPOSE 8000
#start the server
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]

#now create the docker
#on cmd write the following code
# docker build -t my-fastapi-app .