from  sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import select
from prettytable import PrettyTable
from prettytable import from_db_cursor

list_item = []
engine = create_engine('sqlite:///transactions.db')

def CheckIsEmpty(item_name):
    """
    Function untuk melakukan check nama item kosong.

    Parameter:
        nama_item (string): nama dari item.

    Returns:
        isEmpty (boolean): true jika nama item kosong.
    """
    isEmpty = False
    if(len(item_name) == 0):
        isEmpty = True
    
    return isEmpty



def CheckIsExist(item_name):
    """
    Function untuk melakukan check nama item ada di dalam list.

    Parameter:
        nama_item (string): nama dari item.

    Returns:
        isExist (boolean): true jika nama item ada dalam list.
    """
    isExist = False
    isExist = any(item_name.lower() 
                    in item[0].lower() 
                    for item in list_item) 
    
    return isExist


def create_table():
    """
    Function untuk men-create table transaction
    """
    
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

    conn.close()



def insert_to_table():
    """
    Function untuk memasukkan list transaksi ke dalam table transaction.
    """
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
    """
    Function untuk menampilkan pesanan yang ada di list.
    """
    table_view = PrettyTable()

    table_view.field_names = ["Nama Item", "Jumlah Item", "Harga/Item", "Total Harga"]
    
    for item in list_item:
        table_view.add_row([item[0], item[1], item[2], item[3]])
    
    print(table_view)


def check_diskon(total_harga):
    """
    Function untuk melakukan check diskon yang didapatkan oleh item.

    Parameter:
        total_harga (float): total harga per item (item quantity * item price).

    Returns:
        diskon (float): harga diskon yang didapatkan per item
        harga_diskon (float): total harga per item dikurangi diskon
    """
    if((total_harga) >= float(200000)):
        diskon = total_harga * 0.05
        harga_diskon = total_harga * 0.95
        
        return diskon, harga_diskon
    
    elif((total_harga) >= float(300000)):
        diskon = total_harga * 0.06
        harga_diskon = total_harga * 0.94
        
        return diskon, harga_diskon
    
    elif((total_harga) >= float(500000)):
        diskon = total_harga * 0.07
        harga_diskon = total_harga * 0.93
        
        return diskon, harga_diskon
    else:
        diskon = total_harga * 0
        harga_diskon = total_harga * 1
       
        return diskon, harga_diskon


def add_item(item_name, item_qty, price_per_item):
    """
    Function untuk menambahkan item kedalam list.

    Parameter:
        item_name (string): nama dari item.
        item_qty (float): quantity dari item
        price_per_item (float): harga unit dari item.

    Returns:
        list_item (list) = item yang sudah dimasukkan.
    """
    total_harga = item_qty * price_per_item

    isExist = CheckIsExist(item_name)
    IsEmpty = CheckIsEmpty(item_name)

    if (IsEmpty):
        print('\nNama item tidak boleh kosong')
    elif (isExist):
        print("\nItem sudah terdaftar")
    elif (not isExist and not IsEmpty):
        diskon, harga_diskon = check_diskon(total_harga)
        
        new_item = [item_name, item_qty, price_per_item, total_harga, diskon, harga_diskon ]
        list_item.append(new_item) 
        print_pesanan()
        
    menu()
              
    return list_item


def update_item_name(item_name, new_item_name):
    """
    Function untuk mengupdate nama dari item yang berada di list.

    Parameter:
        item_name (string): nama dari item.
        new_item_name (string): nama item yang baru.

    Returns:
        list_item (list) = item yang sudah dimasukkan.
    """

    isExist = CheckIsExist(item_name)
    IsEmpty = CheckIsEmpty(item_name)

    if (IsEmpty):
        print('\nNama item tidak boleh kosong')
    elif (not isExist):
        print("\nItem tidak ditemukan")
    elif (isExist and not IsEmpty):
        print("\nItem name berhasil diubah")
        for item_list in list_item:
            if item_list[0].lower()  == item_name.lower():
                item_list[0] = new_item_name
                print(f'''
item name: {item_list[0]}
item quantity: {item_list[1]}
item price: {item_list[2]}
''')

    menu()

    return list_item
    
 
