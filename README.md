# voice-assistant
 SST+chatGPT+TTS

you have to get a open api key to run this program, if you don't have one go: https://platform.openai.com/account/api-keys sign in and get one.

Then put your API key at the "setting.txt", replace the {OPEN API KEY} with your API key.

HOW TO USE:
1. Run "chatgpt-vyov.py".
2. It will ask you if you want to continue last conversation, if no, type 'n'，yes then type 'y'.(actually it only check for 'n')
3. It will ask you to choose an identity file, in the 'AI_Identity' fold, you can try to add some by directly add file in 'AI_Identity' or type 0 at this point to create one (recommend to watch my examples before write), I set AI's name Alex, and user's name Johnny, if you want to change, you can check the code, there are a global parameter of 'AI_NAME' and 'USER_NAME'.
4. There are three sound you will hear, first is a 'su' sound, means you can speak, program is listening. Second is a sound of hanging up a telephone means program is done listening. Third, a 'bruh' means the transcript result is nothing, maybe your voice is not loud enough, after 'bruh', it will restart the listening process.
5. Operations:say 'Clear' or in chinese '清除紀錄' will clear the conversation history. say 'Stop', 'terminate' or in chinese '結束' will terminate the program.
6. Have fun.


TIPS:
1. If the response text is too long, the output audio may not working, you can adjust 'max_token' in 'setting.txt' to limit the respond text length.
2. Add 'Wait for Johnny's respond.' to the end of your ai identity file to make sure the ai model don't create the conversation between Alex and Johnny(Sometimes it still do that, but very rare)