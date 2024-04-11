# Service Units Calculator

This project provides a set of Python scripts to calculate service units (SU) for computational jobs based on their resource requests and usage. The calculation is performed using a predefined formula that takes into account the number of CPUs requested, memory requested, walltime usage, and queue charge rate.

## Prerequisites

- Python 3.6 or higher

## Installation

No additional installation is required beyond having Python installed on your system.

## Usage

### Main Script

The main script, `main.py`, calculates the service units for all job files in a specified directory and saves the results in a CSV file.

1. **Run the Script:**
   ```bash
   python main.py <directory_path>
   ```
   Replace `<directory_path>` with the path to the directory containing your job files.

2. **View the Results:**
   - The script will create a CSV file named `service_units.csv` in the current working directory.
   - This file contains two columns: `File Name` and `Service Units`. Each row represents a job file and its calculated service units.

### Test Script

The test script, `test.py`, runs a set of predefined test cases to verify the correctness of the service units calculation.

1. **Run the Script:**
   ```bash
   python tests/test.py
   ```

2. **View the Test Results:**
   - The script will output the result of each test case to the console.
   - It will indicate whether each test case passed or failed based on the expected service units.

## Job File Format

The job files should be PBS files containing PBS directives for resource requests. Here is an example format:

```
#!/bin/tcsh
#PBS -P ad73
#PBS -l walltime=03:00:00
#PBS -l mem=180GB
#PBS -l jobfs=10GB
#PBS -l ncpus=32
#PBS -o outputD15_C1.20e-05_S30_B2.0_E0.05.out
#PBS -e outputD15_C1.20e-05_S30_B2.0_E0.05.err
#PBS -l storage=gdata/ad73+scratch/ad73
#PBS -N Allfree
#PBS -M <EMAIL>
#PBS -m ae
#PBS -l software=y_program
#PBS -l wd
set executable="/g/data/ad73/codes/NEMO3D_other_copies/NEMO3D_Broyden/NEMO3D/nemo3d/bin/nemo3d-x86_64_intel20_64_openmpi_gadi.ex"
echo $executable
cd $PBS_O_WORKDIR
set machinefile=`basename $PBS_NODEFILE`
cp $PBS_NODEFILE machinefileD15_C1.20e-05_S30_B2.0_E0.05.txt
module purge
module load pbs
module load intel-compiler/2020.0.166
module load openmpi/4.0.2
module load intel-mkl/2020.0.166
set cmd="mpirun -np $PBS_NCPUS -machinefile machinefileD15_C1.20e-05_S30_B2.0_E0.05.txt $executable xml/QDBase_D15_nm_C1.20e-05_S30_B2.0_E0.05.xml"
echo $cmd
$cmd
```

## Contributing

Feel free to contribute to this project by submitting pull requests or reporting issues.

## License

This project is licensed under the MIT License - see the LICENSE file for details.


