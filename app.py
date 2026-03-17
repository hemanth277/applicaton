from flask import Flask, render_template, request, jsonify, send_file
from scraper import selenium_scrape, save_excel
import os
# Create Flask app
app = Flask(__name__)

cache = []


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():

    global cache

    data = request.get_json()
    query = (data.get("query") or "").strip()

    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400

    print("Searching:", query)

    try:
        results = selenium_scrape(query)
    except Exception as e:
        print("Search error:", e)
        return jsonify({"error": str(e)}), 500

    cache = results

    if not results:
        print("No results returned for", query)

    return jsonify(results)


@app.route("/download")
def download():

    file = save_excel(cache)

    return send_file(file, as_attachment=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
