import cloudscraper, time
from discord_webhook import DiscordWebhook
import playsound

# -------------- CONFIG --------------

# --webhook stuff--
# who doesnt understand this should commit suicide
webhook_state = False
# url of webhook
webhook = ""
# the user id of the user to ping
user_to_ping = "<@1234567890>"

# -- notifs
# who doesnt understand this should commit suicide
shoud_play_sound = True
# path to sound
sound_to_play = "Notification.wav"

# --general settings
# who doesnt understand this should commit suicide
min_amount_of_robux = 500
# how many seconds to wait between checks
refresh_rate = 30
















# check for webhook
if webhook_state:
    # creating webhook and adding content
    webhook = DiscordWebhook(url=webhook, content=f"{user_to_ping} new giveaway")

while True:
    try:
        # creates the scrapper
        scraper = cloudscraper.create_scraper()
        # gets json from chat history (history is very scary word)
        r = scraper.get('https://api.bloxflip.com/chat/history').json()
        check = r['rain']
        # checks if it gives enough bobux and if its active
        if check['active'] and check['prize'] >= min_amount_of_robux:
            # print to console about the giveaway
            print("New rain ", check['prize'], " Robux")
            # play notification sound
            if shoud_play_sound == True:
                playsound(sound_to_play)
            # send to webhook
            if webhook_state:
                webhook.execute()
            # gets rain duration information
            getduration = check['duration']
            umduration = getduration/60000
            duration = round(umduration)
            convert = (getduration/(1000*60))%60
            waiting = (convert*60+10)
            # waits until the rain ends before checking for rain again
            time.sleep(waiting)
        else:
            time.sleep(refresh_rate)

        # pro memory leak fix
        scraper.close()

    except Exception as error:
        print("The programm errored")
        print(error)
        time.sleep(refresh_rate)
