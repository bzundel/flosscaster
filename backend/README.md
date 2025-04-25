# flosscaster backend

## Running instructions

### Docker
In the root of the `backend` directory a `Dockerfile` can be found, which enables a user to run the backend using docker. To do so, build the container using `docker build -t flosscaster-backend` (or any other tag of your choosing) and run the container with `docker run -p 5000:5000 -v $(pwd)/data:/data flosscaster-backend`. The run command exposes the container's port 5000 to your machines port 5000 and creates a volume to persistently store the SQLite database (this can be pointed to any directory of your choosing by changing `$(pwd)/data`).

### Manually
To run the backend manually, simply install all necessary dependencies with `pip install -r requirements.txt` and run the API with `DATA_DIR=path/to/data/directory python main.py`.

## To-Dos
- [x] Create endpoint for getting a specific podcast via id (also add id column to podcasts)
- [x] Create API documentation (with swagger? has good integration with flask)
- [x] Dockerize backend in backend root
- [ ] Add proper logging
- [ ] Add docker-compose file to project root to run both frontend and backend
