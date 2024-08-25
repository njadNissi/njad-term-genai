from time import sleep

from rich import print as rprint
# rprint("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())

from rich.console import Console
console = Console()
# console.print("Hello", "World", style="bold red")
console.print(":vampire:Where there is a [bold cyan]Will[/bold cyan] there [u]is[/u] a [i]way[/i].")

from rich import inspect
my_list = ["foo", "bar"]
# inspect(my_list, methods=True)


def table_live():
    import time
    from rich.live import Live
    from rich.table import Table

    table = Table()
    table.add_column("Row ID")
    table.add_column("Description")
    table.add_column("Level")

    with Live(table, refresh_per_second=4):  # update 4 times a second to feel fluid
        for row in range(12):
            time.sleep(0.4)  # arbitrary delay
            # update the renderable internally
            if row % 4 == 0:
                table.add_row(f"{row}", f"description {row}", "[red]ERROR")
            else:
                table.add_row(f"{row}", f"description {row}", "[green]SUCCESS")
    

def test_live_table():
    import random
    import time

    from rich.live import Live
    from rich.table import Table


    def generate_table() -> Table:
        """Make a new table."""
        table = Table()
        table.add_column("ID")
        table.add_column("Value")
        table.add_column("Status")

        for row in range(random.randint(2, 6)):
            value = random.random() * 100
            table.add_row(
                f"{row}", f"{value:3.2f}", "[red]ERROR" if value < 50 else "[green]SUCCESS"
            )
        return table


    with Live(generate_table(), refresh_per_second=4) as live:
        for _ in range(40):
            time.sleep(0.4)
            live.update(generate_table())


def test_prompt():
    from rich.prompt import Prompt
    name = Prompt.ask("Enter your name", choices=["Paul", "Jessica", "Duncan"], default="Paul")
     

def test_screen():
    from rich.align import Align
    from rich.text import Text
    from rich.panel import Panel


    with console.screen(style="bold white on red") as screen:
        for count in range(5, 0, -1):
            text = Align.center(
                Text.from_markup(f"[blink]Don't Panic![/blink]\n{count}", justify="center"),
                vertical="middle",
            )
            screen.update(Panel(text))
            sleep(1)

if __name__=="__main__":   
    # table_live()
    # test_live_table()
    # test_prompt()

    # with console.status("Working..."):
    #     for _ in range(100):
    #         sleep(.1)        
    #         print("Njad", end='\r')


    # from rich.console import Console
    # blue_console = Console(style="white on blue")
    # blue_console.print("I'm blue. Da ba dee da ba di.")

    pass