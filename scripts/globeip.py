import json
import random
import ipaddress
import uuid

with open('country.json', 'r') as file:
    data = []
    for line in file:
        try:
            entry = json.loads(line)
            data.append(entry)
        except json.JSONDecodeError:
            print(f"无法解析的行: {line.strip()}")

unique_countries = {}

for entry in data:
    start_ip = entry['start_ip']
    try:
        ip_obj = ipaddress.ip_address(start_ip)
        if ip_obj.version != 4:  # 仅接受 IPv4
            raise ValueError("不是 IPv4 地址")
    except ValueError:
        continue

    country_code = entry['country']
    if country_code not in unique_countries:
        unique_countries[country_code] = entry

deduplicated_data = list(unique_countries.values())
print(f"去重后的数据条数: {len(deduplicated_data)}")
random_ips = []
for entry in deduplicated_data:
    start_ip = entry['start_ip']
    end_ip = entry['end_ip']
    start_ip_int = int(ipaddress.ip_address(start_ip))
    end_ip_int = int(ipaddress.ip_address(end_ip))
    random_ip_int = random.randint(start_ip_int, end_ip_int)
    random_ip = str(ipaddress.ip_address(random_ip_int))
    random_uuid = str(uuid.uuid4())  # 生成随机 UUID
    random_ips.append({"ip": random_ip, "UUID": random_uuid,"country": entry['country']})
with open('fakeip.json', 'w') as random_file:
    json.dump(random_ips, random_file, indent=4)