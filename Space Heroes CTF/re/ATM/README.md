# ATM [473 pts]

**Category:** re
**Solves:** 27

## Description
>You\re out of space fuel! Luckily some dope left his alien credit card on the ground outside the ATM at the dark matter station. It has a weird aura though. Oh well! Fill up your tank so you can keep moving!\r\n\r\n```python\r\nfrom pwn import *\r\np = remote("spaceheroes-atm.chals.io", 443, ssl=True, sni="spaceheroes-atm.chals.io")\r\np.interactive()\r\n```\r\n\r\n```python\r\nmd5(atm.bin)= a9bc824d0ee34a041a3a8cb036bb0701\r\n```\r\nAuthor: Parker Cummings

**Hint**
* -

## Solution

### Flag

