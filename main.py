import products
import store
import copy

MENU_DASH = """   ----------"""
MENU = f"""
   Store Menu
{MENU_DASH}
1. List all products in store
2. Show total amount in store
3. Make an order
4. Quit
"""

def page_title(title):
    """Print the title of the page."""
    print("")
    print(title)
    print(MENU_DASH)

def listen_input(text="Please choose a number: "):
    """Ask for input until it is empty or a valid integer, then return it."""
    print("")

    while True:
        choice = input(text)
        try:
            if choice != "":
                choice = int(choice)
            return choice
        except ValueError:
            print('Error with your choice! Try again! (empty to Quit)')

def list_products(item_list,title=""):
    """Return the given products; print them if a title is given."""
    if title != "":
        page_title(title)
    for number, product in enumerate(item_list, start=1):
        if title != "":
            print(f"    {number}. {product.name}, Price: {product.price:g}$, Quantity: {product.quantity}")
    return item_list

def show_shopping_list(shopping_list, title=""):
    """Print each product in the shopping list with its quantity."""
    if title != "":
        page_title(title)
    for number, item in enumerate(shopping_list, start=1):
        print(f"    {number}. {item[0].name}, Price: {item[0].price:g}$, Quantity: {item[1]}")

def show_total_amount(best_buy):
    """Print the total quantity of all products in the store."""
    page_title("Total Amount of Products:")
    print(f'    The Amount of all Products is: {best_buy.get_total_quantity()} Units in the Store')

def make_order(best_buy):
    """Ask the user for products and quantities, then place the order."""
    item_list = copy.deepcopy(best_buy.get_all_products())
    shopping_list = []
    choice = 0

    while choice != "":
        list_products(item_list,"Shop - Products:")
        print("")
        print("When you want to finish order, enter empty text.")

        product = None
        quantity = 0

        while product is None and choice != "":
            choice = listen_input("Which product # do you want? ")
            if choice != "":
                if choice in range(1, len(item_list) + 1):
                    product = item_list[choice - 1]
                    print(f"    {product.name}, Price: {product.price:g}$")
                else:
                    print(f'Invalid number: "{choice}", min: "1" max: "{len(item_list)}"')

        while quantity == 0 and choice != "":
            choice = listen_input("What amount do you want? ")
            if choice != "":
                if 1 <= choice <= product.quantity:
                    quantity = choice
                else:
                    print(f'Invalid quantity: "{choice}", min: "1" max: "{product.quantity}"')

        if product is not None and quantity != 0 and choice != "":
            for entry in shopping_list:
                if entry[0] == product:
                    entry[1] += quantity
                    break
            else:
                shopping_list.append([product, quantity])

            product.quantity -= quantity

            page_title("Product added to list!")

            show_shopping_list(shopping_list, "The Shopping List is:")

    print(MENU_DASH)
    print("")
    if not shopping_list:
        print("No products selected, order cancelled.")
        return
    else:
        print(f'Order made! Total payment: {best_buy.order(shopping_list):g}$')
    print("")

def start(best_buy):
    """Show the menu and handle the user's choice until they quit."""
    while True:
        print(MENU)
        choice = listen_input()

        if choice == 1:
            list_products(best_buy.get_all_products(),"The Product list ist:")
        elif choice == 2:
            show_total_amount(best_buy)
        elif choice == 3:
            make_order(best_buy)
        elif choice == 4:
            break

def main():
    # setup initial stock of inventory
    product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    products.Product("Google Pixel 7", price=500, quantity=250)
                    ]
    best_buy = store.Store(product_list)

    start(best_buy)

if __name__ == "__main__":
    main()