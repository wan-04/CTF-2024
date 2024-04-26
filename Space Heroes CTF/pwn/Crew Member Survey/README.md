# Crew Member Survey [500 pts]

**Category:** pwn
**Solves:** 0

## Description
>The company is developing an anonymous survey for crew members to fill out on the last day before quota.\r\n\r\nThey left an alpha version for us to test on the VM! Be sure to only leave good responses!\r\n\r\n<br/>\r\n\r\n```py\r\nfrom pwn import * \r\np=remote("spaceheroes-crew-member-survey.chals.io", 443, ssl=True, sni="spaceheroes-crew-member-survey.chals.io")\r\np.interactive()\r\n```\r\n\r\nMD5SUM:\r\n\r\n```\r\nbe1d30648b981fbc1ae8d60625abe667  Borson300VM.bin\r\n\r\n6d0abd9a3dada46c4d23c0002d705256  pwnable\r\n```\r\n\r\nAuthor: [B0n3h34d](https://github.com/password987654321)

**Hint**
* -

## Solution

### Flag

