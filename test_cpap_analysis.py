import pytest


@pytest.mark.parametrize("file_input, expected",
                         [("input_testing", ["Hunter Bernier\n",
                                             "5.5\n", "Seal, 10.0, 5.0"])])
def test_read_file(file_input, expected):
    from cpap_analysis import read_file
    answer = read_file(file_input)
    assert answer == expected


@pytest.mark.parametrize("file_input, count, expected",
                         [("sample_data", 0, ["Anne Boynton",
                                              "7.25",
                                              "Seal,11.0,23.6,15.2,2.3,"
                                              "4.0,19.7,3.7",
                                              "Events,5,0,2,3,9,1,2",
                                              "O2,95,93,98,97,96,97,100"])])
def test_parse_input(file_input, count, expected):
    from cpap_analysis import parse_input, read_file
    list_input = read_file(file_input)
    answer = parse_input(list_input, count)
    assert answer == expected


@pytest.mark.parametrize("list_input, expected",
                         [(["Anne Boynton",
                            "7.25",
                            "Seal,11.0,23.6,15.2,2.3,"
                            "4.0,19.7,3.7",
                            "Events,5,0,2,3,9,1,2",
                            "O2,95,93,98,97,96,97,100"],
                           ["Anne Boynton",
                            "7.25",
                            ["Seal", "11.0", "23.6", "15.2", "2.3",
                             "4.0", "19.7", "3.7"],
                            ["Events", "5", "0", "2", "3", "9", "1", "2"],
                            ["O2", "95", "93", "98", "97", "96", "97",
                             "100"]])])
def test_separate_list(list_input, expected):
    from cpap_analysis import separate_list
    answer = separate_list(list_input)
    assert answer == expected


@pytest.mark.parametrize("patient_list, expected",
                         [(["Anne Boynton",
                            "7.25",
                            ["Seal", "11.0", "23.6", "15.2", "2.3",
                             "4.0", "19.7", "3.7"],
                            ["Events", "5", "0", "2", "3", "9", "1", "2"],
                            ["O2", "95", "93", "98", "97", "96", "97",
                             "100"]],
                           {"First Name": "Anne", "Last Name": "Boynton",
                            "Hours": 7.25,
                            "Seal": [11.0, 23.6, 15.2, 2.3,
                                     4.0, 19.7, 3.7],
                            "Events": [5, 0, 2, 3, 9, 1, 2],
                            "O2": [95, 93, 98, 97, 96, 97,
                                   100]})])
def test_create_patient_dict(patient_list, expected):
    from cpap_analysis import create_patient_dict
    answer = create_patient_dict(patient_list)
    assert answer == expected


@pytest.mark.parametrize("seal_list, hours, expected",
                         [([11.0, 23.6, 15.2, 2.3, 4.0, 19.7, 3.7],
                          7.25, 11.35714),
                          ([27.9, 13.3, 15.5, 7.5, 6.1, 15.8],
                          6.8, 14.35)])
def test_avg_leakage(seal_list, hours, expected):
    from cpap_analysis import avg_leakage
    answer = avg_leakage(seal_list, hours)
    assert answer == pytest.approx(expected)


@pytest.mark.parametrize("events_list, hours, expected",
                         [([5, 0, 2, 3, 9, 1, 2],
                          7.25, 3.14285714),
                          ([5, 6, 7, 1, 6, 0],
                          6.8, 4.16666667)])
def test_avg_events(events_list, hours, expected):
    from cpap_analysis import avg_events
    answer = avg_events(events_list, hours)
    assert answer == pytest.approx(expected)


@pytest.mark.parametrize("events, oxygen_list, expected",
                         [(3.14, [95, 93, 98, 97, 96, 97, 100],
                          "normal sleep"),
                          (6, [93, 93, 96, 99, 101, 94, 103],
                          "apnea"),
                          (4, [99, 91, 98, 92, 98, 95],
                          "hypoxia"),
                          (8.2, [94, 91, 96, 92, 93, 94],
                          "hypoxia apnea"),
                          (5, [95, 93, 98, 97, 96, 97, 100],
                          "normal sleep"),
                          (5, [99, 91, 98, 92, 98, 95],
                          "hypoxia")])
def test_patient_diagnosis(events, oxygen_list, expected):
    from cpap_analysis import patient_diagnosis
    answer = patient_diagnosis(events, oxygen_list)
    assert answer == expected


@pytest.mark.parametrize("pat_dict, avg_seal, diagnosis, expected",
                         [({"First Name": "Anne", "Last Name": "Boynton",
                            "Hours": 7.25,
                            "Seal": [11.0, 23.6, 15.2, 2.3,
                                     4.0, 19.7, 3.7],
                            "Events": [5, 0, 2, 3, 9, 1, 2],
                            "O2": [95, 93, 98, 97, 96, 97,
                                   100]}, 11.36, "normal sleep",
                           {"First Name": "Anne", "Last Name": "Boynton",
                            "Hours": 7.25,
                            "Seal": [11.0, 23.6, 15.2, 2.3,
                                     4.0, 19.7, 3.7],
                            "Events": [5, 0, 2, 3, 9, 1, 2],
                            "O2": [95, 93, 98, 97, 96, 97,
                                   100],
                            "Seal Average": 11.36,
                            "Diagnosis": "normal sleep"})])
def test_update_patient_dict(pat_dict, avg_seal, diagnosis, expected):
    from cpap_analysis import update_patient_dict
    answer = update_patient_dict(pat_dict, avg_seal, diagnosis)
    assert answer == expected
