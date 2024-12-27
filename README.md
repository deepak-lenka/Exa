# RLAIF Search Pipeline

This project implements a Retrieval-augmented Language AI Framework (RLAIF) search pipeline using the Exa API. It provides a simple web interface for performing various types of searches and finding similar documents.

## Features

- Basic neural search with autoprompt
- Advanced search with full text and highlights
- Similar document search based on URLs
- Category-based filtering
- Interactive web interface using Streamlit

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root and add your Exa API key:
```
EXA_API_KEY=your_api_key_here
```

3. Run the web application:
```bash
cd src
streamlit run app.py
```

## Usage

The web interface provides three main search options:

1. **Basic Search**: Simple neural search with autoprompt
2. **Advanced Search**: Full-featured search with content retrieval and category filtering
3. **Similar Documents**: Find similar documents based on a URL

Each search type provides relevant configuration options and displays results with titles, scores, and content where available.

## Project Structure

- `src/search_engine.py`: Core search implementation using Exa API
- `src/app.py`: Streamlit web interface
- `requirements.txt`: Project dependencies
- `.env`: Environment variables (create this file)
