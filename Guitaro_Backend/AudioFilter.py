import aubio


class AudioFilter:
    """
    Taken from https://github.com/aubio/aubio/blob/master/python/demos/demo_filter.py

    THIS IS NOT USED.
    This was used to try and clean up the users recording by removing high and low frequencies. It did not
    provide any improvement and in fact made the note detection worse.

    https://en.wikipedia.org/wiki/A-weighting
    """
    def __init__(self,path):
        self.path = path

    def apply_filter(self):
        # open input file, get its samplerate
        s = aubio.source(self.path)
        samplerate = s.samplerate

        # create an A-weighting filter
        f = aubio.digital_filter(7)
        f.set_a_weighting(samplerate)

        # create output file and replace original uploaded by user. Append the word filter to end of filename
        new_file_path = self.path[:-4]
        new_file_path += "_filter.wav"
        o = aubio.sink(new_file_path, samplerate)

        total_frames = 0
        while True:
            # read from source
            samples, read = s()
            # filter samples
            filtered_samples = f(samples)
            # write to sink
            o(filtered_samples, read)
            # count frames read
            total_frames += read
            # end of file reached
            if read < s.hop_size:
                break
