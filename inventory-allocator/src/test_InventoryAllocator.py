# -*- coding: utf-8 -*-
"""
Dylan Kuo
Deliverr recruiting exercise: inventory allocator tests
"""

import unittest
from InventoryAllocator import InventoryAllocator

class test_InventoryAllocator(unittest.TestCase):
    """
    Unit test class to test InventoryAllocator.allocate
    """

    def _get_warehouse_name(self, warehouse):
        """
        Given the warehouse dictionary of an output `warehouse`, returns its name.
        """

        # Assuming well-formed output, the name should be the only key in the dict
        # Save on space and use iterator to get this rather than converting to a list
        name = next( iter( warehouse.keys() ) )
        return name

    def _find_warehouse_in_list_by_name(self, warehouse_name, warehouses):
        """
        Searches for a warehouse in `warehouses` with the name `warehouse_name`.
        Returns the warehouse object, or None if there is no match.
        """
        
        for warehouse in warehouses:
            other_name = self._get_warehouse_name(warehouse)
            if warehouse_name == other_name:
                return warehouse
            
        return None

    def _compare_shipments(self, expected_shipment, output_shipment):
        """
        Compares two shipments `expected` and `output`.
        Returns True if the shipments are equivalent, otherwise False.
        """

        # Compare lengths of shipments
        if len(expected_shipment) != len(output_shipment):
            return False

        # Compare warehouses and quantities between the two shipments
        for expected_warehouse in expected_shipment:
            warehouse_name = self._get_warehouse_name(expected_warehouse)

            # Check that expected warehouse exists in the output shipment
            output_warehouse = \
                self._find_warehouse_in_list_by_name(warehouse_name, output_shipment)
            
            if output_warehouse == None:
                return False

            # Check that warehouses will ship the same items
            expected_items = expected_warehouse[warehouse_name]
            output_items = output_warehouse[warehouse_name]
            if expected_items.keys() != output_items.keys():
                return False
            
            # Compare item quantities
            for item, expected_quantity in expected_items.items():
                output_quantity = output_items[item]
                if expected_quantity != output_quantity:
                    return False

        # All comparisons are done and the shipments should be equivalent.
        return True



    def test_well_formed_output(self):
        """
        Tests that InventoryAllocator.allocate can produce a well-formed output.
        """

        order = { "apple": 1 }
        inventory = [
            { "name": "owd", "inventory": { "apple": 1 } }
        ]
        output = InventoryAllocator.allocate(order, inventory)

        # Check that the output is a list, representing the allocation
        self.assertIsInstance(output, list)

        # Check that the allocation's first element is a dict of length 1,
        # representing a warehouse
        self.assertTrue(len(output) > 0)
        self.assertIsInstance(output[0], dict)
        self.assertEqual(len(output[0]), 1)

        # Check that the warehouse dict's key is its name, and that its value is a dict,
        # representing its inventory to be shipped from that warehouse
        self.assertIn("owd", output[0])
        self.assertIsInstance(output[0]["owd"], dict)

        # Check that the inventory dict's key is an item, and that its value is an int
        self.assertTrue(len(output[0]["owd"]) > 0)
        self.assertIn("apple", output[0]["owd"])
        self.assertIsInstance(output[0]["owd"]["apple"], int)


    def test_exact_match(self):
        """
        Tests that an order for a particular item can be fulfilled if a warehouse has
        the exact quantity needed.
        """

        order = { "apple": 3 }
        inventory = [
            { "name": "owd", "inventory": { "apple": 3 } }
        ]
        expected = [
            { "owd": { "apple": 3 } }
        ]

        output = InventoryAllocator.allocate(order, inventory)
        self.assertTrue(self._compare_shipments(expected, output))

    def test_exact_match_multiple_items(self):
        """
        Tests that an order for a particular item can be fulfilled if several warehouses
        has the exact quantity needed.
        """

        order = { "banana": 6, "orange": 2, "apple": 3 }
        inventory = [
            { "name": "owd", "inventory": { "apple": 3, "banana": 6 } },
            { "name": "dm",  "inventory": { "orange": 2 } }
        ]
        expected = [
            { "owd": { "apple": 3, "banana": 6 } },
            { "dm":  { "orange": 2 } }
        ]

        output = InventoryAllocator.allocate(order, inventory)
        self.assertTrue(self._compare_shipments(expected, output))

    
    def test_warehouse_precedence(self):
        """
        Tests that an order for a particular item will be fulfilled using the cheapest
        warehouse even if other ones have enough inventory, and that only the requested
        quantity will be shipped.
        """

        order = { "apple": 3 }
        inventory = [
            { "name": "owd", "inventory": { "apple": 5 } },
            { "name": "dm",  "inventory": { "apple": 3 } },
            { "name": "pnw", "inventory": { "apple": 6 } },
            { "name": "lmi", "inventory": { "apple": 1 } }
        ]
        expected = [
            { "owd": { "apple": 3 } }
        ]

        output = InventoryAllocator.allocate(order, inventory)
        self.assertTrue(self._compare_shipments(expected, output))

    
    def test_split_across_warehouses(self):
        """
        Tests that when an order can be fulfilled for an item but no single warehouse
        has enough, the shipment correctly gets the right quantity from each warehouse.
        """

        order = { "apple": 10 }
        inventory = [
            { "name": "owd", "inventory": { "apple": 0 } },
            { "name": "dm",  "inventory": { "apple": 6 } },
            { "name": "pnw", "inventory": { "apple": 12 } }
        ]
        expected = [
            { "dm":  { "apple": 6 } },
            { "pnw": { "apple": 4 } }
        ]

        output = InventoryAllocator.allocate(order, inventory)
        self.assertTrue(self._compare_shipments(expected, output))

    def test_split_multiple_items_across_warehouses(self):
        """
        Tests that when an order can be fulfilled for many items but no single warehouse
        has enough, the shipment correctly gets the right quantities from each warehouse.
        """

        order = { "apple": 10, "orange": 1, "banana": 7, "pear": 0 }
        inventory = [
            { "name": "owd", "inventory": { "banana": 2 } },
            { "name": "dm",  "inventory": { "apple": 6, "banana": 0 } },
            { "name": "pnw", "inventory": { "orange": 20, "apple": 3 } },
            { "name": "lmi", "inventory": { "apple": 10, "banana": 6 } }

        ]
        expected = [
            { "owd": { "banana": 2 } },
            { "dm":  { "apple": 6 } },
            { "pnw": { "apple": 3, "orange": 1 } },
            { "lmi": { "apple": 1, "banana": 5 } }
        ]

        output = InventoryAllocator.allocate(order, inventory)
        self.assertTrue(self._compare_shipments(expected, output))

    def test_zero_inventory(self):
        """
        Tests that an order for a particular item will not be fulfilled if any warehouse
        that lists it has 0 of it, or if a warehouse doesn't have any inventory.
        """

        order = { "apple": 1 }
        inventory = [
            { "name": "owd", "inventory": { } },
            { "name": "pnw", "inventory": { "apple": 0 } }
        ]
        expected = []

        output = InventoryAllocator.allocate(order, inventory)
        self.assertTrue(self._compare_shipments(expected, output))

    def test_zero_inventory_some_warehouses(self):
        """
        Tests that an order for a particular item will be fulfilled with only the
        warehouses that have it in their inventory, and that no additional warehouses
        are listed.
        """

        order = { "apple": 3 }
        inventory = [
            { "name": "owd", "inventory": { "apple": 0 } },
            { "name": "dm",  "inventory": { "orange": 5 } },
            { "name": "pnw", "inventory": { "apple": 3 } },
            { "name": "lmi", "inventory": { "apple": 1 } }
        ]
        expected = [
            { "pnw": { "apple": 3 } }
        ]

        output = InventoryAllocator.allocate(order, inventory)
        self.assertTrue(self._compare_shipments(expected, output))
    
    def test_insufficient_inventory_multiple_items(self):
        """
        Tests that an order for several items will not be fulfilled if there aren't
        enough of them across all warehouses to meet the requested quantity.
        """

        order = { "apple": 4, "orange": 5 }
        inventory = [
            { "name": "owd", "inventory": { "apple": 1 } },
            { "name": "dm",  "inventory": { "apple": 2, "orange": 4 } }
        ]
        expected = []

        output = InventoryAllocator.allocate(order, inventory)
        self.assertTrue(self._compare_shipments(expected, output))   

if __name__ == '__main__':
    unittest.main()