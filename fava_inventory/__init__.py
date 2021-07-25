"""
Physical inventory list extension for fava.

Usage: 
YYYY-MM-DD custom "fava-extension" "fava_inventory" "[('Consignment', 'In-Transit', 'In-Stock'), 'inventory.beancount']"
"""
import re

from beancount.core.data import Commodity
from beancount.core.number import Decimal

from fava.ext import FavaExtensionBase
from fava.helpers import FavaAPIException
from fava.template_filters import cost_or_value

class InventoryList(FavaExtensionBase):  # pragma: no cover

    report_title = "Inventory"

    # returns types for query_table headers
    def get_types(self):

        types = []

        types.append(("SKU", str(str)))
        types.append(("Name", str(str)))

        for account in self.config[0]:
            types.append((account, str(Decimal)))

        types.append(("Total", str(Decimal)))

        return types

    # returns contents of query_table
    def get_inventories(self):

        tree = self.ledger.root_tree
        commodities = self.ledger.all_entries_by_type.Commodity

        inventories = {}

        for commodity in commodities:
            if (self.config[1] is not None and re.compile("^.*" + self.config[1] +"$").match(commodity.meta['filename']) is not None):
                inventory = {}
                inventory['Name'] = commodity.meta['name']
                inventories[commodity.currency] = inventory

        for inventory_account in self._get_inventory_accounts(tree):
            label = inventory_account[0]
            account = inventory_account[1]
            for bal in account.balance:
                sku = bal[0]
                inventory = inventories.get(sku) if (inventories.get(sku) is not None) else {}
                inventory[label] = inventory[label] + account.balance[bal] if label in inventory else account.balance[bal]
                inventories[sku] = inventory

        return self._get_rows_from_inventories(inventories)

    # returns list of tuples (label, account_node)
    def _get_inventory_accounts(self, tree):
        selected_accounts = []
        for account in self.config[0]:
            for key in tree.keys():
                if (re.compile("^.*:" + account + "$").match(key) is not None):
                    selected_accounts.append((account, tree[key]))
                    break
        
        return selected_accounts

    # returns rows as results based on inventories dictionary
    def _get_rows_from_inventories(self, inventories):
        rows = []
        for inventory in inventories:
            row = {}
            row["SKU"] = inventory

            balances = inventories[inventory]
            total = 0
            for balance in balances:
                row[balance] = balances[balance]
                if (balance != "Name"):
                    total += row[balance]
            row["Total"] = total

            rows.append(row)

        return rows