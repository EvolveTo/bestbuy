from products import Product

class Store:
    def __init__(self,products:list[Product]):
        self.products :list[Product] = products.copy()

    def add_product(self, product:Product | list[Product] ):
        """add a product to the store"""
        if isinstance(product, Product):
            self.products.append(product)
        else:
            for item in product:
                self.products.append(item)

    def remove_product(self, product):
        """Remove a product by Product, Product Name or Iterator in the Group from the Product list"""
        if isinstance(product, str):
            found = next((item for item in self.products if item.name == product), None)
            if found is not None:
                try:
                    self.products.remove(found)
                except ValueError:
                    return False
            return True

        elif isinstance(product, Product):
            try:
                self.products.remove(product)
            except ValueError:
                return False
            return True

        elif isinstance(product, int):
            try:
                del self.products[product]
            except ValueError:
                return False
            return True
        return False

    def get_total_quantity(self):
        """return the total quantity of the store as an int"""
        total_quantity = 0

        for item in self.products:
            if item.is_active():
                total_quantity += item.quantity
        return int(total_quantity)

    def get_all_products(self):
        """return all activ products as a List[Product]"""
        activ_products = []
        for item in self.products:
            if item.is_active():
                activ_products.append(item)
        return activ_products

    def get_all_all_products(self):
        """return all products as a List[Product]"""
        all_products = []
        for item in self.products:
            all_products.append(item)
        return all_products

    def order(self,shopping_list):
        """contain a list of tulp [(product, order_quantity)] with the shopping list, and return the total cost as fload"""
        cost = 0
        for product, quantity in shopping_list:
            index = self.products.index(product)
            cost += self.products[index].buy(quantity)
        return cost

def main():

    product_list = [Product("MacBook Air M2", price=1450, quantity=100),
                    Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    Product("Google Pixel 7", price=500, quantity=250),
                    ]

    best_buy = Store(product_list)
    products = best_buy.get_all_products()
    print(best_buy.get_total_quantity())
    print(best_buy.order([(products[0], 1), (products[1], 2)]))

if __name__ == "__main__":
    main()
