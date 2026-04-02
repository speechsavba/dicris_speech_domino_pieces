# -*- coding: utf-8 -*-
# Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.
# Copyright (c) 2013, Savoir-faire Linux inc.  All Rights Reserved.

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA

from __future__ import unicode_literals

from .base import Num2Word_Base
from .utils import get_digits, splitbyx

ZERO = ('nula',)

ONES_FEMININE = {
    1: ('jedna',),
    2: ('dve',),
    3: ('tri',),
    4: ('štyri',),
    5: ('päť',),
    6: ('šesť',),
    7: ('sedem',),
    8: ('osem',),
    9: ('deväť',),
}

ONES = {
    1: ('jeden',),
    2: ('dva',),
    3: ('tri',),
    4: ('štyri',),
    5: ('päť',),
    6: ('šesť',),
    7: ('sedem',),
    8: ('osem',),
    9: ('deväť',),
}

ONES_ORDINALS = {
    1: ("prvý", "prvého"),
    2: ("druhý", "druhého"),
    3: ("tretí", "tretieho"),
    4: ("štvrtý", "štvrtého"),
    5: ("piaty", "piateho"),
    6: ("šiesty", "šiesteho"),
    7: ("siedmy", "siedmeho"),
    8: ("ôsmy", "ôsmeho"),
    9: ("deviaty", "deviateho"),
    10: ("desiaty", "desiateho"),
    11: ("jedenásty", "jedenásteho"),
    12: ("dvanásty", "dvanásteho"),
    13: ("trinásty", "trinásteho"),
    14: ("štrnásty", "štrnásteho"),
    15: ("pätnásty", "pätnásteho"),
    16: ("šestnásty", "šestnásteho"),
    17: ("sedemnásty", "sedemnásteho"),
    18: ("osemnásty", "osemnásteho"),
    19: ("devätnásty", "devätnásteho"),
}

TENS = {
    0: ('desať',),
    1: ('jedenásť',),
    2: ('dvanásť',),
    3: ('trinásť',),
    4: ('štrnásť',),
    5: ('pätnásť',),
    6: ('šestnásť',),
    7: ('sedemnásť',),
    8: ('osmnásť',),
    9: ('devätnásť',),
}

TWENTIES = {
    2: ('dvadsať',),
    3: ('tridsať',),
    4: ('štyridsať',),
    5: ('päťdesiat',),
    6: ('šesťdesiat',),
    7: ('sedemdesiat',),
    8: ('osemdesiat',),
    9: ('deväťdesiat',),
}

TWENTIES_ORDINALS = {
    2: ("dvadsiaty", "dvadsiateho"),
    3: ("tridsiaty", "tridsiateho"),
    4: ("štyridsiaty", "štyridsiateho"),
    5: ("päťdesiaty", "päťdesiateho"),
    6: ("šestdesiaty", "šestdesiateho"),
    7: ("sedemdesiaty", "sedemdesiateho"),
    8: ("osemdesiaty", "osemdesiateho"),
    9: ("deväťdesiaty", "deväťdesiateho"),
}

HUNDREDS = {
    1: ('sto',),
    2: ('dvesto',),
    3: ('tristo',),
    4: ('štyristo',),
    5: ('päťsto',),
    6: ('šesťsto',),
    7: ('sedemsto',),
    8: ('osemsto',),
    9: ('deväťsto',),
}

HUNDREDS_ORDINALS = {
    1: ("sto", "sto"),
    2: ("dvesto", "dvesto"),
    3: ("tristo", "tristo"),
    4: ("štyristo", "štyristo"),
    5: ("päťsto", "päťsto"),
    6: ("šesťsto", "šesťsto"),
    7: ("sedemsto", "sedemsto"),
    8: ("osemsto", "osemsto"),
    9: ("deväťsto", "deväťsto"),
}


THOUSANDS = {
    1: ('tisíc', 'tisíce', 'tisíc'),  # 10^3
    2: ('milión', 'milióny', 'miliónov'),  # 10^6
    3: ('miliarda', 'miliardy', 'miliárd'),  # 10^9
    4: ('bilión', 'bilióny', 'biliónov'),  # 10^12
    5: ('biliarda', 'biliardy', 'biliárd'),  # 10^15
    6: ('trilión', 'trilióny', 'triliónov'),  # 10^18
    7: ('triliarda', 'triliardy', 'triliárd'),  # 10^21
    8: ('kvadrilión', 'kvadrilióny', 'kvadriliónov'),  # 10^24
    9: ('kvadriliarda', 'kvadriliardy', 'kvadriliárd'),  # 10^27
    10: ('kvintilión', 'kvintilióny', 'kvintiliónov'),  # 10^30
}


