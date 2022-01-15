for i in *.ogg; do ffmpeg -i $i "${i%.ogg}.wav"; done