def update_item_qty(item_name, new_item_qty):
    """
    Function untuk mengupdate quantity dari item yang berada di list.

    Parameter:
        item_name (string): nama dari item.
        new_item_qty (string): quantity item yang baru.

    Returns:
        list_item (list) = item yang sudah dimasukkan.
    """
    isExist = CheckIsExist(item_name)
    IsEmpty = CheckIsEmpty(item_name)

    if (IsEmpty):
        print('\nNama item tidak boleh kosong')
    elif (not isExist):
        print("\nItem tidak ditemukan")
    elif (isExist and not IsEmpty):
        print("\nItem quantity berhasil diubah")
        for item_list in list_item:
            if item_list[0] == item_name:
                item_list[1] = new_item_qty
                print(f'''
item name: {item_list[0]}
item quantity: {item_list[1]}
item price: {item_list[2]}''')
                
    menu()

    return list_item

  
def update_item_price(item_name, new_item_price):
    """
    Function untuk mengupdate unit price dari item yang berada di list.

    Parameter:
        item_name (string): nama dari item.
        new_item_price (string): unit price item yang baru.

    Returns:
        list_item (list) = item yang sudah dimasukkan.
    """
    isExist = CheckIsExist(item_name)
    IsEmpty = CheckIsEmpty(item_name)

    if (IsEmpty):
        print('\nNama item tidak boleh kosong')
    elif (not isExist):
        print("\nItem tidak ditemukan")
    elif (isExist and not IsEmpty):
        print("\nItem price berhasil diubah")
        for item_list in list_item:
            if item_list[0] == item_name:
                item_list[2] = new_item_price
                print(f'''
item name: {item_list[0]}
item quantity: {item_list[1]}
item price: {item_list[2]}''')
        
    menu()

    return list_item

   
def delete_item(item_name):
    """
    Function untuk menghapus item yang berada di list.

    Parameter:
        item_name (string): nama dari item.

    Returns:
        list_item (list) = item yang sudah dimasukkan.
    """
    popped_item = None
    for i in range(len(list_item)):
        if list_item[i][0] == item_name:
            popped_item = list_item.pop(i)
            print_pesanan()

    if (popped_item is None):
        print('Item tidak ditemukan.') 
               
    menu()
    return list_item
          


def reset_transaction():
    """
    Function untuk menghapus semua item yang berada di list.

    Returns:
        list_item (list) = item yang sudah dimasukkan.
    """
    reset = input("Are you sure you want to delete all item(Y/N): ")
    if reset.upper() == 'Y' :
        list_item.clear()
        print('Semua item berhasil dihapus.')
        menu()
    elif reset.upper() == 'N':
        menu()
    else :
        print("Invalid input. Enter Y (Yes) or N (No)")
        reset_transaction()
        

    return list_item


def check_order():
    """
    Function untuk menghapus semua item yang berada di list.

    Returns:
        list_item (list) = item yang sudah dimasukkan.
    """
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


def check_out():
    """
    Function untuk melakukan check-out terhadap item-item yang ada di list.
    """
    create_table()
    insert_to_table()

    total_bayar = 0.0

    for item in list_item:
        total_bayar = total_bayar + item[5]

    table_view = PrettyTable()

    table_view.field_names = ["Nama Item", "Jumlah Item", "Harga/Item", "Total Harga", "Diskon", "Harga Diskon"]
    
    for item in list_item:
        table_view.add_row([item[0], item[1], item[2], item[3], item[4], item[5]])
    
    print(table_view)
    
    print(f"Total yang harus Dibayar: RP. {total_bayar} ")

def leave():
    """
        Function untuk keluar dari menu.
    """
    print("""
    Anda telah keluar dari sistem. Terima kasih..
    """)
    

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
9. Leave
''')
    menu = input("Choose a menu: ")

    if(menu=='1'):
        item_name = input("Enter the item name: ")
        item_qty = float(input("Enter the item quantity: ") or 0)
        item_price = float(input("Enter the item price: ") or 0)

        add_item(item_name,item_qty,item_price)

    elif(menu=='2'):
        item_name = input("Enter the item name: ")
        new_item_name = input("Enter the new item name: ")

        update_item_name(item_name, new_item_name)

    elif(menu=='3'):
        item_name = input("Enter the item name:")
        new_item_qty = float(input("Enter the new item quantity: ") or 0)

        update_item_qty(item_name, new_item_qty)

    elif(menu=='4'):
        item_name = input("Enter the item name:")
        new_item_price = float(input("Enter the new item price: ") or 0)

        update_item_price(item_name, new_item_price)

    elif(menu=='5'):
        item_name = input("Enter the item name you want to delete:")

        delete_item(item_name)

    elif(menu=='6'):
        reset_transaction()

    elif(menu=='7'):
        check_order()

    elif(menu=='8'):
        check_out()

    elif(menu=='9'):
        leave()
    # masukkan yang user berikan selain yang tersedia 1-9
    else:
        menu()
    

menu()


    
    




    