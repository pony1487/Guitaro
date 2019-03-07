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

fret_frequencies = [
    [82, 87, 92, 98, 103, 110, 116, 123, 130, 138, 146, 155, 164],
    [110, 116, 123, 130, 138, 146, 155, 164, 174, 185, 196, 207, 220],
    [146, 155, 164, 174, 185, 196, 207, 220, 233, 24, 261, 277, 293]
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
