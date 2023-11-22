# DAT2CSV Conversion Program
[日本語](README-ja.md) | [English](./README.md)

## Confirmed Operating Environments
- macOS, Python 3.7.7
- Windows 10, Python 3.7.0
  - ※Both operating systems are 64-bit

## Main Program
`./script/dat2csv.py` is the main script where the process is defined.

## Usage
- Store weather information DAT files of specified format and file name in a specific folder.
  - DAT files can be obtained from the following site: https://github.com/agro-env/
- Execute the process using the following command in the shell:  
`python ./script/dat2csv.py <Path to the folder containing DAT files>  <Destination Directory> (optional)`

### Example of Execution
```
# Example of converting DAT files in a folder named 'dat' in the current directory,
# and creating a folder named 'output_dir' in the current directory to output CSV files
python ./script/dat2csv.py dat -o output_dir
```

Output directory specification is optional, so it can be omitted.

```
# If the output destination is omitted, a directory named 'output' will be created in 
# the same directory as the main program, and CSV files will be output there.
python ./script/dat2csv.py dat
```

### Output Example
1. Directory Structure
   ![fig1](https://github.com/wine-ai/dat2csv/assets/3130494/fbf01bdc-43de-4b49-8da1-e31937a0f090)
2. CSV File Structure
   ![fig2](https://github.com/wine-ai/dat2csv/assets/3130494/ac4bf981-015d-4ce7-bab8-6d161db31a40)

## Additional Notes
- The data volume is large, so the processing takes time (approximately 2 hours for processing all data from 1978 to 2017).
- The character encoding of the output CSV files is UTF-8.

