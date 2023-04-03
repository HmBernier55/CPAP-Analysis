# **CPAP Analysis Assignment**
### **_Author:_**
Hunter Bernier
## **_Purpose:_**
The code within this repository:
1. Reads in patient data from a text file
2. Formats the patient data into a dictionary with values having the correct data type
3. Calculates the average mask leakage for the night
4. Calculates the average events per hour for the night
5. Assigns a diagnosis for the patient based on the calculated average events per hour for the night and hourly average pulse oximeter readings
    * Diagnosis being normal sleep, apnea, hypoxia, or hypoxia apnea
6. Outputs a dictionary of patient data containing the first and last name of the patient, hours of sleep, list of hourly average air leakage, list of the number of events that occur per hour, hourly average pulse oximeter readings, average air leakage per night, and the diagnosis of the patient into a .json file.
## **_How to Run the Program:_**
1. Clone the repository onto your local drive
    * Run `git clone <githubURL>`
2. Create a new virtual environment
    * Run `python -m venv <VirtualEnvironmentName>`
3. Activate the new virtual environment
    * Run `source <VirtualEnvironmentName>/Scripts/activate` 
4. Install the required packages
    * Run `pip install -r requirements.txt`
5. To run the program, type `python cpap_analysis.py` on the command line
## **_How to Use the Program:_**
1. Enter the name of the text file into the read_file input within the main function
    * The text file needs to have the following format for each patient:
        ```
        FirstName LastName
        Hours
        Seal, s1, s2, s3, s4, etc.
        Events, e1, e2, e3, e4, etc.
        O2, o1, o2, o3, o4, etc.
        ```
    * The final line of the file needs to contain the word `END`
2. Run the program using the command stated in the section above
3. The program will then create .json files for each patient and output them into your local directory
    * The filenames for the .json files will be `<FirstName>-<LastName>.json`