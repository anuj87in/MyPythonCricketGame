from collections import deque

class InteractiveFridge:
    def __init__(self):
        self.cabinets = {'A': None, 'B': None, 'C': None}
        self.order = deque(['A', 'B', 'C'])  # order of cabinets by earliest accessed
        self.latest_accessed = None
        
        # Dictionary of available fridge items
        self.available_items = {
            1: "Fruits",
            2: "Vegetables",
            3: "Milk",
            4: "Eggs",
            5: "Cheese",
            6: "Yogurt",
            7: "Butter",
            8: "Juice",
            9: "Meat",
            10: "Fish",
            11: "Leftovers",
            12: "Chocolate",
            13: "Ice Cream",
            14: "Soda",
            15: "Water Bottles"
        }
    
    def store_item(self, item):
        """Store an item in the fridge using LRU policy"""
        # Find cabinets that are empty
        empty_cabinets = [cab for cab, val in self.cabinets.items() if val is None]
        
        if empty_cabinets:
            # Fill next empty cabinet in sequential order (A -> B -> C)
            for cab in ['A', 'B', 'C']:
                if cab in empty_cabinets:
                    self.cabinets[cab] = item
                    self.latest_accessed = cab
                    # Update order: move cabinet to the end as it is latest accessed
                    if cab in self.order:
                        self.order.remove(cab)
                    self.order.append(cab)
                    print(f"\n✓ Stored '{item}' in cabinet {cab}")
                    return
        else:
            # All cabinets full, overwrite earliest accessed cabinet
            earliest_cab = self.order.popleft()
            old_item = self.cabinets[earliest_cab]
            self.cabinets[earliest_cab] = item
            self.latest_accessed = earliest_cab
            # Update order again pushing this cabinet as latest accessed
            self.order.append(earliest_cab)
            print(f"\n⚠ All cabinets full! Replaced '{old_item}' in cabinet {earliest_cab} with '{item}'")
    
    def open_cabinet(self, cabinet_name):
        """Open a cabinet to see what's inside (user pulls out drawer)"""
        cabinet_name = cabinet_name.upper()
        if cabinet_name in self.cabinets:
            self.latest_accessed = cabinet_name
            # Update order for latest access
            if cabinet_name in self.order:
                self.order.remove(cabinet_name)
            self.order.append(cabinet_name)
            contents = self.cabinets[cabinet_name]
            
            print(f"\n🔍 Opening cabinet {cabinet_name}...")
            if contents is None:
                print(f"   Cabinet {cabinet_name} is EMPTY.")
            else:
                print(f"   Cabinet {cabinet_name} contains: {contents}")
        else:
            print("\n❌ Invalid cabinet name. Choose A, B, or C.")
    
    def show_cabinet_status(self):
        """Show which cabinets are occupied vs empty (without revealing contents)"""
        print("\n" + "="*50)
        print("FRIDGE STATUS (Cabinets Overview):")
        print("="*50)
        for cab in ['A', 'B', 'C']:
            status = "🟢 OCCUPIED" if self.cabinets[cab] is not None else "⚫ EMPTY"
            print(f" Cabinet {cab}: {status}")
        print("="*50)
    
    def display_available_items(self):
        """Display the menu of available items"""
        print("\n" + "="*50)
        print("AVAILABLE ITEMS TO STORE:")
        print("="*50)
        for key, item in self.available_items.items():
            print(f" {key:2d}. {item}")
        print("="*50)
    
    def run(self):
        """Main interactive menu loop"""
        print("\n" + "="*50)
        print("   WELCOME TO INTERACTIVE FRIDGE MANAGER")
        print("="*50)
        
        while True:
            print("\n" + "-"*50)
            print("MAIN MENU:")
            print("-"*50)
            print("1. Store an item in the fridge")
            print("2. Open a cabinet to see what's inside")
            print("3. View cabinet status (occupied/empty)")
            print("4. Exit")
            print("-"*50)
            
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == '1':
                # Store an item
                self.display_available_items()
                try:
                    item_choice = int(input("\nEnter the number of the item you want to store: ").strip())
                    if item_choice in self.available_items:
                        item_name = self.available_items[item_choice]
                        self.store_item(item_name)
                    else:
                        print("\n❌ Invalid item number. Please try again.")
                except ValueError:
                    print("\n❌ Invalid input. Please enter a number.")
            
            elif choice == '2':
                # Open a cabinet
                print("\nAvailable cabinets: A, B, C")
                cabinet = input("Which cabinet do you want to open? ").strip().upper()
                self.open_cabinet(cabinet)
            
            elif choice == '3':
                # Show cabinet status
                self.show_cabinet_status()
            
            elif choice == '4':
                # Exit
                print("\n" + "="*50)
                print("Thank you for using Interactive Fridge Manager!")
                print("="*50)
                break
            
            else:
                print("\n❌ Invalid choice. Please enter a number between 1 and 4.")


# Run the interactive fridge manager
if __name__ == "__main__":
    fridge = InteractiveFridge()
    fridge.run()

