import google.generativeai as genai
import os
import sys
import re
from time import sleep
# print imports
from pyfiglet import Figlet
from rich.console import Console
from rich.prompt import Prompt
# prompt imports
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application.current import get_app
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.cursor_shapes import CursorShape, ModalCursorShapeConfig

# set model
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
#model = genai.GenerativeModel('models/gemini-pro')
chat = model.start_chat(history=[])

rconsole = Console()
keybindings = KeyBindings()

@keybindings.add('c-x')
def _(event):
    print(" Exit when `c-x` is pressed. ")
   

@keybindings.add('c-space')
def _(event):
    " Initialize autocompletion, or select the next completion. "
    buff = event.app.current_buffer
    if buff.complete_state:
        buff.complete_next()
    else:
        buff.start_completion(select_first=False)

@keybindings.add('f5')
def _(event):
	" Toggle between Emacs and Vi mode. "
	app = event.app

	if app.editing_mode == EditingMode.VI:
		app.editing_mode = EditingMode.EMACS
	else:
		app.editing_mode = EditingMode.VI
          

# cursor switching          
CURSORS = (
    CursorShape.UNDERLINE,
    CursorShape.BLINKING_UNDERLINE,
    CursorShape.BLOCK,
    CursorShape.BLINKING_BLOCK,
    CursorShape.BEAM,
    CursorShape.BLINKING_BEAM,
)
CURSOR_IDX=4
@keybindings.add('f6')
def _(event):
	global CURSOR_IDX, CURSORS
	CURSOR_IDX += 1 
	promptSession.cursor = CURSORS[CURSOR_IDX % len(CURSORS)]
            
             
# Add a toolbar at the bottom to display the current input mode.
def bottom_toolbar():
	" Display the current input mode. "
	edit_mode = 'Vi' if get_app().editing_mode == EditingMode.VI else 'Emacs'
	cursor = promptSession.cursor
	return [
		('class:toolbar', ' [F5] %s' % edit_mode),
		('class:toolbar', ' [F6] %s' % cursor)
	]


# regex
PATTERNS = [
	# * **Smart homes:**
	# (r"\* \*\*(.*?):\*\*", r"\t\1\n\t\n"), # h2

	# (r"\*\*(.*?):\*\*",   r"\t\t\1"), # h3
	
 	# **Some examples of IoT applications:**
	(r"\*\*(.*?):\*\*",    r"\n\1\n====================================\n\n") # h1 
]

def ask(text:str, stream:bool=False):
    
	response = model.generate_content(text, stream=stream)
	if stream:
		for chunk in response:
			print_colored_text(text=chunk.text, color="white")
	else:
		print_colored_text(text=response.text, color="white")
		

def run_chat(text:str, stream:bool=False):
	global chat
 
	try:	
		# Open Question prompt
		response = chat.send_message(text, stream=stream)
	except Exception as e:
		rconsole.print(f"[i]{e}[/i] :smiley:", style="bold red")
		return

	with rconsole.pager(): # .status("writing...", spinner="bouncingBall"):
		rconsole.print(Figlet(font="bigfig").renderText(f"Response: {len(chat.history) + 1}"), style="bold green")
		text = response.text
		for pattern, replacement in PATTERNS: # work on the text
			text = re.sub(pattern=pattern, repl=replacement, string=text)
			
		rconsole.print(response.text, style="bold white")
	

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


def is_empty(text:str):
	return not (len(text) == 0 or text.replace(" ", "") == "")


promptSession = None
def main():
    
    def prompt_continuation(width, line_number, is_soft_wrap):
        return ' ' * width
    	# Or: return [('', '.' * width)]
    
    word_completer = WordCompleter([
		"/go", '/exit', '/history', '/profile', '/help'
	])
    validator = Validator.from_callable(
								is_empty,
								error_message="Empty prompt ignored, Please say something",
								move_cursor_to_end=True
    )
    global promptSession
    promptSession = PromptSession(completer=word_completer,
                         	complete_while_typing=True,
                          	validator=validator,
							vi_mode=False,
							key_bindings=keybindings,
							bottom_toolbar=bottom_toolbar,
       						prompt_continuation=prompt_continuation,
							mouse_support=True,
							cursor=CursorShape.BLINKING_BEAM,
                          	# history=FileHistory('~/.ask_genai_history')
	)
 
 
if __name__=="__main__":
    
	main()	
	# Rules table
	print(Figlet().renderText("n j a d - AI"))
	rconsole.print("Welcome to njad-term-genai. this is a googles' gemini powered console app.",
                "Type your multi-line text in prompt below then press [i]Shift[/i] then [i]ENTER[/i].",
                "You can type [i][u]/help[/i][/u] to see useful commands.",
                  	style="bold magenta")

	while True:

		rconsole.print(Figlet(font="bigfig").renderText(f"Prompt: {len(chat.history)//2+1}"), style="bold green")
		try:
			# read multiline input: press Ctrl+D (UNIX), Ctrl+Z (windows) to set EOF (stop)
			# prompt = sys.stdin.read()
			# prompt = Prompt.ask(">")	
			text = promptSession.prompt(message="> ", multiline=True)
			
			# process prompt
			
			try:
				run_chat(text=text, stream=False)
			except Exception as e:
				rconsole(f"[red]Sorry, An Error Occured! [white][i]{e}[/i]", style="bold")

		except KeyboardInterrupt:
			print("Bye-bye.")
			exit(0)
