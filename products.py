import math

class IsLowOnStock(Exception):
    """Raised when the requested quantity exceeds the available stock."""
    pass

class IsNotAvailable(ValueError):
    """Raised when trying to buy an inactive product."""
    pass

class NameIsInvalid(ValueError):
    """Raised when a Value not meet the name requirements."""
    pass

class NameTypeIsInvalid(TypeError):
    """Raised when a Type is not valid."""
    pass

class PriceIsInvalid(ValueError):
    """Raised when a Value not meet the name requirements."""
    pass

class PriceTypeIsInvalid(TypeError):
    """Raised when a Type is not valid."""
    pass

class QuantityIsInvalid(ValueError):
    """Raised when a Value not meet the name requirements."""
    pass

class QuantityTypeIsInvalid(TypeError):
    """Raised when a Type is not valid."""
    pass

class Product:
    """A product in the store with name, price, quantity and active status."""
    MAX_NAME_LENGTH = 50
    MIN_NAME_LENGTH = 3

    def __init__(self, name, price, quantity):
        self.set_name(name)
        self.set_price(price)
        self.active = True
        self.set_quantity(quantity)

    def __repr__(self):
        """Return a readable representation of the product."""
        return f'name={self.name}, price={self.price}, quantity={self.quantity}, active={self.active}'

    def __eq__(self, other):
        """Compare name (case-insensitive) and price for equality, ignoring quantity and active status."""
        return self.name.lower() == other.name.lower() and self.price == other.price

    def get_name(self):
        """Return the product name."""
        return self.name

    def set_name(self, name):
        """Set the product name after validation."""
        if self.is_name_valid(name):
            self.name = name
            return True
        else:
            return False

    def is_name_valid(self, name):
        """Check the name; raise NameTypeIsInvalid or NameIsInvalid if invalid."""
        requirements = f"""

                    Product Name Requirements:
                    - Must be a text string (not empty or only spaces/line breaks)
                    - Length must be between {self.MIN_NAME_LENGTH} and {self.MAX_NAME_LENGTH} characters
                    - Must contain at least one letter (cannot consist solely of numbers, spaces or special characters)
                    """
        if not isinstance(name, str):
            raise NameTypeIsInvalid(f'A name must be a string, "{type(name)}" is rejected' + requirements)

        temp_name = name.strip()

        if not temp_name:
            raise NameIsInvalid(f'A name with only Spaces or line breaks is not allowed, "{name}" is rejected' + requirements)

        if len(temp_name) < self.MIN_NAME_LENGTH or len(temp_name) > self.MAX_NAME_LENGTH:
            raise NameIsInvalid(f'A name must have a length from {self.MIN_NAME_LENGTH} to {self.MAX_NAME_LENGTH}, the name with the length "{len(temp_name)}" is rejected' + requirements)

        if not any(c.isalpha() for c in temp_name):
            raise NameIsInvalid(f'A name must contain at least one letter or number, "{name}" is rejected' + requirements)
        return True

    def get_price(self):
        """Return the product price."""
        return self.price

    def set_price(self, price):
        """Set the price after validation; ints are converted to float."""
        if self.is_price_valid(price):
            price = float(price)
            self.price = price
            return True
        else:
            return False

    def is_price_valid(self, price):
        """Check the price; raise PriceTypeIsInvalid or PriceIsInvalid if invalid."""
        requirements = f"""

                            Product Price Requirements:
                            - Must be a number, int will be converted to float.
                            - Must be >= 0 and finite (no NaN or Infinity).
                            """

        if isinstance(price, bool) or not isinstance(price, (int, float)):
            raise PriceTypeIsInvalid(f'Product price must be a number, "{type(price)}" is rejected' + requirements)
        else:
            price = float(price)

        if math.isnan(price) or math.isinf(price):
            raise PriceIsInvalid(F'Price cannot be NaN or Infinity, "{price}" is rejected')

        if not price >= 0:
            raise PriceIsInvalid(f'Product price must be >= 0, "{price}" is rejected' + requirements)
        return True

    def get_quantity(self):
        """Return the current stock quantity."""
        return self.quantity

    def set_quantity(self, quantity):
        """Set the quantity after validation; deactivate the product at 0."""
        if self.is_quantity_valid(quantity):
            self.quantity = int(round(quantity))
            if self.quantity == 0:
                self.deactivate()
            return True
        else:
            return False

    def reduce_quantity(self, quantity):
        """Reduce the stock by quantity; return False if not enough is in stock."""
        if self.get_quantity() >= quantity:
            new_quantity = self.get_quantity() - quantity
            self.set_quantity(new_quantity)
            return True
        else:
            return False

    def is_quantity_valid(self, quantity):
        """Check the quantity; raise QuantityTypeIsInvalid or QuantityIsInvalid if invalid."""
        requirements = f"""

                            Product Quantity Requirements:
                            - Must be a number, float will be round to int.
                            - Must be >= 0 and finite (no NaN or Infinity).
                            """

        if isinstance(quantity, bool) or not isinstance(quantity, (int, float)):
            raise QuantityTypeIsInvalid(f'Product quantity must be a number, "{type(quantity)}" is rejected' + requirements)

        if isinstance(quantity, float) and (math.isnan(quantity) or math.isinf(quantity)):
            raise QuantityIsInvalid(F'Quantity cannot be NaN or Infinity, "{quantity}" is rejected')

        if quantity < 0:
            raise QuantityIsInvalid(f'Product quantity must be >= 0, "{quantity}" is rejected' + requirements)
        return True

    def is_active(self):
        """Return True if the product is available for purchase."""
        return self.active

    def activate(self):
        """Mark the product as available."""
        self.active = True
        return self.active

    def deactivate(self):
        """Mark the product as unavailable."""
        self.active = False
        return self.active

    def show(self):
        """Return a description of the product as a string."""
        product_show = f'{self.name} costs {self.price} there are {self.quantity} units in stock, and it is currently {"available" if self.active else "unavailable"}'
        if __name__ == "__main__":
            print(product_show)
        return product_show

    def buy(self, quantity):
        """Buy the given quantity and return the total price as float.

        Raises IsNotAvailable if the product is inactive and
        IsLowOnStock if there is not enough stock.
        """
        if not self.is_active():
            raise IsNotAvailable(f'{self.name} it is currently unavailable')
        if self.is_quantity_valid(quantity):
            quantity = int(round(quantity))
            cost = quantity * self.get_price()
            if self.reduce_quantity(quantity):
                return cost
            else:
                raise IsLowOnStock(f'{quantity} units of {self.name} costs {cost} there are only {self.quantity} units in stock')

def main():
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)

    print(bose.buy(50))
    print(mac.buy(100))
    print(mac.is_active())

    bose.show()
    mac.show()

    bose.set_quantity(1000)
    bose.show()

if __name__ == "__main__":
    main()
