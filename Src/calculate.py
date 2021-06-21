import speech_recognition as sr
from gtts import gTTS
import wikipedia
from mediawiki import MediaWiki
import operator
import os
  
# Initialize the recognizer 
r = sr.Recognizer() 
  
# Function to convert text to
# speech
def SpeakText(command):
    tts = gTTS(text=command, lang="en-in")
    filename = 'calculate.mp3'
    tts.save(filename)
    os.system("mpg123 calculate.mp3")


def wiki(title):
    """para = wikipedia.summary(title , sentences = 2)
    print(para)
    SpeakText(para)"""
    try:
        wikipedia = MediaWiki()
        p = wikipedia.summary(title,sentences = 2)
        print(p)
        SpeakText(p)

    except:
        SpeakText("Sorry , cant find an adequate paragraph about this title")
        pass

    return 

def get_operator_fn(op):
    return {
        '+' : operator.add,
        '-' : operator.sub,
        'x' : operator.mul,
        'divided' :operator.__truediv__,
        'Mod' : operator.mod,
        'mod' : operator.mod,
        '^' : operator.xor,
        '**' : operator.pow,
        }[op]

def eval_binary_expr(op1, oper, op2):

    print(type(op1) , op1)
    print(type(op2) , op2)
    
    if(op1=='sex'):
        op1 = '6'
    if(op2=='sex'):
        op2 = '6'
    if(op1=='aur'):
        op1 = '4'
    if(op2=='aur'):
        op2 = '4'

    op1,op2 = int(op1), int(op2)
    if(oper=='into' or oper=='multiply'):
        oper = 'x'

    if(oper=='add' or oper=='sum' or oper=='some' or oper=='plus'):
        oper = '+'

    if(oper=='or'):
        oper = '^'

    if(oper=='power'):
        oper = '**'

    return get_operator_fn(oper)(op1, op2)

      
# Loop infinitely for user to
# speak

def problem():

    while(1):    
          
        # Exception handling to handle
        # exceptions at the runtime
        try:
              
            # use the microphone as source for input.
            with sr.Microphone() as source2:
                  
                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level 
                #SpeakText('adjusting noises for clear inputs')
                r.adjust_for_ambient_noise(source2, duration=1)
                #r.adjust_for_ambient_noise(source2)
                ################### CHANGE THE MICROPHONE LIGHT AFTER 1 SEC (A GESTURE TO ASK THE QUESTION)##########
                print("speak now")
                SpeakText("ask a mathematical problem")
                #listens for the user's input 
                audio2 = r.listen(source2)
                  
                # Using ggogle to recognize audio
                MyText = r.recognize_google(audio2)
                MyText = '10 plus 2'
      
                print("Did you say "+MyText)
                SpeakText("searching for " + MyText)
                try:
                    ans = eval_binary_expr(*(MyText.split()))
                    print((ans))
                    SpeakText("the answer is " + str(ans))
                    #SpeakText("thanks for asking !")
                except:
                    SpeakText("sorry this is not a proper problem , please try again")

                return 
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
              
        except sr.UnknownValueError:
            print("unknown error occured")
            
problem()