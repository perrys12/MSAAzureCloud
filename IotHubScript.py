import random
import time

from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "HostName=iot-project-perry.azure-devices.net;DeviceId=MyPythonDevice;SharedAccessKey=P4CLKVpirlmby5JOMMCW8pBQY20mojDBIZ5Dg6ZKKAw="

TEMPERATURE = 25.0
HUMIDITY = 40
PRESSURE = 28
MSG_TXT = '{{"temperature": {temperature}, {{"pressure": {pressure}, "humidity": {humidity}}}'

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def iothub_client_watertank():
    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        while True:
            # Build the message with simulated telemetry values.
            temperature = TEMPERATURE + (random.random() * 15)
            humidity = HUMIDITY + (random.random() * 20)
            pressure = PRESSURE + (random.random() * 1)
            msg_txt_formatted = MSG_TXT.format(temperature=temperature, humidity=humidity, pressure=pressure)
            message = Message(msg_txt_formatted)
# Add a custom application property to the message.
# An IoT hub can filter on these properties without access to the message body.
            if temperature > 20:
              message.custom_properties["temperatureAlert"] = "true"
            else:
              message.custom_properties["temperatureAlert"] = "false"

            # Send the message.
            print( "Measurements:  {}".format(message) )
            client.send_message(message)
            print ( "Measurements successfully sent" )
            time.sleep(1)

    except KeyboardInterrupt:
        print ( "IoTHubClient stopped" )

if __name__ == '__main__':
    print ( "IoT Hub - Simulated Water Tank Pressure" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_watertank()
