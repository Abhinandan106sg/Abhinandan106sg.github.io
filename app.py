from flask import Flask,render_template,request,flash
from pytube import YouTube,Playlist
from pytube.exceptions import VideoUnavailable
import os

app = Flask(__name__)
app.secret_key="Abhigouli"

@app.route('/')
def index():
	return render_template("index.html",
							content1="Enter a valid video link",
							content2="Live streaming, private videos and Unavilable videos cannot be downloaded",
							alert_class="alert",
							content3="Enter a valid playlist link",
							content4="Unavailable videos will be automatically skipped",
							alert_class_playlist="alert")

		
@app.route('/download_video',methods=['POST'])
def download_video():

	if request.method == 'POST':
		link=request.form.get('link')

		try:
			yt=YouTube(link)
			video = yt.streams.get_highest_resolution()
			video.download(os.path.join(app.root_path, 'downloads'))

			return render_template("index.html",
						  			content1="Download Successfull",
						  			content2=f"{video.title} downloaded",
						  			alert_class="alert alert-success",
									content3="Enter a valid playlist link",
									content4="Unavailable videos will be automatically skipped",
									alert_class_playlist="alert")
			
		except Exception as error:
			return render_template("index.html",
									content1=f"{link} is unavailable",
									content2="Please provide a valid link",
									alert_class="alert alert-danger",
									content3="Enter a valid playlist link",
									content4="Unavailable videos will be automatically skipped",
									alert_class_playlist="alert")

@app.route('/download_playlist',methods=['POST'])
def download_playlist():

	if request.method == 'POST':
		playlist_link=request.form.get('playlist_link')

		try:
			p = Playlist(playlist_link)
			for video in p.videos:
				try:
					high_def_video = video.streams.get_highest_resolution()
    
				except VideoUnavailable:
					print(f"{video.title} unavailable ......... skipping ")

				else:
					# high_def_video.download(os.path.join(app.root_path, 'downloads'))
					high_def_video.download(os.path.join(app.root_path, f"downloads/{p.title}"))

			return render_template("index.html",
						  			content1="Enter a valid video link",
						  			content2="Live streaming, private videos and Unavilable videos cannot be downloaded",
						  			alert_class="alert",
									content3="Download Successfull",
									content4=f"{p.title} playlist downloaded",
									alert_class_playlist="alert alert-success")

		except Exception as error:
			return render_template("index.html",
						  			content1="Enter a valid video link",
						  			content2="Live streaming, private videos and Unavilable videos cannot be downloaded",
						  			alert_class="alert",
									content3=f"{playlist_link} not available",
									content4="Please provide a valid link",
									alert_class_playlist="alert alert-danger")


if __name__ == '__main__':

	app.run()
