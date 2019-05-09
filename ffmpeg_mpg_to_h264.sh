for i in *.MPG ; do ffmpeg -i $i -c:v libx264 -c:a aac -crf 16 "${i%.MPG}.mp4" ; done
