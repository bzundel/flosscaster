# flosscaster backend

## Running instructions

### Docker (outdated)
In the root of the `backend` directory a `Dockerfile` can be found, which enables a user to run the backend using docker. To do so, build the container using `docker build -t flosscaster-backend` (or any other tag of your choosing) and run the container with `docker run -p 5000:5000 -v $(pwd)/data:/data flosscaster-backend`. The run command exposes the container's port 5000 to your machines port 5000 and creates a volume to persistently store the SQLite database (this can be pointed to any directory of your choosing by changing `$(pwd)/data`).

### Manually
To run the backend manually, simply install all necessary dependencies with `pip install -r requirements.txt` and run the API with `python main.py`. Setting of the environemnt variables `DATABASE_FILE`,`UPLOAD_PATH`, `RSS_FILE` and `FRONTEND_URL` is also required. For development purposes the following `.env` file can be used:

```.env
export DATABASE_FILE=./data/flosscaster.db
export UPLOAD_PATH=./uploads
export RSS_FILE=./data/feed.xml
export FRONTEND_URL="localhost:3000"
```