prefixes_ordinal = {
    1: "tisící",
    2: "miliontý",
}

class Num2Word_SK(Num2Word_Base):
    CURRENCY_FORMS = {
        'EUR': (
            ('euro', 'euro', 'euro'), ('cent', 'centy', 'centů')
        ),
        'SK': (
            ('koruna', 'koruny', 'korún'), ('halier', 'haliere', 'haliero')
        ),
    }

    def setup(self):
        self.negword = "mínus"
        self.pointword = "celá"

    def to_cardinal(self, number):
        n = str(number).replace(',', '.')
        if '.' in n:
            left, right = n.split('.')
            leading_zero_count = len(right) - len(right.lstrip('0'))
            decimal_part = ((ZERO[0] + ' ') * leading_zero_count +
                            self._int2word(int(right)))
            return u'%s %s %s' % (
                self._int2word(int(left)),
                self.pointword,
                decimal_part
            )
        else:
            return self._int2word(int(n))

    def pluralize(self, n, forms):
        if n == 1:
            form = 0
        elif 5 > n % 10 > 1 and (n % 100 < 10 or n % 100 > 20):
            form = 1
        else:
            form = 2
        return forms[form]

    @staticmethod
    def last_fragment_to_ordinal(last, words, level):
        print(last,words,level)		
        n1, n2, n3 = get_digits(last)
        print(n1,n2,n3)				
        last_two = n2*10+n1
        if last_two == 0:
            print('last_two')				
            words.append(HUNDREDS_ORDINALS[n3][level])
        elif level == 1 and last == 1:
            return
        elif last_two < 20:
            if level == 0:
                if n3 > 0:
                    words.append(HUNDREDS_ORDINALS[n3][0])
                words.append(ONES_ORDINALS[last_two][0])
            else:
                last_fragment_string = ''
                if n3 > 0:
                    last_fragment_string += HUNDREDS_ORDINALS[n3][1]
                last_fragment_string += ONES_ORDINALS[last_two][1]
                words.append(last_fragment_string)
        elif last_two % 10 == 0:
            if level == 0:
                if n3 > 0:
                    words.append(HUNDREDS_ORDINALS[n3][0])
                words.append(TWENTIES_ORDINALS[n2][0])
            else:
                last_fragment_string = ''
                if n3 > 0:
                    last_fragment_string += HUNDREDS_ORDINALS[n3][1]
                last_fragment_string += TWENTIES_ORDINALS[n2][1]
                words.append(last_fragment_string)
        else:
            if level == 0:
                if n3 > 0:
                    words.append(HUNDREDS_ORDINALS[n3][0])
                words.append(TWENTIES_ORDINALS[n2][0])
                words.append(ONES_ORDINALS[n1][0])
            else:
                last_fragment_string = ''
                if n3 > 0:
                    last_fragment_string += HUNDREDS_ORDINALS[n3][1]
                last_fragment_string += TWENTIES_ORDINALS[n2][1]
                last_fragment_string += ONES_ORDINALS[n1][1]
                words.append(last_fragment_string)

    def to_ordinal(self, number):
        self.verify_ordinal(number)

        words = []
        fragments = list(splitbyx(str(number), 3))
        level = 0
        last = fragments[-1]
        while last == 0:
            level = level + 1
            fragments.pop()
            last = fragments[-1]
        if len(fragments) > 1:
            pre_part = self._int2word(number - (last * 1000 ** level))
            words.append(pre_part)
        Num2Word_SK.last_fragment_to_ordinal(
            last,
            words,
            0 if level == 0 else 1
        )
        output = " ".join(words)
        if last == 1 and level > 0 and output != "":
            output = output + " "
        if level > 0:
            output = output + prefixes_ordinal[level]
        return output

    def _int2word(self, n):
        if n == 0:
            return ZERO[0]

        words = []
        chunks = list(splitbyx(str(n), 3))
        i = len(chunks)
        for x in chunks:
            i -= 1

            if x == 0:
                continue

            n1, n2, n3 = get_digits(x)

            if n3 > 0:
                words.append(HUNDREDS[n3][0])

            if n2 > 1:
                words.append(TWENTIES[n2][0])

            if n2 == 1:
                words.append(TENS[n1][0])
            elif n1 > 0 and not (i > 0 and x == 1):
                words.append(ONES[n1][0])

            if i > 0:
                words.append(self.pluralize(x, THOUSANDS[i]))

        return ' '.join(words)
