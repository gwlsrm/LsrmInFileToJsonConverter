"""
    Parse lsrm in-files
"""

import config_parser
from constants import *


class InFileReader(config_parser.ConfigFileParser):
    def get_float_with_cm(self, key):
        value = self.get(key, default=0)
        if value:
            value = float(value.split()[0])
        return value

    def get_material(self, mat_name, prefix):
        elements_count_key = f"{prefix}n{mat_name}Elements"
        if elements_count_key not in self.data:
            elements_count_key = f"{prefix}n{mat_name}"
        elements_count = self.get(elements_count_key, cast_type=int)
        if not elements_count:
            raise RuntimeError(f"Invalid material {mat_name} with 0 elements count")
        rho = self.get(f"{prefix}Ro{mat_name}", cast_type=float)
        if rho < 0:
            raise RuntimeError(f"Material {mat_name} rho cannot be negative: {rho}")
        fraction_type = self.get(f"{prefix}FractionType{mat_name}")
        elements = []
        for i in range(elements_count):
            z = self.get(f"{prefix}Z{mat_name}[{i}]", cast_type=int)
            frac = self.get(f"{prefix}Fractions{mat_name}[{i}]", cast_type=float)
            elements.append({'z': z, 'frac': frac})
        return {'rho': rho, 'fraction_type': fraction_type, 'elements': elements}

    def get_file_type(self):
        if 'DetectorType' in self.data:
            return self.get('DetectorType')
        elif 'SourceType' in self.data:
            return self.get('SourceType')
        else:
            raise RuntimeError('Unknown file type')


def get_object_type(file_type):
    if file_type in ['COAXIAL', 'SCINTILLATOR', 'COAX_WELL']:
        return 'Detector'
    elif file_type in ['POINT', 'CYLINDER', 'MARINELLI', 'CONE']:
        return 'Source'


def parse_geometry(parser, file_type):
    prefix = FILE_TYPE_TO_PREFIX[file_type]
    return {geom_name: parser.get_float_with_cm(prefix+geom_name) for geom_name in FILE_TYPE_TO_GEOM_NAME[file_type]}


def parse_material(parser, file_type):
    prefix = FILE_TYPE_TO_PREFIX[file_type]
    return {mat_name: parser.get_material(mat_name, prefix) for mat_name in FILE_TYPE_TO_MAT_NAME[file_type]}
