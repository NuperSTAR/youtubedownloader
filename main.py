from flask import Flask, request, render_template_string, send_from_directory
from pytube import YouTube
import os

app = Flask(__name__)
download_path = 'downloads'

# HTML content
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>YouTube Downloader</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f0f2f5;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
            width: 500px;
            max-width: 100%;
        }
        h2 {
            color: #333;
            margin-bottom: 20px;
        }
        form {
            margin-bottom: 20px;
        }
        input[type="text"] {
            width: calc(100% - 20px);
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        input[type="submit"] {
            width: 100%;
            padding: 10px;
            border: none;
            background-color: #007bff;
            color: white;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
        }
        video {
            width: 100%;
            border-radius: 4px;
            margin-bottom: 10px;
        }
        a {
            display: inline-block;
            text-decoration: none;
            background-color: #28a745;
            color: white;
            padding: 10px 15px;
            border-radius: 4px;
            transition: background-color 0.3s ease;
        }
        a:hover {
            background-color: #218838;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>YouTube Video Downloader</h2>
        <p>Download your favorite videos! First, enter your youtube video url, and one click away can download it for you! (some videos might be restrictied.)</p>
        <form action="/" method="post">
            <input type="text" id="url" name="url" placeholder="enter youtube url (some videos might be restrictied.)" required>
            <input type="submit" value="Download and Preview">
        </form>
         <p>i can see your videos lol</p>
        {% if filename %}
            <video width="560" height="315" controls>
                <source src="/downloads/{{ filename }}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            <a href="/downloads/{{ filename }}" download>Download Video</a>
        {% endif %}
    </div>
</body>
</html>

'''


@app.route('/', methods=['GET', 'POST'])
def index():
    filename = ''
    if request.method == 'POST':
        url = request.form['url']
        filename = download_video(url)
    return render_template_string(HTML, filename=filename)


@app.route('/downloads/<filename>')
def download(filename):
    return send_from_directory(download_path, filename, as_attachment=True)


def download_video(url):
    try:
        yt = YouTube(url)
        # Additional code to handle age restrictions
        video = yt.streams.get_highest_resolution()
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        video.download(download_path)
        return video.default_filename
    except Exception as e:
        return ''


if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change port if 5000 is busy
