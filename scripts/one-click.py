import yaml
import json
import os

with open('/opt/nezha/agent/config-fake.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)


with open('/opt/nezha/agent/fakeip.json', 'r') as fakeip_file:
    fakeips = json.load(fakeip_file)


os.makedirs('/opt/nezha/agent/fakemjj', exist_ok=True)
services_to_start_enable = []

service_template = """[Unit]
Description=哪吒监控 Agent
ConditionFileIsExecutable=/opt/nezha/agent/nezha-agent-fake


[Service]
StartLimitInterval=5
StartLimitBurst=10
ExecStart=/opt/nezha/agent/nezha-agent-fake "-c" "/opt/nezha/agent/fakemjj/config-%s.yml"

WorkingDirectory=/opt/nezha/agent


Restart=always

RestartSec=120
EnvironmentFile=-/etc/sysconfig/nezha-agent-fake

[Install]
WantedBy=multi-user.target"""


for fakeip in fakeips:
    config['ip'] = fakeip['ip']
    config['uuid'] = fakeip['UUID']

    country = fakeip.get('country', 'default') 
    config_filename = f'config-{country}.yml'
    service_filename = f'nezha-agent-{country}.service'

    with open(os.path.join('/opt/nezha/agent/fakemjj', config_filename), 'w') as new_config_file:
        yaml.dump(config, new_config_file, default_flow_style=False)

    service_content = service_template % country
    with open(os.path.join('/opt/nezha/agent/fakemjj', service_filename), 'w') as service_file:
        service_file.write(service_content)

    print(f'Generated {config_filename} and {service_filename}')
    services_to_start_enable.append(service_filename)

start_command = 'systemctl start ' + ' '.join(services_to_start_enable)
enable_command = 'systemctl enable ' + ' '.join(services_to_start_enable)
os.system("cp ./fakemjj/*.service /etc/systemd/system/")
os.system("systemctl daemon-reload")
os.system(start_command)
os.system(enable_command)