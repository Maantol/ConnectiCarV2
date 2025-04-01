#!/bin/sh

interface=$(ifconfig -a | grep "enx" | awk '{gsub(/:/, "")}; print $1')

echo "interface is $interface"

dhclient -v "$interface"
udhcpc -i "$interface"
route add -net 0.0.0.0 "$interface"

ifconfig