import numpy as np

"""
This is testing an algo for determing what was played on what string and limiting it by how
far apart the notes are

This algorithm goes through each list(frequencies for each note on a string) and finds the index(fret) of where it was
played.
It keeps track of what frequencies(notes) have been seen.
A frequency will be added to the seen list if the distance between the first note played on the string and the next
note is note greater than 5 frets.
The first note changes each string based on whether it whats in the seen list.

For example, the pattern

A C D E G A should look like this. It was how it was played originally in the lesson and with the distance check this
is produced.

-----------------------
-----------------------
-----------------------
------------5--7-------
------5--7-------------
-5--8------------------

Without checking if the distance between notes is greater than 5

-----------------------
-----------------------
-----------------------
-----------------------
-------------10-12-----
-5--8--10-12------------

The above is still correct and should be viewed as an alternative way to play it.

The first note on each new string changes based on the length of the seen list
For example:

freqs = [110,130,146,164,196,220]

seen = [110,130]

len(seen) # 2
freqs[2] # 146

The algorithm will ignore the A note(110), open string 5th string and C note(130) 3rd fret 5th string
start at that 5th fret(146hz)
"""
# Low E to High e
fret_frequencies = [
    [82.41, 87.31, 92.50, 98.00, 103.83, 110.00, 116.54, 123.47, 130.81, 138.59, 146.83, 155.56, 164.81],
    [110.00, 116.54, 123.47, 130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00],
    [146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00, 233.08, 246.94, 261.63, 277.18, 293.66],
    [196.00, 207.65, 220.00, 233.08, 246.94, 261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00],
    [246.94, 261.63, 277.18, 293.66,311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88],
    [329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88, 523.25, 554.37, 587.33, 622.25, 659.25]
]

"""
Guitar strings 6 is the lowest/thickest. Its easier to traverse the 2d array with the 6th string as the first list etc
"""
fret_frequencies_to_string_number_mapping = {
    "0": "6",
    "1": "5",
    "2": "4",
    "3": "3",
    "4": "2",
    "5": "1"
}

max_fret_distance = 5

seen = list()

# Pentatonic
# notes_in_recording = ['A','C','D','E','G','A']
# freq_in_recording = [110,130,146,164,196,220]

# Natural Minor
notes_in_recording = ['A', 'B', 'C', 'D', 'E', 'F']
freq_in_recording = [110, 123, 130, 146, 164, 174]

for i in range(0, len(fret_frequencies)):
    string = fret_frequencies[i]

    index_to_base_diff_off = len(seen)
    fret_of_next_start_note = 0

    if index_to_base_diff_off < len(freq_in_recording):
        # print(freq_in_recording[index_to_base_diff_off])
        # print("len of seen: " + str(index_to_base_diff_off))

        freq_of_next_start_note = freq_in_recording[index_to_base_diff_off]
        fret_of_next_start_note = string.index(freq_of_next_start_note)

        string_num = fret_frequencies_to_string_number_mapping.get(str(i))
        print("String number: " + string_num)
        print("Fret of start note on new string: " + str(fret_of_next_start_note))
        next_start_fret = index_to_base_diff_off

    for j in range(0, len(freq_in_recording)):

        freq = freq_in_recording[j]
        if freq in string:
            if freq not in seen:
                fret = string.index(freq)
                diff = fret - fret_of_next_start_note
                s = "fret {} - {} = {}".format(fret, fret_of_next_start_note, diff)
                # print(s)
                if diff < max_fret_distance:
                    seen.append(freq)
                    print(str(fret) + " ", end="")

    print("\n")

print(seen)

print("--------------------")
# Notated for single string to 12 fret
# Prints each fret the note occes ie 5 8 10 12 for E, 0 3 5 7 10 12 etc
for i in range(0, len(fret_frequencies)):
    string = fret_frequencies[i]

    for j in range(0, len(freq_in_recording)):
        # set to the first note in the recording
        first_freq = freq_in_recording[j]
        if first_freq in string:
            fret = string.index(first_freq)
            print(str(fret) + " ", end="")
    print("\n")

