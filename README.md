# fava_inventory

This simple extension adds an inventory page in fava with an up-to-date  physical inventory count.

## Installation
```bash
pip install fava_inventory
```

## Configuration
```
2000-01-01 custom "fava-extension" "fava_inventory" "[('Consignment', 'In-Transit', 'In-Stock'), 'inventory.beancount']"
```
The example above tells the extension to look for commodity entries in inventory.beancount, then summarize inventory balances in accounts containing "Consignment", "In-Transit" and "In-Stock" in their names. 

## Usage

### Inventory list

Define SKUs in a beancount file (eg inventory.beancount) like so:

```
2020-01-01 commodity BH0107B
    name: "Baby Wash Basin - Blue"

2020-01-01 commodity BH0107P
    name: "Baby Wash Basin - Pink"

2020-01-01 commodity BH0107Y
    name: "Baby Wash Basin - Yellow"

2020-01-01 commodity BH0113J
    name: "Baby Bath Towel - Wagner Magical Jungle"
```

### Accounting Entires Example

1. Initial purchase of physical inventory

    ```
    2020-07-17 * "Inventory purchase"
      Assets:Current:Inventory:In-Transit             5 FD0201P {4.74 AUD}
      Liabilities:Current:AccountsPayable:Supplier
    ```

2. Stock arrival

    ```
    2020-08-17 * "Stock Arrival"
    Assets:Current:Inventory:In-Transit                -4 FD0201P {}
    Assets:Current:Inventory:In-Stock                   4 FD0201P {4.74 AUD}
    ```

3. Sales
    ```
    2020-08-26 * "Shopify sales"
    order: "1037"
      Assets:Current:Inventory:In-Stock                -1 FD0201P {} @ 12.95 AUD
      Income:Operating:A-Revenue:Shopify           -20.00 AUD
      Expenses:Transaction-Fee:Bank                  1.71 AUD
      Expenses:Shipping                              8.95 AUD
      Income:Operating:Z-COGS
    ```


