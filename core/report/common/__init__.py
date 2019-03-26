import os

RELATIVE_XLS_URI = '../../../resources/data/profile_data_structure_template.xlsx' # noqa E501
XLS_URI = os.path.abspath(
    os.path.join(os.path.abspath(__file__), RELATIVE_XLS_URI),
)
SHT_RESERVE_CHAR = '#'
ZERO_DEFAULT = '-'