"""
# Partially works
for i in range(0, len(fret_frequencies)):
  string = fret_frequencies[i]

  for j in range(0,len(freq_in_recording)):
    # set to the first note in the recording
    first_freq = freq_in_recording[j]
    if first_freq in string:
      if first_freq not in seen:
        fret = string.index(first_freq)
        seen.append(first_freq)
        print(str(fret) + " ",end="")
  print("\n")

print(seen)
"""


def find_nearest(array, value):
    array = np.asarray(array)
    index = (np.abs(array - value)).argmin()
    print(array[index])


"""
Below is a working version for floats
"""


"""

import numpy as np

strings = [
    [82.41, 87.31, 92.50, 98.00, 103.83, 110.00, 116.54, 123.47, 130.81, 138.59, 146.83, 155.56, 164.81],
    [110.00, 116.54, 123.47, 130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00],
    [146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00, 233.08, 246.94, 261.63, 277.18, 293.66],
    [196.00, 207.65, 220.00, 233.08, 246.94, 261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00],
    [246.94, 261.63, 277.18, 293.66,311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88],
    [329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88, 523.25, 554.37, 587.33, 622.25, 659.25]
]

fret_frequencies_to_string_number_mapping = {
    "0": "6",
    "1": "5",
    "2": "4",
    "3": "3",
    "4": "2",
    "5": "1"
}


# Pentatonic
#notes_in_recording = ['A','C','D','E','G','A']
#freq_in_recording = [110,130,146,164,196,220]


# Natural Minor
notes_in_recording = ['A', 'B', 'C', 'D', 'E', 'F']
freq_in_recording = [110, 123, 130, 146, 164, 174]


max_fret_distance = 5
seen = list()

#print(len(seen))
next_start_point = len(seen)

#print(freqs[next_start_point])

def find_nearest(array, value):
    array = np.asarray(array)
    index = (np.abs(array - value)).argmin()
    return array[index]



for i in range(0, len(strings)):
    string = strings[i]

    index_to_base_diff_off = len(seen)
    fret_of_next_start_note = 0

    #print("index_to_base_diff_off: " + str(index_to_base_diff_off))
    # Dont overshoot list
    if index_to_base_diff_off < len(freq_in_recording):
        # print(freq_in_recording[index_to_base_diff_off])
        # print("len of seen: " + str(index_to_base_diff_off))

        freq_of_next_start_note = freq_in_recording[index_to_base_diff_off]
        # As the frequencies in the string are floats and the recording gives ints the #nearest has to be found to get fret of the nex start not
        nearest_freq = find_nearest(string,freq_of_next_start_note)
        
        fret_of_next_start_note = string.index(nearest_freq)
        s = "index_to_base_diff_off:{} freq_of_next_start_note:{} nearest_freq: {} fret_of_next_start_note: {}".format(index_to_base_diff_off,freq_of_next_start_note,nearest_freq,fret_of_next_start_note)
        #print(s)
        
        string_num = fret_frequencies_to_string_number_mapping.get(str(i))
        print("String number: " + string_num)

    for j in range(0, len(freq_in_recording)):

        freq = freq_in_recording[j]
        nearest = find_nearest(string,freq)
        if not (nearest - freq) > 5.00:
          #print(freq)
          if nearest in string:
              if freq not in seen:
                fret = string.index(nearest)
                #print(fret)
                #s = "fret: {} nearest: {}".format(fret, nearest)
                #print(s)
                diff = fret - fret_of_next_start_note
                s2 = "fret {} - {} = {}".format(fret, fret_of_next_start_note, diff)
                #print(s2)

                if diff < max_fret_distance and not diff < 0:
                  seen.append(freq)
                  print(str(fret) + " ", end="")

    print("\n")

print(seen)
"""

"""
A working version for multiple occurances of the same note on the same string-ascending
"""

