import speech_recognition as sr
from gtts import gTTS
import calculate
import voiceAssistant
import emotion
import objectdetection
import faceRecog
import faceCollect
import os

from PIL import Image, ImageSequence
from luma.core.sprite_system import framerate_regulator
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
import time

serial = i2c(port=1, address=0x3C)
device = sh1106(serial)

os.system("mpg123 audio/intro.mp3")

# Initialize the recognizer 
r = sr.Recognizer() 
  
# Function to convert text to speech
def SpeakText(command):
    tts = gTTS(text=command, lang="en-in")
    filename = 'speak.mp3'
    tts.save(filename)
    os.system("mpg123 speak.mp3")

os.system("mpg123 audio/afterIntro.mp3")

complete = 1
while(1):    
      
    # Exception handling to handle
    # exceptions at the runtime
    try:
        
        regulator = framerate_regulator(fps=10)
        img_path = 'images/neutral.gif'
        gify = Image.open(img_path)
        device.size = (128, 128)
        size = [min(*device.size)] * 2
        posn = ((device.width - size[0]) // 2, device.height - size[1] + 30)
        for frame in ImageSequence.Iterator(gify):
            with regulator:
                background = Image.new("RGB", device.size, "white")
                background.paste(frame.resize(size, resample=Image.LANCZOS), posn)
                device.display(background.convert(device.mode))
        
        # use the microphone as source for input.
        with sr.Microphone() as source2:
              
            #SpeakText('adjusting noises for clear inputs')
            if(complete==1):
                os.system("mpg123 audio/beforeSayingName.mp3")
            
            r.adjust_for_ambient_noise(source2, duration = 1)
            ############## TURN ON THE MICROPHONE LIGHT AFTER 1 SEC ##############
            #listens for the user's input 
            
            print('speak now')
            audio2 = r.listen(source2)
            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()


            print("Did you say "+MyText)
            complete = 0
            if(MyText=='hey cherry' or MyText=='hi cherry' or MyText=='cherry' or MyText=='hello cherry' or MyText=='chori' or MyText=='high chori' or MyText=='hi chori' or MyText=='hey chori' or MyText=='hey chaudhri' or MyText=='hi chaudhri' or MyText=='chaudhri' or MyText=='hay teri' or MyText=='hey sorry' or MyText=='hay sorry' or MyText=='chayani' or MyText=='hey chayani'):
                complete = 1
                try:
                    os.system("mpg123 audio/afterFirstCommand.mp3")
                    print('speak the command')
                    command = ''
                    audio = r.listen(source2)
                    command = r.recognize_google(audio)
                    command = command.lower()
                    
                    print('command :- ' , command)


                    if( (command.find('emotion') != -1 or command.find('emotions') != -1 or command.find('motions') != -1 ) and ( command.find('not') == -1 or command.find('dont') == -1 ) ):
                        os.system("mpg123 audio/afterFirstCommand.mp3")
                        emotion.checkEmotion()
                        continue  
                        

                    elif((command.find('maths') != -1 or command.find('maths problem') != -1 or command.find('mathematical problem') != -1) and (command.find('not') == -1 or command.find('dont') == -1)):
                        os.system("mpg123 audio/afterFirstCommand.mp3")
                        calculate.problem()
                        continue
                       

                    elif((command.find('detect') != -1 and command.find('object') != -1) and (command.find('not') == -1 or command.find('dont') == -1)):
                        os.system("mpg123 audio/afterFirstCommand.mp3")
                        objectdetection.detectObject()
                        continue
                            

                    elif((command.find('detect') != -1 and command.find('face') != -1) and (command.find('not') == -1 or command.find('dont') == -1)):
                        os.system("mpg123 audio/afterFirstCommand.mp3")
                        faceRecog.recognise()
                        continue
                        
                        
                    elif((command.find('search') != -1 or command.find('internet') != -1) and (command.find('not') == -1 or command.find('dont') == -1)):
                        os.system("mpg123 audio/afterFirstCommand.mp3")
                        voiceAssistant.internet()
                        continue
                        

                    elif((command.find('collect') != -1 and command.find('face') != -1 and command.find('data') != -1) or (command.find('become my friend') != -1) ):
                        os.system("mpg123 audio/afterFirstCommand.mp3")
                        faceCollect.collect()
                        continue
                      

                    else:
                        SpeakText("no such feature available ")
                        continue
                except:
                    SpeakText('no command recognised')

                SpeakText("thanks for asking !")
    
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
          
    except sr.UnknownValueError:
        print("unknown error occured")
        complete = 0

