import json
from datetime import datetime


class InventorySystem:
    """A class to manage inventory system operations."""
    
    def __init__(self):
        """Initialize the inventory system with empty stock data."""
        self.stock_data = {}

    def add_item(self, item_name="default", quantity=0, logs=None):
        """Add items to inventory.
        
        Args:
            item_name (str): Name of the item to add
            quantity (int): Quantity to add
            logs (list, optional): List to store log messages
        
        Returns:
            bool: True if successful, False otherwise
        """
        if logs is None:
            logs = []
            
        if not item_name:
            print("Error: Item name cannot be empty")
            return False
            
        # Validate input types
        if not isinstance(item_name, str):
            print(f"Error: Item name must be a string, got {type(item_name).__name__}")
            return False
            
        if not isinstance(quantity, (int, float)):
            print(f"Error: Quantity must be a number, got {type(quantity).__name__}")
            return False
        
        try:
            self.stock_data[item_name] = self.stock_data.get(item_name, 0) + quantity
            logs.append(f"{datetime.now()}: Added {quantity} of {item_name}")
            return True
        except Exception as error:
            print(f"Error adding item: {error}")
            return False

    def remove_item(self, item_name, quantity):
        """Remove items from inventory.
        
        Args:
            item_name (str): Name of the item to remove
            quantity (int): Quantity to remove
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if item_name in self.stock_data:
                self.stock_data[item_name] -= quantity
                if self.stock_data[item_name] <= 0:
                    del self.stock_data[item_name]
                return True
            print(f"Item '{item_name}' not found in inventory")
            return False
        except (KeyError, TypeError, ValueError) as error:
            print(f"Error removing item: {error}")
            return False

    def get_quantity(self, item_name):
        """Get quantity of an item in inventory.
        
        Args:
            item_name (str): Name of the item
        
        Returns:
            int: Quantity in stock, 0 if item not found
        """
        return self.stock_data.get(item_name, 0)

    def load_data(self, file_path="inventory.json"):
        """Load inventory data from JSON file.
        
        Args:
            file_path (str): Path to the JSON file
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                self.stock_data = json.loads(file.read())
            return True
        except FileNotFoundError:
            print(f"Inventory file {file_path} not found. Starting with empty inventory.")
            return True  # Continue with empty inventory
        except (json.JSONDecodeError, PermissionError) as error:
            print(f"Error loading data: {error}")
            return False

    def save_data(self, file_path="inventory.json"):
        """Save inventory data to JSON file.
        
        Args:
            file_path (str): Path to the JSON file
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(json.dumps(self.stock_data, indent=2))
            return True
        except (IOError, PermissionError) as error:
            print(f"Error saving data: {error}")
            return False

    def print_data(self):
        """Print all items in inventory."""
        print("Items Report")
        if not self.stock_data:
            print("No items in inventory")
            return
            
        for item, quantity in self.stock_data.items():
            print(f"{item} -> {quantity}")

    def check_low_items(self, threshold=5):
        """Check for items with low stock.
        
        Args:
            threshold (int): Minimum quantity threshold
        
        Returns:
            list: Items below threshold
        """
        result = []
        for item, quantity in self.stock_data.items():
            if quantity < threshold:
                result.append(item)
        return result

    def get_all_items(self):
        """Get all items in inventory.
        
        Returns:
            dict: Copy of the stock data
        """
        return self.stock_data.copy()


def main():
    """Main function to demonstrate inventory system functionality."""
    inventory = InventorySystem()
    operation_logs = []
    
    # Test operations
    print("=== Testing Inventory System ===")
    
    # Valid operations
    inventory.add_item("apple", 10, operation_logs)
    inventory.add_item("banana", 5, operation_logs)
    inventory.add_item("orange", 8, operation_logs)
    
    # These should fail with helpful error messages
    inventory.add_item(123, "ten")  # invalid types
    inventory.add_item("", 5)  # empty item name
    inventory.add_item("grape", -2)  # negative quantity (allowed but logged)
    
    inventory.remove_item("apple", 3)
    inventory.remove_item("nonexistent", 1)  # item not in inventory
    
    print("Apple stock:", inventory.get_quantity("apple"))
    print("Banana stock:", inventory.get_quantity("banana"))
    print("Orange stock:", inventory.get_quantity("orange"))
    print("Low items (threshold=5):", inventory.check_low_items())
    
    # Save and load data
    if inventory.save_data():
        print("Data saved successfully")
    
    if inventory.load_data():
        print("Data loaded successfully")
    
    inventory.print_data()
    
    # Show operation logs
    print("\nOperation Logs:")
    for log in operation_logs:
        print(f"  - {log}")
    
    print("\n=== Inventory System Demo Completed ===")


if __name__ == "__main__":
    main()