"""

import numpy as np

strings = [
    [82.41, 87.31, 92.50, 98.00, 103.83, 110.00, 116.54, 123.47, 130.81, 138.59, 146.83, 155.56, 164.81],
    [110.00, 116.54, 123.47, 130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00],
    [146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00, 233.08, 246.94, 261.63, 277.18, 293.66],
    [196.00, 207.65, 220.00, 233.08, 246.94, 261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00],
    [246.94, 261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88],
    [329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88, 523.25, 554.37, 587.33, 622.25, 659.25]
]

fret_frequencies_to_string_number_mapping = {
    "0": "6",
    "1": "5",
    "2": "4",
    "3": "3",
    "4": "2",
    "5": "1"
}

###############################################################

#TESTS

# Pentatonic ascending
# notes_in_recording = ['A','C','D','E','G','A']
# freq_in_recording = [110,130,146,164,196,220]


# Pentatonic ascending and descending
# notes_in_recording = ['A','C','D','E','G','A','G','E','D','C','A']
# freq_in_recording = [110,130,146,164,196,220,196,164,146,130,100]

# Pentonic Descending
# notes_in_recording = ['A','G','E','D','C','A']
# freq_in_recording = [220,196,164,146,130,110]

# freq_in_recording = list(reversed(freq_in_recording))

# Descding with multiple notes occuring on each string
# notes_in_recording = ['A','G','A','G','E','D','A','G','E','D','C','A']
# freq_in_recording = [220,196,220,196,164,146,20,196,164,146,130,110]

# print(list(reversed(notes_in_recording)))
# freq_in_recording = list(reversed(freq_in_recording))

# Same note occurs multiple times on per string
# notes_in_recording = ['A','C','A','C','D','E','D','E','G','A']
# freq_in_recording = [110,130,110,130,146,164,146,164,196,220]

# freq_in_recording = list(reversed(freq_in_recording))
# print(freq_in_recording)

# Natural Minor
notes_in_recording = ['A', 'B', 'C', 'B', 'A' 'D', 'E', 'F']
freq_in_recording = [110, 123, 130, 123, 110, 146, 164, 174]

#######################################################################################
max_fret_distance = 5
# use this to store the notes that occur per string
string_seen_buf = list()
# when changing string turn this into a set to remove duplicates to
# that the notes that have occured on the previous string dont get 
# counted on the the next string
seen = list()

# print(len(seen))
next_start_point = len(seen)


# print(freqs[next_start_point])

def find_nearest(array, value):
    array = np.asarray(array)
    index = (np.abs(array - value)).argmin()
    return array[index]


for i in range(0, len(strings)):
    string = strings[i]

    # This will be the start point on the next string
    index_to_base_diff_off = len(string_seen_buf)
    fret_of_next_start_note = 0

    # Dont overshoot list
    if index_to_base_diff_off < len(freq_in_recording):
        freq_of_next_start_note = freq_in_recording[index_to_base_diff_off]
        # As the frequencies in the string are floats and the recording gives ints the #nearest has to be found to get fret of the nex start not
        nearest_freq = find_nearest(string, freq_of_next_start_note)

        fret_of_next_start_note = string.index(nearest_freq)
        s = "index_to_base_diff_off:{} freq_of_next_start_note:{} nearest_freq: {} fret_of_next_start_note: {}".format(
            index_to_base_diff_off, freq_of_next_start_note, nearest_freq, fret_of_next_start_note)
        # print(s)

        string_num = fret_frequencies_to_string_number_mapping.get(str(i))
        print("String number: " + string_num)

    for j in range(0, len(freq_in_recording)):

        freq = freq_in_recording[j]
        if freq < max(string):
            nearest = find_nearest(string, freq)
            if nearest not in seen:

                if not (nearest - freq) > 5.00:

                    if nearest in string:

                        debug_str = "freq:{} nearest:{}".format(freq, nearest)
                        # print(debug_str)

                        fret = string.index(nearest)
                        # print(fret)
                        # s = "fret: {} nearest: {}".format(fret, nearest)
                        # print(s)
                        diff = fret - fret_of_next_start_note
                        s2 = "fret {} - {} = {}".format(fret, fret_of_next_start_note, diff)
                        # print(s2)

                        if diff < max_fret_distance and not diff < 0:
                            string_seen_buf.append(nearest)
                            print(str(fret) + " ", end="")
    seen = set(string_seen_buf)
    print("\n")

print(string_seen_buf)
print(seen)
###################################################################################
"""