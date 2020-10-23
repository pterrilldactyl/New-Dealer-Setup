import PySimpleGUI as sg
from json import (load as jsonload, dump as jsondump)
from os import path


DEALER_FILE = path.join(path.dirname(__file__), r'dealer_file.cfg') #links file location
DEALER_INFO_KEYS_TO_ELEMENT_KEYS = {'name': '-DEALER NAME-', 'aor': '-AOR-', 'daa': '-DAA-', 'agentagreement': '-AA-', 'implementation': '-IMP-'}
DEFAULT_DEALER = {'name': 'MenuSys', 'aor': 'N/A', 'daa': 'N/A', 'agentagreement': 'N/A', 'implementation': 'N/A'}
DEFAULT_DEALER_LIST = {}
DEFAULT_DEALER_LIST['MenuSys'] = DEFAULT_DEALER
#### Loading and Saving files ####
def load_info(dealer_file, default_dealer):
    try:
        with open(dealer_file, 'r') as f:
            dealer = jsonload(f)
    except Exception as e:
        sg.popup_quick_message(f'exception {e}', 'No dealer file found... creating new file', keep_on_top=True, background_color='red', text_color='white')
        dealer = default_dealer
        save_info(dealer_file, dealer, None)
    return dealer

def save_info(dealer_file, dealer, values):
    if values:  #Checking if the window has information
        for key in DEALER_INFO_KEYS_TO_ELEMENT_KEYS:
            try:
                print(key)
                dealer[key][DEALER_INFO_KEYS_TO_ELEMENT_KEYS[key]] = values[DEALER_INFO_KEYS_TO_ELEMENT_KEYS[key]]
            except Exception as e:
                print(f'Problem updating dealer info from window values.  Key = {key}')

    with open(dealer_file, 'w') as f:
        jsondump(dealer, f)

    sg.popup('Saved')

def add_dealer(dealer_file, dealer, values):
    if values:  #Checking if the window has information
        for key in DEALER_INFO_KEYS_TO_ELEMENT_KEYS:
            try:
                dealer[key] = values[DEALER_INFO_KEYS_TO_ELEMENT_KEYS[key]]
            except Exception as e:
                print(f'Problem updating dealer info from window values.  Key = {key}')

    with open(dealer_file, 'a') as f:
        jsondump(dealer, f)

    sg.popup('Saved')

#### Make the dealer info window ####
def create_dealer_window(dealer):
    #sg.theme(load_info(DEALER_FILE, DEFAULT_DEALER, DEALER_INFO_KEYS_TO_ELEMENT_KEYS)['theme'])

    col_layout = [[sg.T('Dealer: ', size=(20,1)), sg.T('Agent of Record', size=(20,1)), sg.T('DAA', size=(20,1)), sg.T('Agency Agreement', size=(20,1)), sg.T('Implementation', size=(20,1))],
                [sg.Input(size=(20,1), k='-DEALER NAME-'), sg.Input(size=(20,1), k='-AOR-'), sg.Input(size=(20,1), k='-DAA-'), sg.Input(size=(20,1), k='-AA-'), sg.Input(size=(20,1), k='-IMP-')]]
    column = sg.Column(col_layout)
    layout = [[sg.T('Dealer Setup', justification='center')],
              [sg.T('Here is where we will keep track of dealer setup information.', justification='right')],
              [column],
              [sg.B('New'), sg.B('Save'), sg.B('Exit')]]
    window = sg.Window('Settings', layout, keep_on_top=True, finalize=True)
    for key in DEALER_INFO_KEYS_TO_ELEMENT_KEYS:   # update window with the values read from dealer file
        #print(key)
        try:
            window[DEALER_INFO_KEYS_TO_ELEMENT_KEYS[key]].update(value=dealer[key])
        except Exception as e:
            print(f'Problem updating window from settings. Key = {key}')


    return window

def create_main_window(dealer):
    #sg.theme(load_info(DEALER_FILE, DEFAULT_DEALER, DEALER_INFO_KEYS_TO_ELEMENT_KEYS)['theme'])
    key_list = []
    for key in DEFAULT_DEALER_LIST:
        key_list.append(key)
    col_layout = [[sg.T('Dealer Name: ', size=(20,1)), sg.Input(size=(20,1), k='-DEALER NAME-')], 
                    [sg.T('Agent of Record:', size=(20,1)), sg.Input(size=(20,1), k='-AOR-')],
                    [sg.T('DAA:', size=(20,1)),sg.Input(size=(20,1), k='-DAA-')],
                    [sg.T('Agency Agreement:', size=(20,1)), sg.Input(size=(20,1), k='-AA-')],
                    [sg.T('Implementation:', size=(20,1)), sg.Input(size=(20,1), k='-IMP-')]]

    column = sg.Column(col_layout, k='-INFO-')
    layout = [[sg.T('Dealer Setup', justification='center')],
              [sg.T('Here is where we will keep track of dealer setup information.', justification='right')],
              [column, sg.Listbox(key_list, k='-DEALER NAME LIST-', size=(20,len(key_list)), enable_events=True)],
              [sg.B('Save'), sg.B('New Dealer'), sg.B('Exit'), sg.B('Dealer Info')]]
    window = sg.Window('Dealer Setup', layout, finalize=True)
    for key in DEALER_INFO_KEYS_TO_ELEMENT_KEYS:   # update window with the values read from dealer file
        #print(key)
        try:
            window[DEALER_INFO_KEYS_TO_ELEMENT_KEYS[key]].update(value=dealer[key])
            
        except Exception as e:
            print(f'Problem updating PySimpleGUI window from settings. KEY = {key}')
    return window

def main():
    window, dealer, lst_of_dealers = None, load_info(DEALER_FILE, DEFAULT_DEALER_LIST), load_info(DEALER_FILE, DEFAULT_DEALER_LIST)
    #Window Loop
    while True:
        if window is None: #Makes a window if there is no window
            window = create_main_window(dealer)
        event, values = window.read()

        if event: #this is merely for debugging purposes
            print(event, values)

        if event in (sg.WINDOW_CLOSED, 'Exit'): #Closes the window
            break

        elif event == 'Save': #For saving the overall file when editing an existing dealer
            window.close()
            window = None
            save_info(DEALER_FILE, lst_of_dealers, values)

        elif event == 'Dealer Info':  #Brings up a Dealer info popup. Will probably not actually use
            event, values = create_dealer_window(dealer).read(close=True)

            if event in ('Save', 'Exit'):
                window.close()
                window = None
                save_info(DEALER_FILE, dealer, values)

        elif event == '-DEALER NAME LIST-':  #This is supposed to update the Input boxes with the relevant dealer info
            window['-INFO-'].update()

        elif event == 'New Dealer': #I want this to append a newly added dealer to the end of the config dictionary
            print(dealer, values)
            add_dealer(DEALER_FILE, dealer, values)

    window.close(); del window
main()