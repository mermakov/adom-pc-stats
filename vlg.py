import re

starsign_dict = {
    'Raven':       1,
    'Book':        2,
    'Wand':        3,
    'Unicorn':     4,
    'Salamander':  5,
    'Dragon':      6,
    'Sword':       7,
    'Falcon':      8,
    'Cup':         9,
    'Candle':      10,
    'Wolf':        11,
    'Tree':        12
}

starsign_attr_modifier_rules = {
    'Raven':       { 'Pe':2 },
    'Book':        {},
    'Wand':        { 'Ch':2 },
    'Unicorn':     { 'Ap':2 },
    'Salamander':  { 'Ch':1, 'Ma':3 },
    'Dragon':      { 'To':1, 'St':2, 'Wi':-3 },
    'Sword':       { 'Le':1 },
    'Falcon':      { 'Wi':2, 'Ch':1 },
    'Cup':         { 'Le':2 },
    'Candle':      {},
    'Wolf':        { 'Wi':3 },
    'Tree':        { 'Wi':5 }
}

gender_attr_modifier_rules = {
    'male':        { 'St':1 },
    'female':      { 'Dx':1 }
}

age_attr_modifier_rules = {
    'grown-up':    { 'St':1, 'Wi':2, 'Le':2 },
    'young':       {}
}

corruption_dict = {
    'astral space':        1,
    'corrupted tissue':    2,
    'grown thorns':        3,
    'tough scales':        4,
    'grown horns':         5,
    'antennae explore':    6,
    '10 extra eyes':       7,
    'thin and nimble':     8,
    'unholy aura':         9,
    'rage':                10,
    'into hooves':         11,
    'mana battery':        12,
    'bulging cranium':     13,
    'very light':          14,
    'have stiffened':      15,
    'somewhat apish':      16,
    'fragile stilts':      17,
    'sport gills':         18,
    'freezingly cold':     19,
    'sweat blood':         20,
    'hate the sun':        21,
    'attached to ChAoS':   22,
    'mists of ChAoS':      23,
    'babbling mouth':      24,
    'voice of ChAoS':      25,
    'from bronze':         26,
    'tentacles':           27,
    'maggots':             28,
    'one larger eye':      29,
    'turned black':        30,
    'state of decay':      31,
    'flesh of Order':      32
}

corruption_rdict = {
    1:  'astral space',
    2:  'corrupted tissue',
    3:  'grown thorns',
    4:  'tough scales',
    5:  'grown horns',
    6:  'antennae explore',
    7:  '10 extra eyes',
    8:  'thin and nimble',
    9:  'unholy aura',
    10: 'rage',
    11: 'into hooves',
    12: 'mana battery',
    13: 'bulging cranium',
    14: 'very light',
    15: 'have stiffened',
    16: 'somewhat apish',
    17: 'fragile stilts',
    18: 'sport gills',
    19: 'freezingly cold',
    20: 'sweat blood',
    21: 'hate the sun',
    22: 'attached to ChAoS',
    23: 'mists of ChAoS',
    24: 'babbling mouth',
    25: 'voice of ChAoS',
    26: 'from bronze',
    27: 'tentacles',
    28: 'maggots',
    29: 'one larger eye',
    30: 'turned black',
    31: 'state of decay',
    32: 'flesh of Order'
}

