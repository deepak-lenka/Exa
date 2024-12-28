# EXA Search Pipeline

A powerful search application built with the Exa API and Streamlit, providing neural search capabilities with a user-friendly interface.

## Features

- **Basic Search**: Neural search with autoprompt technology (up to 25 results)
- **Advanced Search**: Full-featured search with content retrieval and highlights (up to 50 results)
- **Similar Documents**: Find related documents based on URLs
- **Category Filtering**: Filter results by document type (company, research paper, news, etc.)
- **Rich Content Display**: View full text, highlights, authors, and publication dates
- **Interactive UI**: Built with Streamlit for a seamless user experience

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- An Exa API key (get it from [Exa's website](https://exa.ai))

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd Exa
```

2. Create and activate a virtual environment:
```bash
# On macOS/Linux
python -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
.\venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables:
   - Create a new file named `.env` in the project root directory
   - Add your Exa API key to the `.env` file with the following content:
     ```
     EXA_API_KEY=your_api_key_here
     ```

## Running the Application

1. Ensure your virtual environment is activated:
```bash
source venv/bin/activate  # On macOS/Linux
.\venv\Scripts\activate   # On Windows
```

2. Start the Streamlit application:
```bash
streamlit run src/app.py
```

The application will open automatically in your default web browser at http://localhost:8501

## Usage Guide

### Basic Search
- Enter your search query in the text area
- Adjust the number of results (1-100, default: 25)
- Click "Search" to see results

### Advanced Search
- Enter your search query
- Adjust the number of results (1-100, default: 50)
- Configure additional options:
  - Include full text
  - Include highlights
  - Select category filter
- Click "Search" to see results

### Similar Documents
- Enter a URL to find similar content
- Adjust the number of results (1-100, default: 25)
- Toggle source domain exclusion
- Click "Find Similar" to see results

## Project Structure

```
Exa/
├── src/
│   ├── app.py             # Streamlit web interface
│   └── search_engine.py   # Core search implementation
├── .env                   # Environment variables (create this)
├── requirements.txt       # Project dependencies
└── README.md             # Documentation
```

## Environment Variables

Required environment variables in `.env`:
- `EXA_API_KEY`: Your Exa API key (required for all search operations)

## Dependencies

- exa-py (≥1.7.1): Exa API Python client
- python-dotenv (≥1.0.0): Environment variable management
- streamlit (≥1.29.0): Web interface framework

## Troubleshooting

1. **API Key Issues**:
   - Ensure your `.env` file exists in the project root
   - Verify your API key is correctly formatted
   - Check that python-dotenv is installed

2. **Installation Issues**:
   - Make sure your Python version is compatible
   - Try upgrading pip: `pip install --upgrade pip`
   - Install dependencies one by one if bulk install fails

3. **Runtime Issues**:
   - Verify your virtual environment is activated
   - Ensure all dependencies are installed
   - Check the console for error messages

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

Made with ❤️ by Deepak Lenka

This project is licensed under the MIT License - see the LICENSE file for details.
