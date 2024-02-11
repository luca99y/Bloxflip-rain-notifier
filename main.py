import cloudscraper, time
from discord_webhook import DiscordWebhook
from playsound import playsound

# -------------- CONFIG --------------

# --webhook stuff--
# if it should send webhook message or not
webhook_state = False
# url of webhook
webhook = ""
# the user id of the user to ping
user_to_ping = "<@1234567890>"

# -- notifs
# If it should play sound or not
shoud_play_sound = True
# path to sound
sound_to_play = "Notification.wav"
# --general settings
# The minimum amount of robux to be notified
min_amount_of_robux = 500
# how many seconds to wait between checks
refresh_rate = 30


while True:
    try:
        # creates the scrapper
        scraper = cloudscraper.create_scraper()
        # gets json from chat history (history is very scary word)
        r = scraper.get('https://api.bloxflip.com/chat/history').json()
        check = r['rain']
        # checks if it gives enough bobux and if its active
        if check['active'] and check['prize'] >= min_amount_of_robux:
            # gets rain duration information
            getduration = check['duration']
            umduration = getduration / 60000
            duration = round(umduration)
            convert = (getduration / (1000 * 60)) % 60
            waiting = (convert * 60 + 10)
            # time when the rain started
            date = time.strftime("%d/%m/%Y %I:%M:%S %p", time.localtime(int(time.time())))
            # print to console about the giveaway
            print(f"New rain {date}\n{check['prize']} Robux\nExpires in {duration} minutes\n")
            # play notification sound
            if shoud_play_sound == True:
                playsound(sound_to_play)
            # send to webhook
            if webhook_state:
                DiscordWebhook(url=webhook, content=f"New rain {date}\n{check['prize']} Robux\nExpires in {duration} minutes\n{user_to_ping}").execute()
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
