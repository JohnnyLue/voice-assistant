import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import threading
import json
import requests
from ffmpeg import audio
import os

#names
AI_NAME = 'Alex'
USER_NAME = 'Johnny'

#settings
model = "gpt-3.5-turbo"
max_tokens = 120
temperature = 0.8#the certainity higher is more creative.0~2 
Authorization = ""#api key
top_p = 1#only use top n of the possible result ex:0.1==>top 10% posible answer.0~1
request_timeout = 15
main_language = ""

def input_helper(range):
    choose_code = input('\nenter the code(type 0 to create new one):')

    if(not choose_code.isdecimal()):
        print('Wrong input.(1~'+str(range)+')')
        return input_helper(range)
    else:
        if(int(choose_code)>range or int(choose_code)<0):
            print('Wrong input.(1~'+str(range)+')')
            return input_helper(range)
        else:
            return int(choose_code)
        

def choose_identity():
    all_file_name = os.listdir('AI_Identity')

    print('Choose your identity file:\n')

    counter = 1
    for file in all_file_name:
        print(counter,': ',file)
        counter=counter+1

    if (counter == 1):
        return -1

    choose_code = input_helper(counter-1)

    if(choose_code == 0):
        return 0

    return 'AI_Identity/' + all_file_name[choose_code-1]
    

    


def load_setting():
    with open('settings.txt', 'r') as file:
        data = file.readlines()

    global model
    global max_tokens 
    global temperature
    global Authorization
    global top_p
    global request_timeout
    global main_language

    print('Settings:\n')
    for i in data:
        if(i.strip().split()[0] != 'Authorization'):
            print(i.strip().split()[0] + ': '+i.strip().split()[2])
    print('')

    for i in data:
        if(i.split('=')[0].strip() == 'model'):
            model = i.strip().split()[2]
        if(i.split('=')[0].strip() == 'max_tokens'):
            max_tokens = int(i.strip().split()[2])
        if(i.split('=')[0].strip() == 'temperature'):
            temperature = float(i.strip().split()[2])
        if(i.split('=')[0].strip() == 'Authorization'):
            Authorization = i.strip().split()[2]
        if(i.split('=')[0].strip() == 'top_p'):
            top_p = float(i.strip().split()[2])
        if(i.split('=')[0].strip() == 'request_timeout'):
            request_timeout = i.strip().split()[2]
        if(i.split('=')[0].strip() == 'main_language'):
            main_language = i.strip().split()[2]



# set up STT
r = sr.Recognizer()

def play(path):
    playsound(path)

def clear_history():
    f = open('chat_history.txt','w',encoding='utf-8')
    f.close

try:
    f= open('chat_history.txt','x',encoding='UTF8')
    f.close
except:
    f = open('chat_history.txt',encoding='UTF-8')
    chat_history = f.read()
    f.close
    print("Last conversation:\n" + chat_history)

    ans = input("Continue last conversation?")
    if(ans == 'N' or ans == 'n'):
        clear_history()

print('##########################################################')

load_setting()

print('##########################################################')

identity_path = choose_identity()

if(identity_path == -1 or identity_path == 0):
    if(identity_path==-1):
        print("No Identity file found.Please create one.")
    
    ai_describe = AI_NAME +' is ' + input(AI_NAME + ' is ')
    user_describe = USER_NAME + ' is ' + input(USER_NAME + ' is ')

    new_path = 'AI_Identity/Identity'
    id = 0
    while(1):
        done = False
        try:
            with open(new_path+str(id)+'.txt','xt',encoding='UTF-8') as f:
                f.write(ai_describe)
                f.write('\n')
                f.write(user_describe)
                done = True
        except:
            id+=1

        if(done):
            break
        
    identity_path = new_path+str(id)+'.txt'

else:
    pass


print('##########################################################')

ai_identity = ''
if(identity_path != -1):
    f = open(identity_path,encoding='UTF-8')
    ai_identity = f.read()
    f.close

terminate = False

f = open('chat_history.txt',encoding='UTF-8')
chat_history = f.read()
print("history: \n"+chat_history+'\n')
f.close

while(not terminate):
    # prompt user for input
    with sr.Microphone() as source:

        t = threading.Thread(target = play,args = ("start_record_sound.mp3",))
        t.start()
        r.adjust_for_ambient_noise(source, duration=1)
        while(t.is_alive()):''

        audio = r.listen(source,phrase_time_limit=15)
        

    playsound('success_input_sound.mp3')

    # convert speech to text
    stt = r.recognize_google(audio,show_all=True,language = main_language)
    if(stt == []):
        playsound('fail_recogn_sound.mp3')
        continue
        

    text = stt['alternative'][0]['transcript']
    print("You(" + USER_NAME+ ") said: " + text + '\n')

    #clear history commend
    if(text =='clear' or text =='清除記錄' or text == '刪除記錄' or text == '刪除歷史記錄' or text =='清除歷史記錄' or text =='清除歷史' ):
        clear_history()
        continue

    #terminate condition
    if(text == 'stop' or text == 'Stop' or text == 'terminate' or text == 'Terminate' or text == '結束'):
        terminate = True
        continue

    chat_history += '\n' + USER_NAME+ ': ' + text + '\n' + AI_NAME + ': '

    all_message = ai_identity + chat_history

    #message to sent to gpt-3.5 using openai api
    url = "https://api.openai.com/v1/chat/completions"
    data = {
        "model": model,
        "messages": [{"role": "user", "content": all_message}],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + Authorization
    }


    try:
        response = requests.post(url, data=json.dumps(data), headers=headers,timeout = request_timeout)
        json_data = json.loads(response.text)

        if(json_data['choices'][0]['finish_reason'] == 'null'):
            continue

        output_text = json_data['choices'][0]['message']['content']
        print(AI_NAME + ': '+output_text+'\n')

        chat_history += output_text

        f = open('chat_history.txt','a',encoding='UTF-8')
        f.write('\n' + USER_NAME+ ': ' + text + '\n' + AI_NAME + ': ' + output_text)
        f.close()

        # convert text to speech and play output
        tts = gTTS(output_text,lang = main_language)
        tts.save('output.mp3')

        playsound('output.mp3')
    except:
        print('Error occurred.\n')
  