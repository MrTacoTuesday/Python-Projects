from time import sleep
from replit import clear
from version import version, release, author, username

clear()
print(f'''
	
 
 	\33[1;2mCreated by {author}\33[0m

 
''')
sleep(2)
clear()
sleep(0.3)
print(f'''
	
 
 	\33[1;2mVersion {version}, Release {release} \33[0m

 
''')
sleep(2)
clear()
sleep(0.3)
print('''
	
 
 	\33[1;35mTemperature Statistics\33[0m

 
''')
sleep(2.5)
print("   ", "---" * 18)
sleep(0.5)
print(''' 
	
 	A program that takes provided high and low temperature 
	data for a given place and calculates basic statistics
 	with them.

  	The console outputs the high/low data by day and then 
   	shows the calculated values afterwards.

 	There is an example function that tests temperature
  	across 10 days in Evans, Georgia and can be called by
    typing \33[3;35mexample\33[1;2;34m()\33[0m in the console.

 	To test your own data, use the \33[3;35mrun\33[1;2;34m()\33[0m function in the 
  	console. The \33[3;35mexit\33[1;2;34m()\33[0m function and \33[3;35mexit\33[0m command exit 
   	the program.

   	
''')
sleep(5)
input("\t\t\t<<<  PRESS ENTER TO CONTINUE  >>>\n\n\n")
sleep(0.5)
clear()
clear()


def out():
	print(f'''
	
 
 	Thank you for trying v{version} of \33[1;3;35mTemperature Statistics\33[0m!

  	This program was made by \33[3m{author}\33[0m for the 
   	\33[1;3mCreate Task\33[0m portion of the \33[1m2023 AP Computer 
	Science Principles Exam\33[0m and can be found at:
 	\33[4;34mhttps://replit.com/{username}/Temperature-Statistics#\33[0m

 
	''')
	sleep(8)
