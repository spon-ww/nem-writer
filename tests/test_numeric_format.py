import os
import sys
import datetime
import csv
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
from nemwriter import NEM12


def test_numeric_format():
    """ IntervalValue can contain decimal points, but NOT exponents.
    """
    m = NEM12(to_participant='123')
    readings = [[datetime.datetime(2004, 4, 18, 0, 0) + datetime.timedelta(minutes=30 * (i + 1)),
                 10**-i,
                 'A'] for i in range(24 * 2)]
    m.add_readings(nmi='123',
                   nmi_configuration='E1B1B2',
                   nmi_suffix='E1', uom='kWh',
                   interval_length=30,
                   readings=readings)
    output_filename = "tests/test_output_numeric_format.csv"
    m.nem_output(file_name=output_filename)

    with open(output_filename, newline="") as fin:
        reader = csv.reader(fin)
        for row in reader:
            if row[0] == '300':
                interval_readings = row[2:-5]
                for reading in interval_readings:
                    assert "e" not in reading
