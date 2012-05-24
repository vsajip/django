# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.localflavor.hr.forms import (HRCountySelect,
    HRPhoneNumberPrefixSelect, HRLicensePlatePrefixSelect, HRPhoneNumberField,
    HRLicensePlateField, HRPostalCodeField, HROIBField, HRJMBGField,
    HRJMBAGField)

from django.test import SimpleTestCase

class HRLocalFlavorTests(SimpleTestCase):
    def test_HRCountySelect(self):
        f = HRCountySelect()
        out = '''<select name="county">
<option value="GZG" selected="selected">Grad Zagreb</option>
<option value="BB\u017d">Bjelovarsko-bilogorska \u017eupanija</option>
<option value="BP\u017d">Brodsko-posavska \u017eupanija</option>
<option value="DN\u017d">Dubrova\u010dko-neretvanska \u017eupanija</option>
<option value="I\u017d">Istarska \u017eupanija</option>
<option value="K\u017d">Karlova\u010dka \u017eupanija</option>
<option value="KK\u017d">Koprivni\u010dko-kri\u017eeva\u010dka \u017eupanija</option>
<option value="KZ\u017d">Krapinsko-zagorska \u017eupanija</option>
<option value="LS\u017d">Li\u010dko-senjska \u017eupanija</option>
<option value="M\u017d">Me\u0111imurska \u017eupanija</option>
<option value="OB\u017d">Osje\u010dko-baranjska \u017eupanija</option>
<option value="PS\u017d">Po\u017ee\u0161ko-slavonska \u017eupanija</option>
<option value="PG\u017d">Primorsko-goranska \u017eupanija</option>
<option value="SM\u017d">Sisa\u010dko-moslava\u010dka \u017eupanija</option>
<option value="SD\u017d">Splitsko-dalmatinska \u017eupanija</option>
<option value="\u0160K\u017d">\u0160ibensko-kninska \u017eupanija</option>
<option value="V\u017d">Vara\u017edinska \u017eupanija</option>
<option value="VP\u017d">Viroviti\u010dko-podravska \u017eupanija</option>
<option value="VS\u017d">Vukovarsko-srijemska \u017eupanija</option>
<option value="ZD\u017d">Zadarska \u017eupanija</option>
<option value="ZG\u017d">Zagreba\u010dka \u017eupanija</option>
</select>'''
        self.assertHTMLEqual(f.render('county', 'GZG'), out)

    def test_HRPhoneNumberPrefixSelect(self):
        f = HRPhoneNumberPrefixSelect()
        out = '''<select name="phone">
<option value="1" selected="selected">01</option>
<option value="20">020</option>
<option value="21">021</option>
<option value="22">022</option>
<option value="23">023</option>
<option value="31">031</option>
<option value="32">032</option>
<option value="33">033</option>
<option value="34">034</option>
<option value="35">035</option>
<option value="40">040</option>
<option value="42">042</option>
<option value="43">043</option>
<option value="44">044</option>
<option value="47">047</option>
<option value="48">048</option>
<option value="49">049</option>
<option value="51">051</option>
<option value="52">052</option>
<option value="53">053</option>
<option value="91">091</option>
<option value="92">092</option>
<option value="95">095</option>
<option value="97">097</option>
<option value="98">098</option>
<option value="99">099</option>
</select>'''
        self.assertHTMLEqual(f.render('phone', '1'), out)

    def test_HRLicensePlatePrefixSelect(self):
        f = HRLicensePlatePrefixSelect()
        out = '''<select name="license">
<option value="BJ" selected="selected">BJ</option>
<option value="BM">BM</option>
<option value="\u010cK">\u010cK</option>
<option value="DA">DA</option>
<option value="DE">DE</option>
<option value="DJ">DJ</option>
<option value="DU">DU</option>
<option value="GS">GS</option>
<option value="IM">IM</option>
<option value="KA">KA</option>
<option value="KC">KC</option>
<option value="KR">KR</option>
<option value="KT">KT</option>
<option value="K\u017d">K\u017d</option>
<option value="MA">MA</option>
<option value="NA">NA</option>
<option value="NG">NG</option>
<option value="OG">OG</option>
<option value="OS">OS</option>
<option value="PU">PU</option>
<option value="P\u017d">P\u017d</option>
<option value="RI">RI</option>
<option value="SB">SB</option>
<option value="SK">SK</option>
<option value="SL">SL</option>
<option value="ST">ST</option>
<option value="\u0160I">\u0160I</option>
<option value="VK">VK</option>
<option value="VT">VT</option>
<option value="VU">VU</option>
<option value="V\u017d">V\u017d</option>
<option value="ZD">ZD</option>
<option value="ZG">ZG</option>
<option value="\u017dU">\u017dU</option>
</select>'''
        self.assertHTMLEqual(f.render('license', 'BJ'), out)

    def test_HRPhoneNumberField(self):
        error_invalid = ['Enter a valid phone number']
        error_area = ['Enter a valid area or mobile network code']
        error_number = ['The phone nubmer is too long']
        valid = {
            '+38511234567': '+38511234567',
            '0038511234567': '+38511234567',
            '011234567': '+38511234567',
            '+38521123456': '+38521123456',
            '0038521123456': '+38521123456',
            '021123456': '+38521123456',
        }
        invalid = {
            '123456789': error_invalid,
            '0811234567': error_area,
            '0111234567': error_number,
        }
        self.assertFieldOutput(HRPhoneNumberField, valid, invalid)

    def test_HRLicensePlateField(self):
        error_invalid = ['Enter a valid vehicle license plate number']
        error_area = ['Enter a valid location code']
        error_number = ['Number part cannot be zero']
        valid = {
            'ZG 1234-AA': 'ZG 1234-AA',
            'ZG 123-A': 'ZG 123-A',
        }
        invalid = {
            'PV12345': error_invalid,
            'PV1234AA': error_area,
            'ZG0000CC': error_number,
        }
        self.assertFieldOutput(HRLicensePlateField, valid, invalid)

    def test_HRPostalCodeField(self):
        error_invalid = ['Enter a valid 5 digit postal code']
        valid = {
            '10000': '10000',
            '35410': '35410',
        }
        invalid = {
            'ABCD': error_invalid,
            '99999': error_invalid,
        }
        self.assertFieldOutput(HRPostalCodeField, valid, invalid)

    def test_HROIBField(self):
        error_invalid = ['Enter a valid 11 digit OIB']
        valid = {
            '12345678901': '12345678901',
        }
        invalid = {
            '1234567890': ['Ensure this value has at least 11 characters (it has 10).'] + error_invalid,
            'ABCDEFGHIJK': error_invalid,
        }
        self.assertFieldOutput(HROIBField, valid, invalid)

    def test_HRJMBGField(self):
        error_invalid = ['Enter a valid 13 digit JMBG']
        error_date = ['Error in date segment']
        valid = {
            '1211984302155': '1211984302155',
            '2701984307107': '2701984307107',
        }
        invalid = {
            '1211984302156': error_invalid,
            'ABCDEFG': error_invalid,
            '9999999123456': error_date,
        }
        self.assertFieldOutput(HRJMBGField, valid, invalid)

    def test_HRJMBAGField(self):
        error_invalid = ['Enter a valid 19 digit JMBAG starting with 601983']
        error_copy = ['Card issue number cannot be zero']
        valid = {
            '601983 11 0130185856 4': '6019831101301858564',
        }
        invalid = {
            '601983 11 0130185856 5': error_invalid,
            '601983 01 0130185856 4': error_copy,
        }
        self.assertFieldOutput(HRJMBAGField, valid, invalid)
