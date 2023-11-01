"""
Program 1: Build a Flask app that scrapes data from multiple websites and displays it on your site.
You can try to scrap websites like YouTube , Amazon and show data on output pages and deploy it on cloud
platform .

"""

from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)
app.config['STATIC_FOLDER'] = '/images'

save_dir = "static/images"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)


def scrape_google_images(url, query):
    """
    Scrape images from Google Image Search results.

    :param url: (str) The URL of the Google Image Search results page.

    Downloads and saves images to the 'static/images' directory.

    """
    response = requests.get(url, params=query)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        images = soup.find_all("img")

        del images[0]

        for i in images:
            image_url = i["src"]
            image_data = requests.get(image_url).content

            with open(os.path.join(save_dir, f"{query}_{images.index(i)}.jpg"), "wb") as directory:
                directory.write(image_data)


def get_image_files(directory, search_query):
    """
    Get a list of image files in the specified directory that match the Google search query.

    :param directory: (str) The directory to search for image files.
    :param search_query: (str) The Google search query string.

    :return: list[str]: A list of image file names matching the query.
    """
    image_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") and filename.startswith(search_query):
            image_files.append(filename)

    return image_files


@app.route("/")
def home():
    item = request.form.get("user_input")
    return render_template("index.html", user_input=item)

@app.route('/result', methods=["POST"])
def index():
    """
    Main route for the Flask app.

    :return:
    str: HTML page with scraped and displayed images.

    Example:
    When a user accesses the root URL, the route scrapes images from Google Image Search results and displays them on an HTML page.
    """
    item = request.form.get("user_input")
    google_search_url = f"https://www.google.com/search?q={item}&tbm=isch&ved=2ahUKEwiaoNfao5qCAxVAm2MGHXewC3MQ2-cCegQIABAA&oq=lal+bagh&gs_lcp=CgNpbWcQAzIECCMQJzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDoHCCMQ6gIQJzoLCAAQgAQQsQMQgwE6CAgAELEDEIMBOggIABCABBCxAzoECAAQA1DPCFjMJGCgJ2gBcAB4AIABgQGIAdgIkgEDMC45mAEAoAEBqgELZ3dzLXdpei1pbWewAQrAAQE&sclient=img&ei=m8w9ZdrmNsC2juMP9-CumAc&bih=911&biw=1903&hl=en"
    scrape_google_images(google_search_url, item)
    google_data = get_image_files(save_dir, item)
    return render_template('index.html', image_files=google_data)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)

