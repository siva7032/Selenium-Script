from flask import Flask, render_template, jsonify
import subprocess
import twitter_scraper  # Import the scraper script

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run-script")
def run_script():
    try:
        result = twitter_scraper.get_trending_topics()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
