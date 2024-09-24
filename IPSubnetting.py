import ipaddress
from tabulate import tabulate

def subnet_ipv4(ip, subnet_mask, num_subnets):
    subnet = ipaddress.ip_network(f"{ip}/{subnet_mask}", strict=False)

    max_subnets = 2 ** (32 - subnet.prefixlen)
    if num_subnets > max_subnets:
        print(f"Error: Number of subnets requested ({num_subnets}) exceeds maximum possible subnets ({max_subnets}) for the given subnet mask.")
        return

    new_prefix_length = subnet.prefixlen
    while (2 ** (new_prefix_length - subnet.prefixlen)) < num_subnets:
        new_prefix_length += 1

    if new_prefix_length > 32:
        print("Error: Subnetting request exceeds address space limits.")
        return


    subnets = list(subnet.subnets(new_prefix=new_prefix_length))[:num_subnets]

    subnet_details = []
    for sub in subnets:
        subnet_details.append([
            sub,
            f"/{new_prefix_length}",
            f"{sub.network_address + 1} - {sub.broadcast_address - 1}",
            sub.num_addresses - 2,
            sub.broadcast_address
        ])

    return subnet_details


ip_address = input("Enter IPv4 address: ")
subnet_mask = input("Enter subnet mask in slash notation (e.g., 24): ")
num_subnets = int(input("Enter the number of subnets desired: "))

subnet_row = ["Subnet", "1", "2", "4", "8", "16", "32", "64", "128", "256"]

if int(subnet_mask) >= 24:
    hostmask_row = [
        ["Host", "256", "128", "64", "32", "16", "8", "4", "2", "1"],
        ["Mask", "/24", "/25", "/26", "/27", "/28", "/29", "/30", "/31", "/32"]
    ]
elif int(subnet_mask) >= 16:
    hostmask_row = [
        ["Host", "256", "128", "64", "32", "16", "8", "4", "2", "1"],
        ["Mask", "/16", "/17", "/18", "/19", "/20", "/21", "/22", "/23", "/24"]
    ]
else:
    hostmask_row = [
        ["Host", "256", "128", "64", "32", "16", "8", "4", "2", "1"],
        ["Mask", "/8", "/9", "/10", "/11", "/12", "/13", "/14", "/15", "/16"]
    ]


mainTable = tabulate(hostmask_row, subnet_row, tablefmt="grid")
print(mainTable)

subnets_info = subnet_ipv4(ip_address, subnet_mask, num_subnets)



print("\nSubnet Details:")
print(tabulate(subnets_info, headers=["Subnet", "Subnet Mask", "IPv4 Range", "Total Usable Hosts", "Broadcast Address"], tablefmt="grid"))
