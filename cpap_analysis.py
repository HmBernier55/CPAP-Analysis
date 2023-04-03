import math
import json


def read_file(filename):
    """Reads in a text file of data line by line

    The function takes an input of a text document filename, opens and
    reads in the text file line by line, and saves each line of the
    text file as a string in a list format.

    Args:
        filename (string): name of the text file with patient data

    Returns:
        list of strings: every line within the inputted text file
    """
    data_file = open("{}.txt".format(filename), 'r')
    in_lines = data_file.readlines()
    data_file.close()
    return in_lines


def parse_input(lines, count):
    """Extracts five lines of patient data and removes \n formatting

    The function receives a list of lines from a text file
    and an iteration value. It extracts 5 lines (or five
    elements from the inputted list), using the iteration
    value to tell it which lines from the list to extract,
    and removes the \n from the end of each line.

    Args:
        lines (list of strings): list of lines from a text file
        count (int): an integer used for indexing which lines to
            extract from the list

    Returns:
        list of strings: five lines (or five elements) from the list
    """
    patient = lines[count:(count + 5)]
    new_patient = []
    for ele in patient:
        new_patient.append(ele.strip())
    return new_patient


def separate_list(patient):
    """Separates each element in the list into its respective category

    The function recieves a list of five strings and puts the first string
    in a variable called name and the second string in a variable called hours.
    It takes strings three, four, and five, and splits them into a list of
    strings using a ',' as a delimiter. It takes these new variables and
    creates a new list with the form of [string, string, list of strings,
    list of strings, list of strings]

    Args:
        patient (list of strings): list containing five strings of patient data

    Returns:
        list: a new list of strings with the third, fourth, and fifth elements
            being another list of strings
    """
    name = patient[0]
    hours = patient[1]
    seal = patient[2].split(",")
    events = patient[3].split(",")
    o2 = patient[4].split(",")
    patient_list = [name, hours, seal, events, o2]
    return patient_list


def create_patient_dict(patient):
    """Creating a dictionary of patient data

    The function receives a list of strings containing patient data and creates
    a dictionary from the patient data. The first element of the inputted list
    gets broken up into a first and last name key. The second element gets
    converted into a float and is assigned the 'Hours' key. The third element
    (which is a list) gets converted to a list of floats and is assigned the
    'Seal' key. The fourth element (a list) gets converted to a list of
    integers and is assigned the 'Events' key. The last element (a list)
    gets converted to a list of integers and is assigned the 'O2' key.

    Args:
        patient (list of strings): a list of strings containing patient data

    Returns:
        dictionary: a dictionary of patient data with keys of First Name
            (string), Last Name (string), Hours (float), Seal (float),
            Events (int), and O2 (int)
    """
    first, last = patient[0].split(" ")
    patient_dict = {"First Name": first,
                    "Last Name": last,
                    "Hours": float(patient[1]),
                    "Seal": [float(x) for x in patient[2][1:]],
                    "Events": [int(x) for x in patient[3][1:]],
                    "O2": [int(x) for x in patient[4][1:]]}
    return patient_dict


def avg_leakage(leakage, hours):
    """Calculates the average air leakage from the CPAP mask during sleep

    The function calculates the average air leakage per night using
    the data for the average air leakage per hour of sleep and the number
    of hours of sleep. The number of hours of sleep is rounded down to
    the nearest hour for the calculation. The formula for average leakage
    is: avg_leakage = sum(average leakage per hour)/number of hours of
    sleep. The average leakage has units of L/min.

    Args:
        leakage (list of floats): list of values for the average leakage
            per hour
        hours (float): number of hours the patient slept

    Returns:
        float: the calculated average leakage per night
    """
    num_hours = math.floor(hours)
    avg_leak = sum(leakage)/num_hours
    return avg_leak


def avg_events(events, hours):
    """Calculates the average number of events that occurred during sleep

    The function calculates the average events per night using
    the data for the number of events that occurred per hour of sleep
    and the number of hours of sleep. The number of hours of sleep is
    rounded down to the nearest hour for the calculation.
    The formula for average events per night is:
    avg_events = sum(number of events per hour)/number of hours of sleep

    Args:
        events (list of integers): list of values for the number of events
            that occurred per hour
        hours (float): number of hours the patient slept

    Returns:
        float: the calculated average events per night
    """
    num_hours = math.floor(hours)
    avg_events = sum(events)/num_hours
    return avg_events


