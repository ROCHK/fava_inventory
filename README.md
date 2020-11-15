# fava_inventory

WORK IN PROGRESS

## Installation
```bash
pip install fava_inventory
```

### Usage
```
2000-01-01 custom "fava-extension" "fava_inventory" "[('Consignment', 'In-Transit', 'In-Stock'), 'inventory.beancount']"
```
The example above tells the extension to look for commodity entries in inventory.beancount, then summarize inventory balances in accounts containing "Consignment", "In-Transit" and "In-Stock" in their names. 
