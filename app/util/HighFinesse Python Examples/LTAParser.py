"""Longterm array parser class + example usage code"""

import matplotlib.pyplot as plt
import numpy as np

class LTAParser(): # pylint: disable=too-few-public-methods
    """Parse a .lta file into a numpy array and a header line"""
    def __init__(self, fname):
        with open(fname, encoding='utf_8') as f: # open the file for reading
            m_data = False
            act_line = 0
            data = []
            self.headerinfo = []
            for line in f:
                # Remove the new line at the end and then split the string based on
                # tabs. This creates a python list of the values.
                #print(line.encode())
                if act_line == 2:
                    # Extract the header from the data
                    self.headerline = line.replace(',', '.').strip('\n').split('\t')
                if act_line > 2:
                    # Extract the data from the file
                    values = line.replace(',', '.').strip('\n').split('\t')
                    vals = []
                    for v in values:
                        try:
                            val = float(v)
                            if v != '':
                                vals.append(val)
                            else:
                                vals.append(np.nan)
                        except ValueError:
                            vals.append(np.nan)
                    data.append(vals)
                else:
                    self.headerinfo.append(line)
                if line.strip() == '[Measurement data]': # Start of Measurement data
                    m_data = True
                if m_data:
                    act_line += 1
            self.data = np.array(data[1:])

    def export2csv(self, filename, separator=','):
        """Convert the parsed .lta to a .csv with a header line"""
        np.savetxt(filename, self.data, header=separator.join(self.headerline), delimiter=separator)

if __name__ == '__main__':
    file_name = 'SLR 4338.lta'

    # Load the desired LTA file to an instance of LTAParser
    data = LTAParser(file_name)

    # Search for desired column in the data by searching for the proper header entry
    t_index = data.headerline.index('Time  [ms]')
    # Extract the corresponding data
    t = data.data[:,t_index]

    # Search for desired column in the data by searching for the proper header entry
    data1_index = data.headerline.index('Signal 1  Wavelength. vac.  [nm]')
    # Extract the corresponding data
    data1 = data.data[:,data1_index]

    # Plot
    plt.plot(t, data1)
