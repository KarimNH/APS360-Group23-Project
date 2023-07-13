seizures_info = {}

def Filenames(filename):
    # open file 
    with open(filename) as f:
        lines = f.readlines() 

    name = ""
    start = 0 
    for idx, line in enumerate(lines): 
        if "Name:" in line.split():
            name = line.split()[2]
        if "Start" in line.split() and "seconds" in line.split():
            start = line.split()[-2]
        if "End" in line.split() and "seconds" in line.split():
            if name in seizures_info:
                seizures_info[name] += [(int(start), int(line.split()[-2]))]
            else:
                seizures_info[name] = [(int(start), int(line.split()[-2]))]

def DetectSeizure(filename, window_start_time, window_end_time):
    time = (window_start_time+window_end_time)/2 # 50% of the window 
    if filename not in seizures_info:
        return False
    seizure = False
    for i in range(len(seizures_info[filename])):
        seizure |= time <= seizures_info[filename][i][1] and time >= seizures_info[filename][i][0]
    return seizure      

Filenames("..\Data\PatientSummary\PatientsSummary.txt")



