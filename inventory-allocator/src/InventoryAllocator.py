# -*- coding: utf-8 -*-
"""
Dylan Kuo
Deliverr recruiting exercise: Inventory Allocator
"""
from collections import defaultdict

class InventoryAllocator():
    """
    Inventory Allocator static class
    Contains the class method allocate(), which allocates the order based on the requirements.
    """
    
    @classmethod
    def allocate(cls, order, warehouses):
        '''  
        Allocates the best shipment for the order, given a list of inventories representing various warehouses.
        '''
        
        # Store a dictionary of warehouses to the dictionary of item quantity
        # that will be shipped
        item_inv_allocation = defaultdict( lambda: {} )
        
        # Iterate over every item-quantity pair in the order
        for item, quantity_remain in order.items():
            # Store a dicionary of warhouses to the quantity of item that will be allocated
            warehouses_for_item = {}
            
            # Iterative over warhouses from the cheapest to most expensive
            for warehouse in warehouses:
                warehouse_name = warehouse['name']
                warehouse_inv = warehouse['inventory']
                
                # Skip this warehouse if it doesn't contain any of 'item'
                if item not in warehouse_inv or warehouse_inv[item] < 1:
                    continue
                
                item_stock = warehouse_inv[item]
                
                # If there's at least enough stock to finish the order with this
                # warehouse, break out of the loop
                if quantity_remain <= item_stock:
                    warehouses_for_item[warehouse_name] = quantity_remain
                    quantity_remain = 0
                    break
                
                # If there's no enough of 'item', take all of its item stock 
                # and check the next warehouse for this item
                elif quantity_remain > item_stock:
                    warehouses_for_item[warehouse_name] = item_stock
                    quantity_remain -= item_stock
                    
            # If we cannot fulfill the order from all warehouses, an empty list 
            # will be returned representing that the order is cancelled and
            # no item will be shipped 
            if quantity_remain > 0:
                return []
            
            # Otherwise, add the item quantities per warehouse to our dictionary of warehouses
            for warehouse_name, item_quantity in warehouses_for_item.items():
                item_inv_allocation[warehouse_name][item] = item_quantity
                
        # Convert the dictionary to a list of one-key dictionary, as the format required by the problem
        output = [{name: items} for name, items in item_inv_allocation.items()]
        return output