# Call Transcript Analyzer (Mini Tech Challenge)

This project is a small FastAPI app that analyzes customer transcripts using Groq.<br>
It generates a summary and detects sentiment (Positive / Neutral / Negative), then saves results to a CSV file.

## Setup

### Clone / download this project.

git clone https://github.com/Niki-098/Soothsayer.git


### Create a virtual environment (recommended).

python -m venv venv<br>
source venv/bin/activate   # macOS/Linux<br>
venv\Scripts\activate      # Windows<br>


### Install dependencies.

pip install -r requirements.txt


### Usage

*Start the server:*

uvicorn main:app --reload --port 8000


### Open in browser:

Go to: http://127.0.0.1:8000<br>

Paste a transcript and click Analyze.

### API usage with JSON:

curl -X POST "http://127.0.0.1:8000/analyze" \<br>
     -H "Content-Type: application/json" \<br>
     -d '{"transcript": "Hi, I was trying to book a slot yesterday but the payment failed..."}'


### Check results:

Console prints transcript, summary, and sentiment.<br>

Results are saved into call_analysis.csv with columns:<br>

Transcript | Summary | Sentiment
