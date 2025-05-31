from dao.OrderProcessorRepositoryImpl import OrderProcessorRepositoryImpl
from entity.customers import Customers
from entity.products import Products
from myexceptions.CustomerNotFoundException import CustomerNotFoundException
from myexceptions.ProductNotFoundException import ProductNotFoundException
from myexceptions.OrderNotFoundException import OrderNotFoundException

def main():
    service = OrderProcessorRepositoryImpl()

    while True:
        try:
            print("\n--- E-Commerce App Menu ---")
            print("1. Register Customer")
            print("2. Create Product")
            print("3. Delete Product")
            print("4. Add to Cart")
            print("5. View Cart")
            print("6. Place Order")
            print("7. View Customer Orders")
            print("0. Exit")
        
            choice = input("Enter your choice: ")

        
            if choice == '1':
                name = input("Enter customer name: ")
                email = input("Enter email: ")
                password = input("Enter password: ")
                customer = Customers(name=name, email=email, password=password)
                if service.create_customer(customer):
                    print("Customer registered successfully.")
                else:
                    print("Customer registration failed.")

            elif choice == '2':
                name = input("Enter product name: ")
                price = float(input("Enter price: "))
                description = input("Enter description: ")
                stock = int(input("Enter stock quantity: "))
                product = Products(name=name, price=price, description=description, stockQuantity=stock)
                if service.create_product(product):
                    print("Product created successfully.")
                else:
                    print("Product creation failed.")

            elif choice == '3':
                product_id = int(input("Enter product ID to delete: "))
                if service.delete_product(product_id):
                    print("Product deleted successfully.")
                else:
                    print("Product deletion failed.")

            elif choice == '4':
                customer_id = int(input("Enter customer ID: "))
                product_id = int(input("Enter product ID: "))
                quantity = int(input("Enter quantity: "))
                customer = Customers(customer_id=customer_id)
                product = Products(product_id=product_id)
                if service.add_to_cart(customer, product, quantity):
                    print("Product added to cart.")
                else:
                    print("Failed to add to cart.")

            elif choice == '5':
                customer_id = int(input("Enter customer ID to view cart: "))
                customer = Customers(customer_id=customer_id)
                cart_items = service.get_all_from_cart(customer)
                if cart_items:
                    print("Cart Items:")
                    for item in cart_items:
                        print(f"{item.name} | Price: {item.price} | Description: {item.description}")
                else:
                    print("Cart is empty.")

            elif choice == '6':
                customer_id = int(input("Enter customer ID: "))
                customer = Customers(customer_id=customer_id)

                num_items = int(input("How many items to order? "))
                order_items = {}

                for _ in range(num_items):
                    product_id = int(input("Enter product ID: "))
                    quantity = int(input("Enter quantity: "))

                    try:
                        # Get full product info including price
                        product = service.get_product_by_id(product_id)
                        if product in order_items:
                            order_items[product] += quantity
                        else:
                            order_items[product] = quantity
                    except ProductNotFoundException as e:
                        print(f"Error: {e}")

                address = input("Enter shipping address: ")

                if service.place_order(customer, order_items, address):
                    print("Order placed successfully.")
                else:
                    print("Order failed.")

            elif choice == '7':
                customer_id = int(input("Enter customer ID to view orders: "))
                try:
                    orders = service.get_orders_by_customer(customer_id)
                    if orders:
                        print("Customer Orders:")
                        for i, order in enumerate(orders, start=1):
                            print(f"\nOrder {i}:")
                            for product, quantity in order.items():
                                print(f"Product: {product.name}, Price: {product.price}, Qty: {quantity}")
                    else:
                        print("No orders found.")
                except OrderNotFoundException as e:
                    print(f"Error: {e}")
                
            elif choice == '0':
                print("Exiting the application. Goodbye!")
                break


        except CustomerNotFoundException as e:
            print(f"Error: {e}")
        except ProductNotFoundException as e:
            print(f"Error: {e}")
        except OrderNotFoundException as e:
            print(f"Error: {e}")
        except ValueError:
            print("Invalid input. Please enter valid data.")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
