# Generated by Django 5.0 on 2023-12-28 23:09

from django.db import migrations

def populate_peripherals(apps, schemaeditor):
    entries = [
        {
            "name": "LED",
            "type": "INOUT",
            "neededPins": 1,
            "icon": "lightbulb",
        },
        {
            "name": "BUZZER",
            "type": "OUT",
            "icon": "volume-up",
            "neededPins": 1,
        },
        {
            "name": "DHT11",
            "type": "IN",
            "icon": "thermometer-half",
            "neededPins": 1,
        },
        {
            "name": "POTENTIOMETER",
            "type": "IN",
            "icon": "speedometer2",
            "neededPins": 1,
        },
        {
            "name": "PIR",
            "type": "IN",
            "icon": "eye",
            "neededPins": 1,
        },
    ]
    Peripheral = apps.get_model("pages", "Peripheral")
    for peripheral in entries:
        peripheral_obj = Peripheral(
                            name=peripheral["name"], 
                            type=peripheral["type"],
                            icon=peripheral["icon"], 
                            neededPins=peripheral["neededPins"],
                         )
        peripheral_obj.save()
def populate_microcontrollers(apps, schemaeditor):
    entries = [
        {
            "name": "ESP32",
            "availablePins": 32,
            "infoLink": "https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_en.pdf",
        },
        {
            "name": "Raspberry Pi Pico",
            "availablePins": 32,
            "infoLink": "https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html",
        },
        {
            "name": "Arduino Uno R4",
            "availablePins": 20,
            "infoLink": "https://docs.arduino.cc/hardware/uno-r4-wifi",
        },
    ]
    Microntroller = apps.get_model("pages", "Microcontroller")
    for microcontroller in entries:
        microcontroller_obj = Microntroller(
                            name=microcontroller["name"], 
                            availablePins=microcontroller["availablePins"],
                            infoLink=microcontroller["infoLink"], 
                         )
        microcontroller_obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_peripherals),
        migrations.RunPython(populate_microcontrollers),
    ]