corruption_attr_modifier_rules = {
    'astral space':        {},
    'corrupted tissue':    {},
    'grown thorns':        { 'Dx':-2, 'Ap':-3 },
    'tough scales':        { 'Dx':-6, 'Ap':-4 },
    'grown horns':         { 'Ap':-4 },
    'antennae explore':    { 'Ap':-4 },
    '10 extra eyes':       { 'Ap':-6, 'Pe':6 },
    'thin and nimble':     {},
    'unholy aura':         { 'Ch':-10 },
    'rage':                {},
    'into hooves':         { 'Dx':-6 },
    'mana battery':        {},
    'bulging cranium':     { 'Le':6, 'Wi':4, 'Ap':-6, 'To':-3 },
    'very light':          { 'St':-6, 'Dx':4, 'To':-6, 'Ap':-6 },
    'have stiffened':      { 'St':2 },
    'somewhat apish':      { 'St':3, 'Le':-1, 'Wi':-1, 'Ch':-2, 'Ap':-3 },
    'fragile stilts':      { 'Ap':-6 },
    'sport gills':         { 'Ap':-3 },
    'freezingly cold':     { 'Dx':-2, 'Ap':-6 },
    'sweat blood':         { 'Ch':-2, 'Ap':-4 },
    'hate the sun':        {},
    'attached to ChAoS':   {},
    'mists of ChAoS':      { 'Pe':-10 },
    'babbling mouth':      { 'Le':8, 'Ch':-6, 'Ap':-6, 'Pe':-4 },
    'voice of ChAoS':      { 'Le':4, 'Wi':-6, 'Ma':2 },
    'from bronze':         { 'Dx':-2 },
    'tentacles':           { 'Dx':6, 'Ap':-15 },
    'maggots':             { 'To':-6, 'Ch':-2, 'Ap':-4 },
    'one larger eye':      { 'Ch':-2, 'Ap':-2, 'Pe':4 },
    'turned black':        { 'Pe':3 },
    'state of decay':      { 'St':-5, 'Wi':10, 'Ap':-5 },
    'flesh of Order':      {}
}

corruption_pattern_s = ""
for corruption in corruption_dict.keys():
    corruption_pattern_s += "|" + corruption

def apply_attr_modifier_rule(attribute, rule):
    return (attribute[0], - rule.get(attribute[0], 0) + attribute[1])
    

starsign_pattern_s = ""
for starsign in starsign_dict.keys():
    starsign_pattern_s += "|" + starsign

starsign_pattern = re.compile(starsign_pattern_s[1:])
corruption_pattern = re.compile(corruption_pattern_s[1:])
skill_pattern = re.compile(r"[a-zA-Z ]* \.* [ \d]\d\s*\([a-z]*\)\s*\[\+[0-9d]*\]")
skill_parse_pattern = re.compile(r"([A-Z][a-zA-Z ]*[a-z])[ \.]*([0-9]+).*\[(.*)\]")
attribute_pattern = re.compile(r"[A-Z][a-z]:[ 0-9][0-9](?= )")
attribute_parse_pattern = re.compile(r"(Le|St|Wi|Dx|To|Ap|Ch|Ma|Pe)\:([ 0-9]*)")

alignment_pattern = re.compile(r"(?<=Pe:[ 0-9]{4})[LCN]")
gender_pattern = re.compile(r"(?<=Race: )[a-z]*")

age_pattern = re.compile(r"(?<=Age:).*")
age_parse_pattern = re.compile(r"\s*([0-9]*) \((.*)\)")

eye_color_pattern = re.compile(r"(?<=Eye color: )[a-z]*")
hair_color_pattern = re.compile(r"(?<=Hair color: )[a-z]*")
height_pattern = re.compile(r"(?<=Height: )[a-z\'\"]*")
complexion_pattern = re.compile(r"(?<=Complexion: )[a-z]*")

starsign_rdict = {
    1:    'Raven',
    2:    'Book',
    3:    'Wand',
    4:    'Unicorn',
    5:    'Salamander',
    6:    'Dragon',
    7:    'Sword',
    8:    'Falcon',
    9:    'Cup',
    10:   'Candle',
    11:   'Wolf',
    12:   'Tree'
}

history_dict = {
    'lower class':        1,
    'moderately well':    2,
    'is a guildmaster':   3,
    'humble shepherd':    4,
    'to the nobility':    5,
    'the middle class':   6,
    'Both are compet':    7,
    'were poor people':   8,
    'were often alone':   11,
    'ever-declining':     12,
    'cared a lot for':    13,
    'through happy':      14,
    'enjoyed your pre':   15,
    'everchanging':       16,
    'of your uncles':     17,
    'cruel parents':      18,
    'seriously ill':      21,
    'were very lazy':     22,
    'watched the adul':   23,
    'very active kid':    24,
    'center of inter':    25,
    'exploring woods':    26,
    'embarked on many':   27,
    'become rich and':    28,
    'left your home':     31,
    'renowned master':    32,
    'deeper meaning':     33,
    'with all means':     34,
    'clearly lying':      35,
    'steady determ':      36,
    'many occupations':   37,
    'a lot to finance':   38
}
    

