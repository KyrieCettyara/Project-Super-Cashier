from  sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import select
from prettytable import PrettyTable
from prettytable import from_db_cursor

list_item = []
engine = create_engine('sqlite:///transaction.db')

def create_table():
    
    conn = engine.connect()

    query = text("""CREATE TABLE IF NOT EXISTS transactions (
no_id INTEGER PRIMARY KEY AUTOINCREMENT,
nama_item VARCHAR(200),
jumlah_item integer,
harga float,
total_harga float,
diskon float,
harga_diskon float
)
""")
    conn.execute(query)
    query = text("""SELECT * FROM transactions""")
    results = conn.execute(query)
    for result in results:
        print(result)

    conn.close()

def insert_to_table():
    
    for item in list_item:

        list_to_dic = {
            'nama_item' : item[0], 
            'jumlah_item' : item[1], 
            'harga': item[2], 
            'total_harga': item[3], 
            'diskon': item[4], 
            'harga_diskon': item[5]
        }

        with engine.connect() as conn:
            sql = text(
            "INSERT INTO transactions(nama_item, jumlah_item, harga, total_harga, diskon, harga_diskon) VALUES (:nama_item, :jumlah_item, :harga, :total_harga, :diskon, :harga_diskon)"
            )
            conn.execute(sql, list_to_dic)
            conn.commit()
        conn.close()
        
    
        



def print_pesanan():
    table_view = PrettyTable()

    table_view.field_names = ["Nama Item", "Jumlah Item", "Harga/Item", "Total Harga"]
    
    for item in list_item:
        table_view.add_row([item[0], item[1], item[2], item[3]])
    
    print(table_view)


def check_diskon(total_harga):
    if((total_harga) >= float(200000)):
        diskon = total_harga * 0.05
        harga_diskon = total_harga * 0.95
        
        return diskon, harga_diskon
    
    elif((total_harga) >= 300000):
        diskon = total_harga * 0.06
        harga_diskon = total_harga * 0.94
        
        return diskon, harga_diskon
    
    elif((total_harga) >= 500000):
        diskon = total_harga * 0.07
        harga_diskon = total_harga * 0.93
        
        return diskon, harga_diskon
    else:
        diskon = total_harga * 0
        harga_diskon = total_harga * 1
        return diskon, harga_diskon


##function to add master item 
def add_item(item_name, item_qty, price_per_item):
    total_harga = item_qty * price_per_item

    #check if name is empty
    if(len(item_name) == 0):
        print("Nama barang tidak boleh kosong")
        menu()

    #check apakah item sudah terdaftar
    isExist = any(item_name.lower() 
                    in item[0].lower() 
                    for item in list_item) 

    if(isExist):
        print("\nItem sudah terdaftar")
    else:
        diskon, harga_diskon = check_diskon(total_harga)

        new_item = [item_name, item_qty, price_per_item, total_harga, diskon, harga_diskon ]
        list_item.append(new_item) 
        print_pesanan()
        
    menu()
              
    return list_item

##function to update name of an item  
def update_item_name(item_name, new_item_name):
    for item_list in list_item:
        if item_list[0] == item_name:
            item_list[0] = new_item_name
            print(f'''
item name: {item_list[0]}
item quantity: {item_list[1]}
item price: {item_list[2]}
''')

    menu()

    return list_item
    

##function to update qty of an item   
def update_item_qty(item_name, new_item_qty):
    for item_list in list_item:
        if item_list[0] == item_name:
            item_list[1] = new_item_qty
            print(f'''
item name: {item_list[0]}
item quantity: {item_list[1]}
item price: {item_list[2]}''')

    menu()

    return list_item

##function to update price of an item   
def update_item_price(item_name, new_item_price):
    for item_list in list_item:
        if item_list[0] == item_name:
            item_list[2] = new_item_price
            print(f'''
item name: {item_list[0]}
item quantity: {item_list[1]}
item price: {item_list[2]}''')

    menu()

    return list_item

##function to delete  an item   
def delete_item(item_name):
    for i in range(len(list_item)):
        if list_item[i][0] == item_name:
            popped_item = list_item.pop(i)
            print(popped_item)

    menu()
    return list_item
          


##function to reset an transaction 
def reset_transaction():
    reset = input("Are you sure you want to delete all item(Y/N): ")
    if reset == 'Y' :
        list_item.clear()
        menu()
    elif reset == 'N':
        menu()
    else :
        print("Invalid input. Enter Y (Yes) or N (No)")
        reset_transaction()

    return list_item

    
##function to check an transaction
def check_order():
    total_bayar = 0

    ##chack if item quantity and price is null or negatif
    check_item= any([int(item[1]) <= 0 or int(item[2]) <= 0 for item in list_item])

    if check_item:
        print("Terdapat data yang tidak benar. Silahkan check dan update pesanan Anda.\n\n")
        print_pesanan()
    else:
        print("Data pesanan sudah benar.\n\n")
        print_pesanan()


    menu()

    return list_item 

##function to check-out an transaction
def check_out():
    create_table()
    insert_to_table()
    print_pesanan()

    for item in list_item:
        total_bayar = total_bayar + item[5]

    table_view = PrettyTable()

    table_view.field_names = ["Nama Item", "Jumlah Item", "Harga/Item", "Total Harga", "Diskon", "Harga Diskon"]
    
    for item in list_item:
        table_view.add_row([item[0], item[1], item[2], item[3], item[4], item[5]])
    
    print(table_view)
    
    print(f"Total yang harus Dibayar: {total_bayar} ")

    

def menu():
    print('''
1. Add Item
2. Update Item Name
3. Update Item Quantity
4. Update Item Price
5. Delete Item
6. Reset Transaction
7. Check Order
8. Check Out Order
''')
    print("Selamat Datang di Toko")
    menu = input("Choose a menu: ")
    match menu:
        case "1":
            item_name = input("Enter the item name: ")
            item_qty = float(input("Enter the item quantity: ") or 0)
            item_price = float(input("Enter the item price: ") or 0)

            add_item(item_name,item_qty,item_price)

        case "2":
            item_name = input("Enter the item name: ")
            new_item_name = input("Enter the new item name: ")

            update_item_name(item_name, new_item_name)

        case "3":
            item_name = input("Enter the item name:")
            new_item_qty = input("Enter the new item quantity: ")

            update_item_qty(item_name, new_item_qty)

        case "4":
            item_name = input("Enter the item name:")
            new_item_price = input("Enter the new item price: ")


            update_item_price(item_name, new_item_price)

        case "5":
            item_name = input("Enter the item name you want to delete:")

            delete_item(item_name)

        case "6":
           reset_transaction()

        case "7":
            check_order()

        case "8":
            check_out()

        case _:
            print("Invalid input.")
    

menu()


    
    




    