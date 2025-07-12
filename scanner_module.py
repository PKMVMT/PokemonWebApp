import csv
from difflib import get_close_matches
import os
from PIL import Image

def load_vault(vault_path='vault.csv'):
    with open(vault_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def match_card(value, vault_rows):
    vault_entries = [f"{row['Name']} {row['Number']}" for row in vault_rows]
    number_entries = [row['Number'] for row in vault_rows]

    hits = get_close_matches(value, vault_entries, n=3, cutoff=0.3)
    if hits:
        name, number = hits[0].split(" ", 1)
    else:
        num_hits = get_close_matches(value, number_entries, n=1, cutoff=0.6)
        if num_hits:
            number = num_hits[0]
            row = next((r for r in vault_rows if r['Number'] == number), None)
            name = row['Name'] if row else None
        else:
            return None

    return next((row for row in vault_rows if row['Name'] == name and row['Number'] == number), None)

def preview_image(name, folder='static/images'):
    filename = f"{name}.jpg"
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        print(f"🖼 Previewing image: {filename}")
        img = Image.open(path)
        img.show()
    else:
        print(f"🚫 No image found for: {name}")

def add_to_inventory(card_data, quantity, log_path='inventory_log.csv'):
    exists = os.path.exists(log_path)
    with open(log_path, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Number', 'Set', 'Quantity']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not exists:
            writer.writeheader()
        writer.writerow({
            'Name': card_data['Name'],
            'Number': card_data['Number'],
            'Set': card_data['Set'],
            'Quantity': quantity
        })
    print(f"✔ Added {quantity}x {card_data['Name']} to inventory.")

def manual_entry(name, number, set_name, quantity):
    card_data = {'Name': name, 'Number': number, 'Set': set_name}
    add_to_inventory(card_data, quantity)