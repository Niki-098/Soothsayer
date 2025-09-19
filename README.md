# Document Q&A Assistant

A simple Streamlit app that lets you upload PDFs or Excel files, extracts their content, and asks questions about them using Ollama models (like TinyLlama).

## Setup

### Clone / download this project.

git clone https://github.com/Niki-098/Soothsayer.git


### Create a virtual environment (optional but recommended).

python -m venv venv<br>
venv\Scripts\activate      # Windows<br>
source venv/bin/activate   # macOS/Linux<br>


### Install dependencies.

pip install -r requirements.txt<br><br>


Make sure Ollama is running and you have pulled a model, e.g.:<br>

ollama pull tinyllama<br>
ollama serve

## Usage

### Run the app:

streamlit run app.py


### Open in browser:
Streamlit will open automatically, usually at http://localhost:8501
.

### Steps inside the app:

Upload PDF or Excel (.xlsx/.xls) files from the sidebar.<br>

Preview extracted text, tables, or Excel sheets.<br>

Enter a question about the documents.<br>

The app builds a prompt and sends it to Ollama for an answer.



