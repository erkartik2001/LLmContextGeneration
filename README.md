# LLMContextGenerationAPI

This repository contains a Flask API for generating context from an input query.

## Requirements
- Python 3.10
- requirements.txt dependencies (run pip install -r requirements.txt)

## Environment Variables
The API requires a .env file in the root directory with the following variables:

- SERPER_API_KEY: Your Serper API key.
- OPENAI_API_KEY: Your OpenAI API key.
- VALIDATION_TOKEN: The validation token to use for API requests.
- SCRAPPED_DATA_PATH: The directory path to store scraped data.
- VECTOR_DB_DIR_PATH: The directory path for the vector database.


## Running the API
Ensure Python 3.10 and dependencies are installed.
Set the VALIDATION_TOKEN environment variable with your desired token.
Run the run_server.py file:
python3 run_server.py
This will start the API on port 6000 in debug mode.


## API Endpoints

### /checkAPI
- Method: GET or POST
- Response: {"result":"Live"}
- Description: Checks if the API is running.

### /generatecontext
- Method: GET or POST
- Headers: VALIDATION-TOKEN: Your desired validation token (must match environment variable).
- Body: JSON object with the following key:
- input_query: The query for which context is required.

### Response:
- On success: {"result":**<generated_context>**}

### On error:
- 400 Bad Request: {"Error":"Missing input_query paramter in request"}
- 400 Bad Request: {"Error":"Incorrect Validation Token"}

### Example curl call for generating context

curl -X POST http://localhost:6000/generatecontext \
-H "Content-Type: application/json" \
-H "VALIDATION-TOKEN: your_token" \
-d '{"input_query": "What is the best way to make coffee?"}'

### Contributing
Pull requests are welcome for bug fixes and improvements.

