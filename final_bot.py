import discord
import random
import nest_asyncio
nest_asyncio.apply()
import gspread
import datetime
from datetime import date
import calendar
from datetime import datetime 
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from gspread_formatting.dataframe import format_with_dataframe


TOKEN = 'OTI1MDEyOTIzOTA1MDg1NDQx.Ycm7ag.86w8W9Ss-kDH2VRtu_Fi0gCEzDQ'

gc = gspread.service_account(filename ='credentials.json')
noman = gc.open_by_key('1du7kaTd12uO3qU6j6RPms1_14UJ_c300-g-7hu2E0nw')
nabeel = gc.open_by_key('1KUmXAmmCuK192VNIiT6fraNx_90NmizNmsFGv1paTXw')
hr = gc.open_by_key('16MMCXKValL2LGOk5q_egqhuVXBhzcTd-txgBbhWkNn4')

noman_attend = noman.sheet1
nabeel_attend = nabeel.sheet1
hr_attend = hr.sheet1


client = discord.Client()
@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))
@client.event
async def on_message(message):# every single message that enters the server
  username = str(message.author).split('#')[0]
  user_message = str(message.content)
  channel = str(message.channel.name)
  print(f"{username}: {user_message} ({channel})")# logging everthing that happens on server
  
  # Avoid bot to reply infinitely and reply once
  if message.author == client.user:
    return
  
  # get current date and time format
  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")
  curr_date = date.today()
  day = calendar.day_name[curr_date.weekday()]
  today = date.today()
  d1 = today.strftime("%m/%d")
 # date_time_obj = datetime. strptime(date_time_str, '%d/%m/%y %H:%M:%S')

  #today_date = day[:3] + ' '+ d1 # 
  today_date = 'Sat 1/1'
  # dictionary of employees in MATIX.AI
  Attendance = {
    "noman" : noman_attend,
    "nabeel1011" : noman_attend,
    'SyedKhurram' : noman_attend,
    "hr matix" : hr_attend
 } 
  # cell coordinates where to append sign in and sign out timings
  cell = Attendance[username.lower()].find(today_date)
  sign_in_row = cell.row
  sign_in_col = cell.col + 1 
  sign_out_row = cell.row
  sign_out_col = cell.col + 2
  flag = 0 # signed_out state
  sign_in_array = []
  sign_out_array = []
  for i in range(3):
    if Attendance[username.lower()].cell(sign_in_row, sign_in_col).value:
        sign_in_array.append(Attendance[username.lower()].cell(sign_in_row, sign_in_col).value)
        flag = 1 # signed in state
        sign_in_col = sign_in_col + 3
    else:
        break
    if Attendance[username.lower()].cell(sign_out_row, sign_out_col).value:
        sign_out_array.append(Attendance[username.lower()].cell(sign_out_row, sign_out_col).value)
        flag = 0 #signed out state
        sign_out_col = sign_out_col + 3
        



  if channel.lower() == 'general':

    if user_message.lower() == '/show_week':
        for j in range(7):
            if len(Attendance[username.lower()].cell(sign_in_row-j,1).value) > 9 or len(Attendance[username.lower()].cell(sign_in_row-j,1).value) < 1:
                break
            else:
                 temp4 = "duration of " + str( Attendance[username.lower()].cell(sign_in_row-j,1).value) + ' ' + str(Attendance[username.lower()].cell(sign_out_row-j, 11).value) + "\n" 
                 await message.channel.send(temp4)


    elif user_message.lower() == '/help':
     await message.channel.send(""" 
     Commands:
     1- "/sign_in" : add your current sign in time, maximum three sign in are allowed
     2- "/sign_in list of tasks" : add current time of sign in with tasks
     3- "/sign_out": add your current sign out time , maximum three sign out are allowed
     4- "/sign_out list of tasks": add current sign out time with tasks
     5- "/show_today": prints today sign in and sign out timings
     6- "/show_week" : prints this week sign in and sign out timings

     """)
    # Add sign in time and tasks to sheet
    elif user_message[:len("/sign_in")] == '/sign_in' and len(user_message)>len('/sign_in'):
        # if flag == "sign_in" throw error
        if flag == 1:
            await message.channel.send("cannot sign in consecutively")

        elif Attendance[username.lower()].cell(sign_in_row, 12).value:
            await message.channel.send('you have signed in with tasks already')
        else:  
           task = user_message[len("/sign_in"):len(user_message)]
           Attendance[username.lower()].update_cell(sign_in_row, sign_in_col, current_time)
           
           Attendance[username.lower()].update_cell(sign_in_row, 12, task)
           await message.channel.send("sign in acknowleged")
           # flag = sign_in
           flag = 1
           sign_in_col = sign_in_col + 3
           print("sign in added to sheet")

    # return list of tasks if user has already signed in with /sign_in tasks
    elif user_message == '/sign_in':
        # flag check sign in
        if flag == 1:
            await message.channel.send("cannot sign in consecutively")
        else:
            Attendance[username.lower()].update_cell(sign_in_row, sign_in_col, current_time)
            sign_in_col = sign_in_col + 3
            flag = 1
            await message.channel.send("sign in acknowleged")


    # sign out 
    elif user_message[:len("/sign_out")] == '/sign_out' and len(user_message)>len('/sign_out'): 
        # sign out flag check
        if flag == 0:
            await message.channel.send("cannot sign out consecutively or sign in before sign out")
        
        else:
           task = user_message[len("/sign_out"):len(user_message)]
           Attendance[username.lower()].update_cell(sign_out_row, sign_out_col, current_time)
           Attendance[username.lower()].update_cell(sign_in_row, 12, task)
           await message.channel.send("good bye, see you")
           flag = 0
           sign_out_col = sign_out_col +3
           print("sign out added to sheet")
    
    elif user_message.lower() == '/sign_out':
        #sign out flag check 
        if flag == 0:
            await message.channel.send("cannot sign out consecutively") 
        elif Attendance[username.lower()].cell(sign_in_row, 12).value:
            Attendance[username.lower()].update_cell(sign_out_row, sign_out_col, current_time)
            flag = 0
            sign_out_col = sign_out_col +3
            await message.channel.send("sign out acknowleged")

        else:
            await message.channel.send("kindly add tasks before signing out")

    elif user_message.lower() == '/show_today':
        if len(sign_out_array) > 0: 
            for i in range(len(sign_out_array)):
                today_timings = "/sign_in: " + sign_in_array[i-1]  + "/sign_out: " + sign_out_array[i-1] +'\n'
                await message.channel.send(today_timings)
            temp5 = "total duration today " +  Attendance[username.lower()].cell(sign_in_row, 11).value
            await message.channel.send(temp5)
        else:
            await message.channel.send("you have skipped sign in or sign out")

    else:
        await message.channel.send("invalid statement. write '/help' to get knowldge about commands")
  return
    
client.run(TOKEN)

