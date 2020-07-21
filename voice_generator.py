import vlc
from gtts import gTTS

#small script to generate various mp3 messages ( text to speech )
#save them at the same directory and use them later in the main script to output various audio messages
def say(text, name):
    tts = gTTS(text=text, lang="en")
    filename = name+".mp3"
    tts.save(filename)
    p = vlc.MediaPlayer(filename)
    p.play()
    
#say("Hello, my name is Veronica. To unlock the door with facial recognition, press the Blue button... To leave a voice-mail, press the Red button... ", "welcome")
