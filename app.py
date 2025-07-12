from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)

def load_cards():
    with open('PokemonCards.csv', mode='r', encoding='utf-8') as file:
        return list(csv.DictReader(file))

def save_cards(cards):
    with open('PokemonCards.csv', mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['Name','Set','Condition','Rarity','EstimatedValue','Quantity','FoilType']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cards)

def log_sale_to_history(sale):
    with open('sales_history.csv', mode='a', newline='', encoding='utf-8') as file:
        fieldnames = ['Name', 'Quantity', 'Price', 'PackagingUsed']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(sale)

def load_packaging():
    with open('shipping_inventory.csv', mode='r', encoding='utf-8') as file:
        return list(csv.DictReader(file))

def save_packaging(items):
    with open('shipping_inventory.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Item','Quantity'])
        writer.writeheader()
        writer.writerows(items)

@app.route('/')
def dashboard():
    return render_template('dashboard.html',
        cards=load_cards(),
        packaging=load_packaging())

@app.route('/log_sale', methods=['POST'])
def log_sale():
    name = request.form['name'].strip()
    quantity = int(request.form['quantity'])
    price = request.form['price'].strip()
    packaging_used = request.form['packaging'].strip()

    cards = load_cards()
    for card in cards:
        if card['Name'].lower() == name.lower():
            current_qty = int(card['Quantity'])
            if current_qty >= quantity:
                card['Quantity'] = str(current_qty - quantity)
                break
    save_cards(cards)

    packages = load_packaging()
    for item in packages:
        if item['Item'].lower() == packaging_used.lower():
            qty = int(item['Quantity'])
            if qty > 0:
                item['Quantity'] = str(qty - 1)
                break
    save_packaging(packages)

    log_sale_to_history({
        'Name': name,
        'Quantity': quantity,
        'Price': price,
        'PackagingUsed': packaging_used
    })

    return redirect('/')

@app.route('/restock', methods=['POST'])
def restock():
    item = request.form['restock_item'].strip()
    amount = int(request.form['restock_amount'])

    packages = load_packaging()
    for p in packages:
        if p['Item'].lower() == item.lower():
            p['Quantity'] = str(int(p['Quantity']) + amount)
            break
    save_packaging(packages)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)