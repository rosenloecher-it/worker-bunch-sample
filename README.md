# Sample-App for Worker-Bunch

For details about what and why see [Worker-Bunch](https://github.com/rosenloecher-it/worker-bunch). 
This is just a sample application to see how it works.


## Startup

### Prepare python environment
```bash
cd /opt
sudo mkdir worker-bunch-sample
sudo chown <user>:<user> worker-bunch-sample  # type in your user
git clone https://github.com/rosenloecher-it/worker-bunch-sample worker-bunch-sample

cd worker-bunch-sample
virtualenv -p /usr/bin/python3 venv

# activate venv
source ./venv/bin/activate

# check python version >= 3.8
python --version

# install required packages
pip install -r requirements.txt

# in your own application this will do too
pip install worker-bunch
```

### Configuration

```bash
# cd ... goto project dir
cp ./worker-bunch-sample.yaml.sample ./worker-bunch-sample.yaml

# security concerns: make sure, no one can read the stored passwords
chmod 600 ./worker-bunch-sample.yaml
```

Edit your `worker-bunch-sample.yaml`.

### Run

```bash
# see command line options
./worker-bunch-sample.sh --help

# prepare your own config file based on ./worker-bunch-sample.yaml.sample
# the embedded json schema may contain additional information
./worker-bunch-sample.sh --json-schema
# the JSON schema get dynamically adapted by configured workers, so this output contain more also the worker sections.
./worker-bunch-sample.sh --json-schema --config-file ./worker-bunch-sample.yaml

# start the logger
./worker-bunch-sample.sh --print-logs --config-file ./worker-bunch-sample.yaml
# abort with ctrl+c

```

## Register as systemd service
```bash
# prepare your own service script based on worker-bunch-sample.service.sample
cp ./worker-bunch-sample.service.sample ./worker-bunch-sample.service

# edit/adapt paths and user in worker-bunch-sample.service
vi ./worker-bunch-sample.service

# install service
sudo cp ./worker-bunch-sample.service /etc/systemd/system/
# alternativ: sudo cp ./worker-bunch-sample.service.sample /etc/systemd/system//worker-bunch-sample.service
# after changes
sudo systemctl daemon-reload

# start service
sudo systemctl start worker-bunch-sample

# check logs
journalctl -u worker-bunch-sample
journalctl -u worker-bunch-sample --no-pager --since "5 minutes ago"

# enable autostart at boot time
sudo systemctl enable worker-bunch-sample.service
```

## Additional infos

### MQTT broker related infos

If no messages get logged check your broker.
```bash
sudo apt-get install mosquitto-clients

# prepare credentials
SERVER="<your server>"

# start listener
mosquitto_sub -h $SERVER -d -t smarthome/#

# send single message
mosquitto_pub -h $SERVER -d -t smarthome/test -m "test_$(date)"

# just as info: clear retained messages
mosquitto_pub -h $SERVER -d -t smarthome/test -n -r -d
```


## Maintainer & License

MIT © [Raul Rosenlöcher](https://github.com/rosenloecher-it)

The code is available at [GitHub][home].

[home]: https://github.com/rosenloecher-it/worker-bunch-sample
