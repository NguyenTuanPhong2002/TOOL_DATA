import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import math
import random
from datetime import datetime

# Initialize Firebase Admin SDK
cred = credentials.Certificate('C:/Users/luuma/PycharmProjects/pythonProject1/Capacitor.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://capacitor-129e8-default-rtdb.firebaseio.com/'
})

# Get input values from the user
active_power = float(input("Enter the value of Active Power: "))
cos_fi = float(input("Enter the value of CosFi: "))

# Calculate Reactive Power
radian = math.acos(cos_fi)
tan_fi = math.tan(radian)
reactive_power = round(tan_fi * active_power)

# Initialize default values for coil variables
coil_1 = "0"
coil_2 = "0"
coil_3 = "0"
coil_4 = "0"
contactor_status_1 = "OFF"
contactor_status_2 = "OFF"
contactor_status_3 = "OFF"
contactor_status_4 = "OFF"

if cos_fi < 0.9:
    tan_fi_2 = math.tan(math.acos(0.9))
    reactive_power_adapt = tan_fi_2 * active_power
    compensated_reactive_power = reactive_power - reactive_power_adapt

    # Calculate the number of capacitors to be switched on/off
    num_capacitors = int(compensated_reactive_power / 1500)# 20 is the capacity of one capacitor
    print(num_capacitors)
    if num_capacitors == 1:
        contactor_status_1 = "ON"
        coil_1 = "1"
    elif num_capacitors == 2:
        contactor_status_1 = "ON"
        contactor_status_2 = "ON"
        coil_1 = "1"
        coil_2 = "1"
    elif num_capacitors == 3:
        contactor_status_1 = "ON"
        contactor_status_2 = "ON"
        contactor_status_3 = "ON"
        coil_1 = "1"
        coil_2 = "1"
        coil_3 = "1"
    elif num_capacitors >= 4:
        contactor_status_1 = "ON"
        contactor_status_2 = "ON"
        contactor_status_3 = "ON"
        contactor_status_4 = "ON"
        coil_1 = "1"
        coil_2 = "1"
        coil_3 = "1"
        coil_4 = "1"
else:
    contactor_status_1 = "OFF"

# Generate random frequency
frequency = random.uniform(49, 51)
rounded_frequency = round(frequency, 2)
print(rounded_frequency)
# Get current time
current_time = datetime.now()
formatted_time = current_time.strftime('%d/%m/%y,%H:%M:%S')
print(formatted_time)
# Generate random voltage
three_phase_voltage = random.uniform(390, 420)
rounded_voltage = round(three_phase_voltage, 2)
print(rounded_voltage)
# Calculate current
three_phase_current = round(active_power / (cos_fi * three_phase_voltage), 2)
print(three_phase_current)
# Prepare data to update in Firebase Realtime Database
data = {
    'test': {
        '1': {
            'ActivePower': active_power,
            'CosFi': cos_fi,
            'ReactivePower': reactive_power,
            'Coil 1': coil_1,
            'Coil 2': coil_2,
            'Coil 3': coil_3,
            'Coil 4': coil_4,
            'Contactor1': contactor_status_1,
            'Contactor2': contactor_status_2,
            'Contactor3': contactor_status_3,
            'Contactor4': contactor_status_4,
            'Frequency': rounded_frequency,
            'TIME': formatted_time,
            'Three_phase_Equivalent_Voltage': rounded_voltage,
            'Three_phase_Equivalent_Current': three_phase_current
        }
    }
}

# Write data to Firebase Realtime Database
ref = db.reference()
ref.update(data)

print('Data has been created and written to the Firebase Realtime Database.')