from Vidasan.models import Siparis, QualityTypes, Materials, KaplamaTypes, ProcessState, SiparisState
from Vidasan.serializers import SiparisSerializer
from Authentication.models import UserType
from random import choice, randint
from datetime import datetime, timedelta

# Helper function to generate random dates
def random_date(start, end):
    return start + timedelta(days=randint(0, int((end - start).days)))

# Set the date range for orderDate and deadline
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)

# Automatically generate 100 Siparis objects
for i in range(100):
    siparis_data = {
        'definition': f'Definition {i+1}',
        'description': f'This is a detailed description for Siparis {i+1}.',
        'amount': randint(1, 1000),
        'deadline': random_date(start_date, end_date).date(),
        'orderDate': random_date(start_date, end_date).date(),
        'isOEM': choice([True, False]),
        'isActive': choice([True, False]),
        'material': choice([material[0] for material in Materials.get_choices()]),
        'quality': choice([quality[0] for quality in QualityTypes.get_choices()]),
        'kaplama': choice([kaplama[0] for kaplama in KaplamaTypes.get_choices()]),
        'patch': f'Patch {i+1}',
        'materialNumber': f'MaterialNumber {i+1}',
        'clientOrderNumber': f'ClientOrderNumber {i+1}',
        'company': f'Company {i+1}',
        'state': choice([state[0] for state in SiparisState.get_choices()]),
        'pressState': choice([state[0] for state in ProcessState.get_choices()]),
        'byckState': choice([state[0] for state in ProcessState.get_choices()]),
        'ovalamaState': choice([state[0] for state in ProcessState.get_choices()]),
        'sementasyonState': choice([state[0] for state in ProcessState.get_choices()]),
        'kaplamaState': choice([state[0] for state in ProcessState.get_choices()]),
        'ambalajState': choice([state[0] for state in ProcessState.get_choices()]),
    }

    # Serialize and save the Siparis object
    serializer = SiparisSerializer(data=siparis_data)
    if serializer.is_valid():
        serializer.save()
    else:
        print(f"Error creating Siparis {i+1}: {serializer.errors}")

print("100 Siparis objects have been created successfully.")
