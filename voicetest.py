import pyttsx3 
engine = pyttsx3.init() 
voices = engine.getProperty('voices') 
for voice in voices: 
    print(voice, voice.id)
    if 'French' in voice.name:
        engine.setProperty('voice', voice.id) 
        engine.say(f"Bonjour Diane, je suis la voix du gn!") 
        engine.runAndWait() 
        engine.stop() 

    break