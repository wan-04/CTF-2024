# Lethal Virtualization [500 pts]

**Category:** re
**Solves:** 0

## Description
>The company created a VM for our ship\s computer to test new software. \r\n\r\nIt looks like the company left a debug session of the VM on the network.\r\nCan you find the contents of `flag.txt`?\r\n\r\nYou should probably run it in Docker or at least patch our check that requires you to run it in Docker. \r\n\r\n<br/>\r\n\r\n```py\r\nfrom pwn import * \r\np=remote("spaceheroes-lethal-virtualization.chals.io", 443, ssl=True, sni="spaceheroes-lethal-virtualization.chals.io")\r\np.interactive()\r\n```\r\n\r\nMD5SUM:\r\n\r\n```\r\nbe1d30648b981fbc1ae8d60625abe667  Borson300VM.bin\r\n```\r\n\r\nAuthor: [B0n3h34d](https://github.com/password987654321)

**Hint**
* 500 credits have been added to your quota.

## Solution

### Flag

