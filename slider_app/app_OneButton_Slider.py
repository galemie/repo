# Imports
import requests
import tkinter as tk
import tkinter.font as tkFont
import threading
import json

# Definitions

ip_adres_ha = "http://100.75.222.81:8123"
#ip_adres_ha = "homeassistant.local:8123"
target_entity_ids = [
    "switch.0x00124b00246caf6a",
    "switch.0x7cb03eaa0a0002cf",
    "light.0x001788010b307e9a",
    "light.0x84ba20fffe5ae4f8"
]

# API KEY function
def read_api_key(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config['api_key']

config_file = 'config.json'
ha_api_key = read_api_key(config_file)


# Functions
# Function turn on switches
def turn_on_switch(entity_id):
    headers = {
        "Authorization": f"Bearer {ha_api_key}",
        "Content-Type": "application/json",
    }
    url = f"{ip_adres_ha}/api/services/switch/turn_on"
    data = {"entity_id": entity_id}
    
    with requests.Session() as session:
        response = session.post(url, json=data, headers=headers)
    
    if response.ok:
        print(f"Switch {entity_id} turned on successfully")
    else:
        print(f"Error turning on switch {entity_id}")


# Function turn off switches
def turn_off_switch(entity_id):
    headers = {
        "Authorization": f"Bearer {ha_api_key}",
        "Content-Type": "application/json",
    }
    url = f"{ip_adres_ha}/api/services/switch/turn_off"
    data = {"entity_id": entity_id}
    
    with requests.Session() as session:
        response = session.post(url, json=data, headers=headers)
    
    if response.ok:
        print(f"Switch {entity_id} turned off successfully")
    else:
        print(f"Error turning off switch {entity_id}")


# Function turn on bulbs
def turn_on_entity(entity_id):
    headers = {
        "Authorization": f"Bearer {ha_api_key}",
        "Content-Type": "application/json",
    }
    url = f"{ip_adres_ha}/api/services/light/turn_on"
    data = {"entity_id": entity_id}
    
    with requests.Session() as session:
        response = session.post(url, json=data, headers=headers)
    
    if response.ok:
        print(f"Bulb {entity_id} turned on successfully")
    else:
        print(f"Error turning on bulb {entity_id}")
   

# Function turn off bulbs
def turn_off_entity(entity_id):
    headers = {
        "Authorization": f"Bearer {ha_api_key}",
        "Content-Type": "application/json",
    }
    url = f"{ip_adres_ha}/api/services/light/turn_off"
    data = {"entity_id": entity_id}
    
    with requests.Session() as session:
        response = session.post(url, json=data, headers=headers)
    
    if response.ok:
        print(f"Bulb {entity_id} turned off successfully")
    else:
        print(f"Error turning off bulb {entity_id}")

# Function all on
def all_on():
    for entity_id in target_entity_ids:
        if "switch" in entity_id:
            turn_on_switch(entity_id)
        elif "light" in entity_id:
            turn_on_entity(entity_id)

# Function all off
def all_off():
    for entity_id in target_entity_ids:
        if "switch" in entity_id:
            turn_off_switch(entity_id)
        elif "light" in entity_id:
            turn_off_entity(entity_id)

# Function to change brightness
def change_brightness(entity_id, brightness):
    headers = {
        "Authorization": f"Bearer {ha_api_key}",
        "Content-Type": "application/json",
    }
    url = f"{ip_adres_ha}/api/services/light/turn_on"
    data = {
        "entity_id": entity_id,
        "brightness": brightness
    }
    
    with requests.Session() as session:
        response = session.post(url, json=data, headers=headers)
    
    if response.ok:
        print(f"Brightness of {entity_id} changed to {brightness} successfully")
    else:
        print(f"Error changing brightness of {entity_id}")


# GUI elements
# Creating window
root = tk.Tk()
root.title("GUI - Switches and Bulbs")
root.configure(bg="white")

# Create a custom font and padding
custom_font = tkFont.Font(family="Arial", size=12,)
padding_x = 10
padding_y = 10

# Creating sliders
slider_1 = tk.Scale(root, from_=255, to=0, orient=tk.VERTICAL, length=240, sliderlength=45, width=45, command=lambda brightness: (change_brightness(target_entity_ids[2], int(brightness))))
slider_2 = tk.Scale(root, from_=255, to=0, orient=tk.VERTICAL, length=240, sliderlength=45, width=45, command=lambda brightness: (change_brightness(target_entity_ids[3], int(brightness))))

# Positioning sliders on the grid
slider_1.grid(row=1, column=2, padx=padding_x, pady=padding_y)
slider_2.grid(row=1, column=3, padx=padding_x, pady=padding_y)



# Function to fetch button names from external json file
def read_button_names(url):
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise Exception(f"Unable to fetch data from {url}. Status code: {response.status_code}")

url = "https://raw.githubusercontent.com/galemie/Json/main/button_names.json"
button_names = read_button_names(url)

button_1, button_2, button_3, button_4 = button_names.values()

# Functions
def toggle_entity(entity_id):
    headers = {
        "Authorization": f"Bearer {ha_api_key}",
        "Content-Type": "application/json",
    }
    url = f"{ip_adres_ha}/api/states/{entity_id}"
    response = requests.get(url, headers=headers)
    if response.ok:
        state = response.json()["state"]
        if state == "on":
            if "switch" in entity_id:
                turn_off_switch(entity_id)
            elif "light" in entity_id:
                turn_off_entity(entity_id)
        elif state == "off":
            if "switch" in entity_id:
                turn_on_switch(entity_id)
            elif "light" in entity_id:
                turn_on_entity(entity_id)

# Creating buttons
button_1 = tk.Button(root, text=button_1, font=custom_font, command=lambda: (toggle_entity(target_entity_ids[0]), update_button_color(target_entity_ids[0], button_1)), height=4, width=22)
button_2 = tk.Button(root, text=button_2, font=custom_font, command=lambda: (toggle_entity(target_entity_ids[1]), update_button_color(target_entity_ids[1], button_2)), height=4, width=22)
button_3 = tk.Button(root, text=button_3, font=custom_font, command=lambda: (toggle_entity(target_entity_ids[2]), update_button_color(target_entity_ids[2], button_3)), height=4, width=22)
button_4 = tk.Button(root, text=button_4, font=custom_font, command=lambda: (toggle_entity(target_entity_ids[3]), update_button_color(target_entity_ids[3], button_4)), height=4, width=22)

# Positioning buttons on the grid
button_1.grid(row=0, column=0, padx=padding_x, pady=padding_y)
button_2.grid(row=0, column=1, padx=padding_x, pady=padding_y)
button_3.grid(row=0, column=2, padx=padding_x, pady=padding_y)
button_4.grid(row=0, column=3, padx=padding_x, pady=padding_y)
# all_on_button.grid(row=0, column=4, padx=padding_x, pady=padding_y)
# all_off_button.grid(row=1, column=4, padx=padding_x, pady=padding_y)

# Function update button color
def update_button_color(entity_id, button):
    headers = {
        "Authorization": f"Bearer {ha_api_key}",
        "Content-Type": "application/json",
    }
    url = f"{ip_adres_ha}/api/states/{entity_id}"
    response = requests.get(url, headers=headers)
    if response.ok:
        state = response.json()["state"]
        if state == "on":
            button.configure(bg="green", fg="white")
        elif state == "off":
            button.configure(bg="red", fg="white")
    else:
        print(f"Error getting state for {entity_id}")

# Device status check
def check_device_state():
    update_button_color(target_entity_ids[0], button_1)
    update_button_color(target_entity_ids[1], button_2)
    update_button_color(target_entity_ids[2], button_3)
    update_button_color(target_entity_ids[3], button_4)
    root.after(500, check_device_state)

# Multithreading to avoid tread conflict
state_thread = threading.Thread(target=check_device_state)
state_thread.start()

# Running the application
root.mainloop()