Based on Mordor 6.66 from http://mordor.nazgul.com/treasures/

See patch.diff for changes

Requires  qemu-system-microblazeel

To get the machine online,you might need to set it up yourself
ifconfig eth0 10.0.2.15 netmask 255.255.255.0
echo 4.2.2.2 > /etc/resolv.conf
ip route add default via 10.0.2.2 dev eth0

cd /moror/bin
./mordord -r


