# FastAPI File Processor

This is a FastAPI application that accepts a file URL, fetches the file, partitions it, and sends the first chunk to an OpenAI GPT-4 model for processing.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/yourrepository.git
   ```
2. Navigate to the project directory:
   ```bash
   cd yourrepository
   ```
3. Install Poetry if you haven't already:
   ```bash
   curl -sSL https://install.python-poetry.org | python -
   ```
4. Install the required Python packages:
   ```bash
   poetry install
   ```

## Usage

1. Start the FastAPI server:
   ```bash
   poetry run uvicorn main:app --reload
   ```
2. Send a POST request to the `/process` endpoint with a JSON body that contains the `url` parameter. Replace `http://example.com/path/to/your/file` with the actual URL of the file you want to process:
   ```bash
   curl -X POST "http://localhost:8000/process" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"url\":\"http://example.com/path/to/your/file\"}"
   ```

## API Key

The application uses an OpenAI API key for the GPT-4 model. Make sure to replace the placeholder API key in the `main.py` file with your actual OpenAI API key.

## License

This project is licensed under the terms of the MIT license.
