"""
    Reads Data from .csv in Utilities Folder OR from Google Sheet (G Sheet reader code not yet added)
    Output -> WhatsApp message Sent
    To Note:
            --Use Chrome Browser
            --WhatsApp Web already signed on to your Browser
            --This Code has been Tested on a 1920 * 1080 Landscape Display with two monitors, you might need to figure
               out your screen resolution using the get_screen_details function.
            -- You might also have to uncomment pyautogui.moveTo() in the code below and play around with the scaling
               factors (sfh,sfw) in the Setting.py file to get the message Bar pressed in the whatsApp on Web messenger.
            -- Dates are used in the %-m%d format i.e. 2nd May is 502 , without the leading 0
            -- Timezone +08 means UTC + 8 ie HongKong/Singapore TimeZone. It will be used further to automate sending at
                midnight of the timezone in next iteration.
"""
import random
import pywhatkit as pwt
import pyautogui
from tkinter import *
from Utilities import settings, messages as msg
import pandas as pd
from datetime import datetime


def get_screen_details() -> tuple:
    """ To get Scaling Factor based on the screen resolution to ensure the Send Button is pressed at correct Pixels"""
    my_win = Tk()  # Setup Tkinter Window
    screen_width = my_win.winfo_screenwidth()  # Gets the resolution (width) of your monitor
    screen_height = my_win.winfo_screenheight()  # Gets the resolution (height) of your monitor
    return screen_width, screen_height


def decide_msg_and_image(msgtype: str, event: str) -> tuple:
    """ Get the Kind of Msgs and Image to Send"""
    if event == 'BirthDay':
        image = msg.images_birthday[random.randint(0, len(msg.images_birthday) - 1)]
        if msgtype == 'message_friends_not_4_everyone':
            message = msg.message_friends_not_4_everyone[random.randint(0, len(msg.message_friends_not_4_everyone) - 1)]
        elif msgtype == 'messages_special_spouse':
            message = msg.messages_special_spouse[random.randint(0, len(msg.messages_special_spouse) - 1)]
        elif msgtype == 'messages_good_friends':
            message = msg.messages_good_friends[random.randint(0, len(msg.messages_good_friends) - 1)]
        else:
            message = msg.messages_general[random.randint(0, len(msg.messages_general) - 1)]

    elif event == 'Anniversary':
        image = msg.images_anniversary[random.randint(0, len(msg.images_anniversary) - 1)]
        if msgtype == 'messages_special_spouse':
            message = msg.messages_anniversary_spouse[random.randint(0, len(msg.messages_anniversary_spouse) - 1)]
        else:
            message = msg.messages_anniversary_general[random.randint(0, len(msg.messages_anniversary_general) - 1)]

    return message, image


def send_msg(my_row: list, event: str):
    scaling_width, scaling_height = get_screen_details()
    final_message, final_image = decide_msg_and_image(msgtype=my_row[-1], event=event)
    final_image = f"{settings.BASE_DIR}\\Images\\{final_image}"
    message = f'Hey {my_row[1]}. Happy {event}. Hope you have a great Day!'
    tt = datetime.today().strftime('%H:%M')
    tt_h = int(tt.split(':')[0])
    tt_m = int(tt.split(':')[1])
    pwt.sendwhats_image(receiver=f'{my_row[2]}', img_path=final_image, caption=f'{final_message}', wait_time=15, tab_close=True, close_time=3)
    # pyautogui.moveTo(scaling_width * settings.sfw, scaling_height * settings.sfh)  # Moves the cursor the the message bar in Whatsapp
    # pyautogui.click()  # Clicks the bar if only press enter doesnt work
    pyautogui.press('enter')  # Sends the message
    pwt.sendwhatmsg(phone_no=f'{my_row[2]}', message=f'{message}', time_hour=tt_h, time_min=tt_m + 1, wait_time=18, tab_close=True, close_time=3)
    # pyautogui.moveTo(scaling_width * settings.sfw, scaling_height * settings.sfh)  # Moves the cursor the the message bar in Whatsapp
    # pyautogui.click()  # Clicks the bar if only press enter doesnt work
    pyautogui.press('enter')  # Sends the message


def find_today_persons():
    (td, tt) = settings.today_date.split(' ')  # Get Date and Time for today separately
    if settings.use_google_sheet is False:
        my_celebrations_file = pd.read_csv(settings.names_file, delimiter=',')
        today_birthday_list = my_celebrations_file[my_celebrations_file['BirthDay'] == int(td)]
        today_anniversary_list = my_celebrations_file[my_celebrations_file['Anniversary'] == int(td)]
    else:
        pass  # GoogleReader Code will be added in next iteration
    if len(today_birthday_list) > 0:
        for row in today_birthday_list.itertuples(index=True):
            my_list = [row.Name, row.Alias, row.PhoneNumber, row.TimeZone, row.MessageType]
            send_msg(my_row=my_list, event='BirthDay')
    if len(today_anniversary_list) > 0:
        for row in today_anniversary_list.itertuples(index=True):
            my_list = [row.Name, row.Alias, row.PhoneNumber, row.TimeZone, row.MessageType]
            send_msg(my_row=my_list, event='Anniversary')


if __name__ == '__main__':
    find_today_persons()