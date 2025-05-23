# Backend Testing

### Prerequisites
Enviorment `.env` variables (best to create `.env.test` in the `/tests` directory):
```
export FLOSSCASTER_DATA_PATH=backend/tests/data
export DATABASE_FILE=backend/tests/data/test.db
export UPLOAD_PATH=backend/tests/uploads
export RSS_FILE=backend/tests/data/feed.xml
export FRONTEND_URL="localhost:3000"
export PYTHONPATH=backend/src
```
The following commands should be executed from the parent directory 
```
cd /flosscaster
```
Load the environmental variables
```
source backend/tests/.env.test
```
Install all necessary Packages
```
pip install pytest gtts pydub
```
Create neccessary directories for testing
```
mkdir ./backend/tests/data
```
## Execute test
_at the moment the test_create test are failing_

Dont forget to navigate to the parent directory `/flosscaster` before executing the tests.
```
python3 -m pytest

# or just 

pytest

# (didn't work for me though)
```
