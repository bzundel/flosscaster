# flosscaster frontend

## Running instructions

### Docker
To run the frontend as a docker container, build it with `docker build -t flosscaster-frontend` or another appropriate tag and run with `docker run -it -p 3000:3000 flosscaster-frontend`. The flag `-it` makes sure that `CTRL-C` responds properly to stop the container and the flag `-p 3000:3000` exposes the container's port 3000 to your machines port 3000.

### Manually
To run the frontend manually, install necessary dependencies with `npm install` and run with `npm start`.
