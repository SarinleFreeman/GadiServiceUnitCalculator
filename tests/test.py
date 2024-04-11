import os
from tempfile import TemporaryDirectory
import subprocess
import csv

# Test cases
test_cases = [
    {
        'queue': 'normal',
        'ncpus': 4,
        'mem': 16,
        'walltime': '05:00:00',
        'expected_su': 40
    },
    {
        'queue': 'normal',
        'ncpus': 8,
        'mem': 128,
        'walltime': '05:00:00',
        'expected_su': 320
    },
    {
        'queue': 'express',
        'ncpus': 8,
        'mem': 16,
        'walltime': '05:00:00',
        'expected_su': 240
    },
    {
        'queue': 'gpuvolta',
        'ncpus': 12,
        'mem': 380,
        'walltime': '05:00:00',
        'expected_su': 716.23
    }
]

def create_test_file(test_dir, queue, ncpus, mem, walltime, file_index):
    """
    Create a test file with the specified job details.
    """
    filename = f'test_file_{file_index}.pbs'
    filepath = os.path.join(test_dir, filename)
    with open(filepath, 'w') as f:
        f.write(f'#PBS -l ncpus={ncpus}\n')
        f.write(f'#PBS -l mem={mem}GB\n')
        f.write(f'#PBS -l walltime={walltime}\n')
        if queue == 'gpuvolta':
            f.write('#PBS -q gpuvolta\n')
        elif queue == 'express':
            f.write('#PBS -q express\n')
    return filename

def run_tests():
    """
    Run the test cases and compare the calculated SU with the expected SU.
    """
    with TemporaryDirectory() as test_dir:
        # Create test files
        for i, test_case in enumerate(test_cases):
            print(test_dir, test_case['queue'], test_case['ncpus'], test_case['mem'], test_case['walltime'])
            create_test_file(test_dir, test_case['queue'], test_case['ncpus'], test_case['mem'], test_case['walltime'], i)

        # Run the main script on the test directory
        subprocess.run(['python', 'main.py', test_dir])

        # Read the results from the CSV file
        with open('service_units.csv', newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            for row, test_case in zip(reader, test_cases):
                calculated_su = float(row['Service Units'])
                expected_su = test_case['expected_su']
                if abs(calculated_su - expected_su) < 0.1:
                    print(f'Test case {row["File Name"]}: PASSED')
                else:
                    print(f'Test case {row["File Name"]}: FAILED (Expected: {expected_su} SU, Calculated: {calculated_su:.2f} SU)')

if __name__ == '__main__':
    run_tests()