def patient_diagnosis(events, oxygen):
    """Determines the diagnosis of the patient using average events and
        O2 values

    The function determines the diagnosis of the patient (either 'normal
    sleep', 'apnea', 'hypoxia', or 'hypoxia apnea') using the average
    events per night and the hourly average pulse oximeter readings. If
    the patient has an average of 5 or less events per night and all of
    their O2 values are greater than or equal to 93%, then they are diagnosed
    with normal sleep. If the patient has an average of 5 or less events per
    night and any one of their O2 values is 92% or less, then the patient is
    diagnosed with hypoxia. If the patient has an average of 6 or more events
    per night and all of their O2 values are 93% or more, then the patient is
    diagnosed with apnea. If the patient has an average of 6 or more events per
    night and any one of their O2 values is 92% or less, then the patient is
    diagnosed with hypoxia apnea.

    Args:
        events (float): average events that occur per night
        oxygen (list of integers): a list of hourly average pulse oximeter
            readings

    Returns:
        string: a diagnosis for the patient either normal sleep, apnea,
            hypoxia, or hypoxia apnea
    """
    if all(values >= 93 for values in oxygen) and events <= 5:
        diagnosis = "normal sleep"
    elif all(values >= 93 for values in oxygen) and events > 5:
        diagnosis = "apnea"
    elif any(values < 93 for values in oxygen) and events <= 5:
        diagnosis = "hypoxia"
    else:
        diagnosis = "hypoxia apnea"
    return diagnosis


def update_patient_dict(patient_dict, avg_seal, diagnosis):
    """Updates the patient dictionary with average leakage value and diagnosis

    The function updates the patient dictionary that was created in the
    create_patient_dict function with the newly calculated average leakage
    value and newly determined diagnosis for the patient

    Args:
        patient_dict (dictionary): dictionary of patient data containing
            First Name, Last Name, Hours, Seal, Events, and O2
        avg_seal (float): average leakage per night in L/min
        diagnosis (string): determined diagnosis of patient either normal
            sleep, apnea, hypoxia, or hypoxia apnea

    Returns:
        dictionary: updated dictionary of patient data containing First Name,
            Last Name, Hours, Seal, Events, O2, Seal Average, and Diagnosis
    """
    patient_dict["Seal Average"] = float(avg_seal)
    patient_dict["Diagnosis"] = "{}".format(diagnosis)
    return patient_dict


def output_file(patient_dict):
    """Creates a .json file and outputs the file

    The function receives a dictionary of patient data, creates a .json
    file with the filename of 'firstname-lastname.json', dumps the
    patient dictionary into the .json file, and outputs the file
    into the local directory

    Args:
        patient_dict (dictionary): dictionary of patient data containing
            First Name, Last Name, Hours, Seal, Events, O2, Seal Average,
            and Diagnosis

    Returns:
        file: a .json file containing a dictionary of patient data
    """
    filename = "{}-{}.json".format(patient_dict["First Name"],
                                   patient_dict["Last Name"])
    out_file = open(filename, "w")
    json.dump(patient_dict, out_file)
    out_file.close()
    return out_file


def main():
    """Runs each function above to obtain the final .json file

    The function is the driver function for the code. It first runs
    the read_file function to read in a specified text file. It iterates
    through a for loop where the number of iterations is equal to
    the number of patients. This value is determined by calculating
    the number of lines in the text file, subtracting one, and dividing
    by 5 (since each patient has 5 lines of data). The iterations
    variable is a list of integers starting at 0, incrementing by
    5 and ending at the number of lines in the text file minus 1.
    Within the for loop, the following functions are run in this order:
    parse_input, separate_list, create_patient_dict, avg_leakage,
    avg_events, patient_diagnosis, update_patient_dict, and output_file.
    The end result of the function is .json files for each patient.

    Returns:
        file: .json files for each patient
    """
    file_lines = read_file("sample_data")
    iterations = list(range(0, int((len(file_lines)-1)), 5))
    for a in iterations:
        patient_info = parse_input(file_lines, a)
        patient_list = separate_list(patient_info)
        patient_dict = create_patient_dict(patient_list)
        seal_avg = avg_leakage(patient_dict["Seal"], patient_dict["Hours"])
        events_avg = avg_events(patient_dict["Events"], patient_dict["Hours"])
        diagnosis = patient_diagnosis(events_avg, patient_dict["O2"])
        new_patient_dict = update_patient_dict(patient_dict,
                                               seal_avg, diagnosis)
        out_file = output_file(new_patient_dict)


if __name__ == "__main__":
    main()
