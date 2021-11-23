import sys
import os.path
import json
from infile_reader import InFileReader, parse_geometry, get_object_type, parse_material, parse_anal_params


def _getoutput_file_name(input_filename):
    fname, ext = os.path.splitext(input_filename)
    return fname + '.json'


def convert_in_to_json(parser, file_type):
    object_type = get_object_type(file_type)
    if object_type in ('Detector', 'Source'):
        res = {
            object_type: {
                'Type': file_type,
                'Geometry':
                    parse_geometry(parser, file_type),
                'Material':
                    parse_material(parser, file_type),
            }
        }
    elif object_type == 'Analyzer':
        res = {
            object_type: parse_anal_params(parser),
        }
    return res


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print('converter <infile.in>')
        sys.exit()

    file_name = sys.argv[1]
    out_file_name = _getoutput_file_name(file_name)
    parser = InFileReader(file_name)
    file_type = parser.get_file_type()
    output_json = convert_in_to_json(parser, file_type)
    with open(out_file_name, 'w') as f:
        json.dump(output_json, f, indent=4)
