'''
Converts anb template to gedcom and gedcom to anbtemplate
'''
def parse_gedcom_file(file_path):
    individuals = {}
    families = {}

    with open(file_path, 'r') as gedcom_file:
        current_individual = None
        current_family = None

        for line in gedcom_file:
            level, tag, value = parse_gedcom_line(line)

            if tag == 'INDI':
                current_individual = value
                individuals[value] = {
                    'name': '',
                    'birth_date': '',
                    'spouse': None,
                    'child': None
                }
            elif tag == 'FAM':
                current_family = value
                families[value] = {
                    'husband': None,
                    'wife': None,
                    'children': []
                }
            elif tag == 'NAME':
                if current_individual is not None:
                    individuals[current_individual]['name'] = value
            elif tag == 'BIRT':
                if current_individual is not None:
                    individuals[current_individual]['birth_date'] = value
            elif tag == 'MARR':
                if current_family is not None:
                    families[current_family]['marriage_date'] = value
            elif tag == 'HUSB':
                if current_family is not None:
                    families[current_family]['husband'] = value
                    individuals[value]['spouse'] = current_family
            elif tag == 'WIFE':
                if current_family is not None:
                    families[current_family]['wife'] = value
                    individuals[value]['spouse'] = current_family
            elif tag == 'CHIL':
                if current_family is not None:
                    families[current_family]['children'].append(value)
                    individuals[value]['child'] = current_family

    return individuals, families



def parse_gedcom_line(line):
    if line.strip():
        level = int(line[0])
        parts = line.strip().split(' ', 2)
        tag = parts[1]
        value = parts[2] if len(parts) > 2 else ''
        return level, tag, value
    else:
        return None, None, None


def convert_to_custom_format(individuals, families):
    custom_format = ''

    for individual_id, individual in individuals.items():
        name = individual['name']
        birth_date = individual['birth_date']
        spouse = individual['spouse']
        child = individual['child']

        custom_format += f'{name} ({birth_date})\n'

        if spouse is not None:
            custom_format += f'+ {spouse}\n'

        if child is not None:
            custom_format += f'.#{child}\n'

    for family_id, family in families.items():
        husband = family['husband']
        wife = family['wife']
        children = family['children']
        marriage_date = family.get('marriage_date')

        if husband is not None and wife is not None:
            custom_format += f'\n{husband} + {wife}'

            if marriage_date is not None:
                custom_format += f' ({marriage_date})'

        if children:
            for child in children:
                custom_format += f'\n.{child}'

        custom_format += '\n'

    return custom_format

gedcom_file_path = 'gedcom.ged'
individuals, families = parse_gedcom_file(gedcom_file_path)
custom_format = convert_to_custom_format(individuals, families)
print(custom_format)