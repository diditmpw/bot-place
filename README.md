# Project Documentation

This is a fullstack project that consists of a React frontend and a FastAPI backend. This application also incorporates the use of a Large Language Model (LLM) to provide enhanced functionality. Below are the details for setting up and running both parts of the application.


## Install Local LLM

This project uses Ollama to run a local large language model.

1.  **Install Ollama:** Follow the installation instructions for your operating system (macOS, Windows, or Linux) on the [Ollama website](https://ollama.com/).
2.  **Download Llama 3:** Once Ollama is installed, open your terminal and run the following command to download the Llama 3 model.
    ```bash
    ollama pull llama3
    ```
3.  **Run the Ollama Server:** The Ollama server typically runs in the background automatically. If you need to manually start it, you can use the following command:
    ```bash
    ollama serve
    ```

## Client Setup

1.  **Create `.env` file:** In the root of the `client` directory, create a new file named `.env`.

2.  **Add environment variables:** Paste the following into your new `.env` file, and replace `your_key` with your actual Google Maps API key.

    ```env
    REACT_APP_GOOGLE_MAPS_API_KEY=your_key
    REACT_APP_SERVER_URL=http://localhost:8000
    ```

3.  **Navigate to the `client` directory:**

    ```bash
    cd client
    ```

4.  **Install dependencies:**

    ```bash
    npm install
    ```

5.  **Start the development server:**

    ```bash
    npm start
    ```

## Server Setup

1.  **Create `.env` file:** In the root of the `server` directory, create a new file named `.env`.

2.  **Add environment variables:** Paste the following into your new `.env` file, and replace `your_key` with your actual Google Maps API key.

    ```env
    GOOGLE_MAPS_API_KEY=your_key
    CLIENT_URL=http://localhost:3000
    ```

3.  **Navigate to the `server` directory:**

    ```bash
    cd server
    ```

4.  **Create and activate a virtual environment:**

    ```bash
    # Create virtual environment
    python -m venv venv

    # Activate virtual environment
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows:
    venv\Scripts\activate
    ```

5.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

6.  **Run the FastAPI application:**

    ```bash
    uvicorn app.main:app --reload
    ```

## Features

- The frontend is built using React.
- The backend is built using FastAPI, providing a RESTful API for the frontend.

