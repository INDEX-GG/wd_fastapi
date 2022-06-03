## fastapi server

### Instruction:
#### start:
1. fill `app/core/config.py`
2. `pip install -r requirements.txt`
3. `uvicorn app.main:app --reload `
#### start with docker:
1. fill `app/core/config.py`
2. `docker build --no-cache -t wd_api .`
3. `docker-compose up -d`