history_rdict = {
    1:     'lower class',
    2:     'are travelling',
    3:     'is a guildmaster',
    4:     'humble shepherd',
    5:     'to the nobility',
    6:     'the middle class',
    7:     'Both are compet',
    8:     'were poor people',
    11:    'were often alone',
    12:    'ever-declining',
    13:    'cared a lot for',
    14:    'through happy',
    15:    'enjoyed your pre',
    16:    'everchanging',
    17:    'of your uncles',
    18:    'cruel parents',
    21:    'seriously ill',
    22:    'were very lazy',
    23:    'watched the adul',
    24:    'very active kid',
    25:    'center of inter',
    26:    'exploring woods',
    27:    'embarked on many',
    28:    'become rich and',
    31:    'left your home',
    32:    'renowned master',
    33:    'deeper meaning',
    34:    'with all means',
    35:    'clearly lying',
    36:    'steady determ',
    37:    'many occupations',
    38:    'a lot of finance'
}

history_pattern_s = ""
for history in history_dict.keys():
    history_pattern_s += "|" + history.replace(" ", "\s*")

history_pattern = re.compile(history_pattern_s[1:], )

def ss_to_int(starsign):
    return starsign_dict[starsign]

def int_to_ss(starsign):
    return starsign_rdict[starsign]

def hist_to_int(history):
    return history_dict[re.sub("\s+", " ", history)]

def int_to_hist(history):
    return history_rdict[history]

def parse_skills(contents):
    result = []
    skills = re.findall(skill_pattern, contents)
    for skill in skills:
        skill_mo = re.search(skill_parse_pattern, skill)
        result.append((skill_mo.group(1), int(skill_mo.group(2))))
    return result


def parse_attributes(contents):
    result = []
    for attribute in re.findall(attribute_pattern, contents):
        attribute_mo = re.search(attribute_parse_pattern, attribute)
        attr = (attribute_mo.group(1), int(attribute_mo.group(2)))
        if not attr in result:
            result.append(attr)
    return result

def parse_age(contents):
    age = re.search(age_pattern, contents).group(0)
    return re.search(age_parse_pattern, age).groups()


class Vlg:

    def __init__(self,contents):
        self.starsign = re.search(starsign_pattern, contents).group(0)
        self.skills = parse_skills(contents)
        self.attributes = parse_attributes(contents)
        self.alignment = re.search(alignment_pattern, contents).group(0)
        (self.age, self.age_group) = parse_age(contents)
        self.gender = re.search(gender_pattern, contents).group(0)
        self.history = []
        for history in re.findall(history_pattern, contents):
            self.history.append(hist_to_int(history))
        self.eye_color = re.search(eye_color_pattern, contents).group(0)
        self.hair_color = re.search(hair_color_pattern, contents).group(0)
        self.height = re.search(height_pattern, contents).group(0)
        self.complexion = re.search(complexion_pattern, contents).group(0)
        self.corruptions = []
        for corruption in re.findall(corruption_pattern, contents):
            self.corruptions.append(corruption)

    def get_base_attributes(self):
        result = []
        for attribute in self.attributes:
            attr = apply_attr_modifier_rule(attribute, starsign_attr_modifier_rules[self.starsign])
            attr = apply_attr_modifier_rule(attr, age_attr_modifier_rules[self.age_group])
            attr = apply_attr_modifier_rule(attr, gender_attr_modifier_rules[self.gender])
            for corruption in self.corruptions:
                attr = apply_attr_modifier_rule(attr, corruption_attr_modifier_rules[corruption])
            if (attr[0] == 'St') or (attr[0] == 'To') or (attr[0] == 'Dx') or (attr[0] == 'Ma'):
                attr = (attr[0], attr[1] - len(self.corruptions) / { 'C':2, 'N':3, 'L':4 }[self.alignment])
            if attr[0] == 'Wi':
                attr = (attr[0], attr[1] + len(self.corruptions) / { 'C':2, 'N':3, 'L':4 }[self.alignment])
                if (self.starsign == 'Wand') and (self.alignment == 'N'):
                    attr = (attr[0], attr[1] - 2)
            result.append(attr)

        return result    
