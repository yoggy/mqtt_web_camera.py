# mqtt_web_camera.py

## How to use
```
$ git clone https://github.com/yoggy/mqtt_web_camera.git
$ cd mqtt_web_camera
$ sudo apt install python3-opencv  python3-yaml
$ sudo pip3 install paho-mqtt

$ cp config.yaml.sample config.yaml
$ vi config.yaml

mqtt_host: iot.eclipse.org
mqtt_port: 1883
mqtt_use_auth: false
mqtt_username: username
mqtt_password: password
mqtt_publish_topic_img:  web_camera/01/image
mqtt_publish_topic_time: web_camera/01/publish_time

jpeg_width:   240
jpeg_height:  160
jpeg_quality: 20

$ python3 mqtt_web_camera.py

```

## Copyright and license
Copyright (c) 2023 yoggy

Released under the [MIT license](LICENSE)
