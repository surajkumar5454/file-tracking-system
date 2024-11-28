import os

# Create directories
directories = [
    'instance',
    'uploads',
    'uploads/temp',
    'app/templates/admin',
    'app/templates/auth',
    'app/templates/proposal'
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f'Created directory: {directory}') 