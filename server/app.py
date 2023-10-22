import os
import ssl
import urllib.request
from gtts import gTTS
from flask_cors import CORS
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

# Initialize app
app = Flask(__name__)
CORS(app) 

context = ssl._create_unverified_context()

@app.route('/api/search', methods=['POST'])
def search():
    data = request.get_json()
    keyword = data.get('keyword')
    output_folder = '/Users/hercules/Desktop/webScraper_assignment/client/public/'


    # Construct the URL for the Google search
    search_query = keyword.replace(" ", "+")
    url = f"https://www.google.com/search?q={search_query}"

    # User-Agent header to mimic a web browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.9999.99 Safari/537.36"
    }

    # Create a Request object with headers
    req = urllib.request.Request(url, headers=headers)

    try:
        response = urllib.request.urlopen(req, context=context)
        
        data = response.read().decode("utf-8")
        soup = BeautifulSoup(data, "html.parser")

        #extracting data from response
        image_element = soup.find('div', class_='Gor6zc')
        title_element = soup.find('span', class_='pymv4e')
        price_element = soup.find('span', class_='e10twf')

        if image_element and title_element and price_element:
            image = image_element.find('img')['src']
            title = title_element.get_text()
            price = price_element.get_text()

            #text-to-speech
            text = f"The price of {title} is {price}"
            audio_file_name = f"{title.replace(' ', '_')}.mp3"
            audio_file = os.path.join(output_folder, f"{title.replace(' ', '_')}.mp3")
            tts = gTTS(text, lang='en')
            tts.save(audio_file)

            #return extracted text
            return jsonify({'image':image, 'title':title, 'price':price, 'audio_file':audio_file_name, 'status': "success"})
        else:
            return jsonify({'image':"", 'title':"", 'price':"", 'status': "error"})
    except urllib.error.HTTPError as e:
        return jsonify({'error': f"HTTP Error {e.code}: {e.reason}"})

if __name__ == '__main__':
    app.run(debug=True, port=8080)
