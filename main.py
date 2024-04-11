import csv
import os
import re
import argparse

# Define the queue charge rates
queue_charge_rates = {
    'normal': 2,
    'express': 6,
    'gpuvolta': 3
}

# Define the ncpus per node and mem per node for different queues
node_resources = {
    'normal': {'ncpus_per_node': 48, 'mem_per_node': 192},  # GB
    'express': {'ncpus_per_node': 48, 'mem_per_node': 192},  # GB
    'gpuvolta': {'ncpus_per_node': 48, 'mem_per_node': 382}  # GB
}


def calculate_su(queue, ncpus_request, mem_request, walltime_usage):
    """
    Calculate the service units based on the provided parameters.
    """
    ncpus_per_node = node_resources[queue]['ncpus_per_node']
    mem_per_node = node_resources[queue]['mem_per_node']
    queue_charge_rate = queue_charge_rates[queue]

    job_cost = ncpus_request * max(1, (ncpus_per_node / mem_per_node) * (
            mem_request / ncpus_request)) * walltime_usage * queue_charge_rate
    return job_cost


def extract_job_info(job_file):
    """
    Extract job information from the provided file.
    """
    with open(job_file, 'r') as file:
        content = file.read()

    # Extract relevant information using regular expressions
    ncpus = int(re.search(r'-l ncpus=(\d+)', content).group(1))
    mem = int(re.search(r'-l mem=(\d+)GB', content).group(1))
    walltime = re.search(r'-l walltime=(\d+):(\d+):(\d+)', content)
    walltime_hours = int(walltime.group(1)) + int(walltime.group(2)) / 60 + int(walltime.group(3)) / 3600

    # Determine the queue based on the presence of certain keywords
    if 'gpuvolta' in content:
        queue = 'gpuvolta'
    elif 'express' in content:
        queue = 'express'
    else:
        queue = 'normal'

    return queue, ncpus, mem, walltime_hours


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Calculate service units for all job files in a directory.')
    parser.add_argument('directory', type=str, help='Path to the directory containing job files')

    # Parse arguments
    args = parser.parse_args()
    directory = args.directory

    # Create a CSV file to store the results
    with open('service_units.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['File Name', 'Service Units'])

        # Loop through all files in the directory
        for filename in os.listdir(directory):
            if filename.endswith('.pbs'):  # Assuming job files have a .txt extension
                job_file = os.path.join(directory, filename)
                queue, ncpus_request, mem_request, walltime_usage = extract_job_info(job_file)
                su = calculate_su(queue, ncpus_request, mem_request, walltime_usage)
                print(f'{filename}: {su:.2f} SU')
                writer.writerow([filename, f'{su:.2f}'])

if __name__ == '__main__':
    main()