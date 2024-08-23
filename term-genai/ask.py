import google.generativeai as genai
import os
import sys
import re
from pyfiglet import Figlet

# set model
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
#model = genai.GenerativeModel('models/gemini-pro')

# regex
PATTERNS = [
	# * **Smart homes:**
	# (r"\* \*\*(.*?):\*\*", r"\t\1\n\t\n"), # h2

	# (r"\*\*(.*?):\*\*",   r"\t\t\1"), # h3
	
 	# **Some examples of IoT applications:**
	(r"\*\*(.*?):\*\*",    r"\n\1\n====================================\n\n") # h1 
]

def ask(prompt:str):
    
	response = model.generate_content(prompt, stream=True)
	for chunk in response:
		print(chunk.text)


def run_chat(prompt:str):
	response = chat.send_message(prompt, stream=True)

	for chunk in response:
		for pattern, replacement in PATTERNS:
			# match = re.search(pattern=pattern, string=chunk.text)
			# text = chunk.text			
			# if match:
			text = re.sub(pattern=pattern, repl=replacement, string=chunk.text)

			print_colored_text(text=text, color="white")
	

def print_colored_text(text, color):
    colors = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
    }

    print(colors[color] + text + "\033[0m")


if __name__=="__main__":
    
	# Rules table
	print(Figlet().renderText("n j a d - AI"))
	print_colored_text(color="green", text=
    "/--------------------------------------------\\\n"+
	"|(#) Please, type your muliline prompt below |\n"+
	"|   (-) press ENTER to create new line       |\n"+
	"|(*) Please, Use below commands:             |\n"+
	"|   (-) CTRL+D(UNIX) or CTRL+Z(DOS) to send  |\n"+
	"|       preferably press ENTER first         |\n"+
	"|   (-) CTRL+C  to quit                      |\n"+
	"\\-------------------------------------------/"
	)

	chat = model.start_chat(history=[])
	num=1
	while True:

		try:
			# Open Question prompt
			print_colored_text(text=Figlet(font="bigfig").renderText(f"Prompt #{num}"),
                      color="green")

			# read multiline input: press Ctrl+D (UNIX), Ctrl+Z (windows) to set EOF (stop)
			prompt = sys.stdin.read()

			if len(prompt) == 0:
				
				print_colored_text(color="green", text=
				"+-----------------------------------------------------+\n"+
				"|  Empty prompt ignored, Please say something (*_*)   |\n"+
				"+-----------------------------------------------------+\n"
				)
				continue
			
   			# Open Answer
			print_colored_text(text=Figlet(font="bigfig").renderText(f"Response #{num}"),
                      color="green")

			# process prompt
			run_chat(prompt=prompt)

			num += 1

		except KeyboardInterrupt:
      
			print("Bye-bye.")
			exit(0)