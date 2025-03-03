```markdown
# PDF Summarizer

## Overview
PDF Summarizer is a Chrome extension that extracts text from PDF files and sends it to a Flask backend for automated summarization. It integrates a custom PDF viewer and uses NLP techniques to generate concise summaries.

## Features
- **Custom PDF Viewer:** Displays and extracts text from PDFs.
- **Automated Summarization:** Uses NLP to generate meaningful summaries.
- **Chrome Extension:** Includes a popup interface for easy interaction.
- **Backend Integration:** Connects to a Flask API for processing.

## Installation
### 1. Clone the Repository
```bash
git clone https://github.com/your-username/pdf-summarizer.git
cd pdf-summarizer
```

### 2. Set Up the Backend
```bash
# Navigate to the backend directory (if applicable)
cd backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py
```

### 3. Load the Chrome Extension
1. Open **Google Chrome** and go to `chrome://extensions/`.
2. Enable **Developer mode** (toggle in the top right).
3. Click **Load unpacked** and select the project folder.
4. The PDF Summarizer extension should now appear in your extensions list.

## Usage
1. Open a PDF file using the custom PDF viewer.
2. Click the **Summarize PDF** button in the popup.
3. The extracted text is sent to the Flask backend, and a summary appears in the extension.


## Future Improvements
- Add **support for multiple languages** in summarization.
- Enhance **summary accuracy** using fine-tuned transformer models.
- Improve **user interface** with a better design.
