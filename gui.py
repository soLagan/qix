import PySimpleGUI as sg


def setup_theme():
    sg.theme_background_color(color='#0EFFE9')  # Background Colour
    sg.set_options(element_padding=(5, 9), font=('Terminal',))  # Set font
    return None


def make_initial_window():
    # Create the layout
    layout_initial = [
        [sg.Text("WELCOME TO QIX", font='Terminal', size=(15, 3), pad=(330, 10), text_color='black',
                 background_color='#0EFFE9')],
        [sg.Text("Select Difficulty", font='Terminal', size=(30, 3), pad=(315, 10), text_color='black',
                 background_color='#0EFFE9')],
        [sg.Button("Easy", size=(15, 2), pad=(45, 10), button_color='#FF0E83'),
         sg.Button("Intermediate", size=(15, 2), pad=(45, 10), button_color='#FF0E83'),
         sg.Button("Insane", size=(15, 2), pad=(45, 10), button_color='#FF0E83')],
        [sg.Button("Exit", size=(15, 2), pad=(323, 50), button_color='#FF0E83')],

    ]

    # Create the window
    window_initial = sg.Window("QIX", layout_initial, margins=(230, 250), font='Terminal')

    # Return the window
    return window_initial


def render_initial_screen():
    # Create an event loop
    initial_window = make_initial_window()

    while True:
        event, values = initial_window.read()

        # End program if user closes window or
        # presses the EXIT button
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "Easy":
            print('Difficulty Selected: Easy')
        elif event == "Intermediate":
            print('Difficulty Selected: Intermediate')
        elif event == "Insane":
            print('Difficulty Selected: Insane')

    initial_window.close()
    return None


def make_game_over_window():
    # Create the layout
    layout_game_over = [
        [sg.Text("GAME OVER", font='Terminal', size=(15, 3), pad=(330, 10), text_color='black',
                 background_color='#0EFFE9')],
        [sg.Text("User Score: CONSTANT", font='Terminal', size=(30, 3), pad=(315, 10), text_color='black',
                 background_color='#0EFFE9')],
        [sg.Button("Restart", size=(15, 2), pad=(45, 10), button_color='#FF0E83')],
        [sg.Button("Exit", size=(15, 2), pad=(323, 50), button_color='#FF0E83')],

    ]

    # Create the window
    window_game_over = sg.Window("QIX", layout_game_over, margins=(230, 250), font='Terminal')

    # Return the window
    return window_game_over


def render_game_over_screen():
    # Boolean which checks whether to restart game or not
    restart = False
    game_over_window = make_game_over_window()

    # Create an event loop
    while True:
        event, values = game_over_window.read()

        # End program if user closes window or
        # presses the EXIT button
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "Restart":
            print('Restarting Game')
            restart = True
            break

    game_over_window.close()

    if restart:
        render_initial_screen()


if __name__ == "__main__":
    CHOICES = ['INITIAL', 'GAME_OVER']
    CHOICE = CHOICES[0]

    setup_theme()
    if CHOICE == "INITIAL":
        render_initial_screen()
    elif CHOICE == "GAME_OVER":
        render_game_over_screen()
