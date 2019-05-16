ffmpeg -i pritcha_color_deniose.mov -i watermark.png -filter_complex "[1]lut=a=val*0.2[a];[0][a]overlay=0:0" -t 6 pritcha_wm24.mp4
