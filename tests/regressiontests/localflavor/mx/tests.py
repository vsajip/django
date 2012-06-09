# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.localflavor.mx.forms import (MXZipCodeField, MXRFCField,
    MXStateSelect, MXCURPField)
from django.test import SimpleTestCase
from django.utils.py3 import text_type

from .forms import MXPersonProfileForm


class MXLocalFlavorTests(SimpleTestCase):

    def setUp(self):
        self.form = MXPersonProfileForm({
            'state': 'MIC',
            'rfc': 'toma880125kv3',
            'curp': 'toma880125hmnrrn02',
            'zip_code': '58120',
        })

    def test_get_display_methods(self):
        """Test that the get_*_display() methods are added to the model instances."""
        place = self.form.save()
        self.assertEqual(place.get_state_display(), 'Michoacán')

    def test_errors(self):
        """Test that required MXFields throw appropriate errors."""
        form = MXPersonProfileForm({
            'state': 'Invalid state',
            'rfc': 'invalid rfc',
            'curp': 'invalid curp',
            'zip_code': 'xxx',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['state'], ['Select a valid choice. Invalid state is not one of the available choices.'])
        self.assertEqual(form.errors['rfc'], ['Enter a valid RFC.'])
        self.assertEqual(form.errors['curp'], ['Ensure this value has at least 18 characters (it has 12).', 'Enter a valid CURP.'])
        self.assertEqual(form.errors['zip_code'], ['Enter a valid zip code in the format XXXXX.'])

    def test_field_blank_option(self):
        """Test that the empty option is there."""
        state_select_html = """\
<select name="state" id="id_state">
<option value="">---------</option>
<option value="AGU">Aguascalientes</option>
<option value="BCN">Baja California</option>
<option value="BCS">Baja California Sur</option>
<option value="CAM">Campeche</option>
<option value="CHH">Chihuahua</option>
<option value="CHP">Chiapas</option>
<option value="COA">Coahuila</option>
<option value="COL">Colima</option>
<option value="DIF">Distrito Federal</option>
<option value="DUR">Durango</option>
<option value="GRO">Guerrero</option>
<option value="GUA">Guanajuato</option>
<option value="HID">Hidalgo</option>
<option value="JAL">Jalisco</option>
<option value="MEX">Estado de México</option>
<option value="MIC" selected="selected">Michoacán</option>
<option value="MOR">Morelos</option>
<option value="NAY">Nayarit</option>
<option value="NLE">Nuevo León</option>
<option value="OAX">Oaxaca</option>
<option value="PUE">Puebla</option>
<option value="QUE">Querétaro</option>
<option value="ROO">Quintana Roo</option>
<option value="SIN">Sinaloa</option>
<option value="SLP">San Luis Potosí</option>
<option value="SON">Sonora</option>
<option value="TAB">Tabasco</option>
<option value="TAM">Tamaulipas</option>
<option value="TLA">Tlaxcala</option>
<option value="VER">Veracruz</option>
<option value="YUC">Yucatán</option>
<option value="ZAC">Zacatecas</option>
</select>"""
        self.assertHTMLEqual(text_type(self.form['state']), state_select_html)

    def test_MXStateSelect(self):
        f = MXStateSelect()
        out = '''<select name="state">
<option value="AGU">Aguascalientes</option>
<option value="BCN">Baja California</option>
<option value="BCS">Baja California Sur</option>
<option value="CAM">Campeche</option>
<option value="CHH">Chihuahua</option>
<option value="CHP">Chiapas</option>
<option value="COA">Coahuila</option>
<option value="COL">Colima</option>
<option value="DIF">Distrito Federal</option>
<option value="DUR">Durango</option>
<option value="GRO">Guerrero</option>
<option value="GUA">Guanajuato</option>
<option value="HID">Hidalgo</option>
<option value="JAL">Jalisco</option>
<option value="MEX">Estado de México</option>
<option value="MIC" selected="selected">Michoacán</option>
<option value="MOR">Morelos</option>
<option value="NAY">Nayarit</option>
<option value="NLE">Nuevo León</option>
<option value="OAX">Oaxaca</option>
<option value="PUE">Puebla</option>
<option value="QUE">Querétaro</option>
<option value="ROO">Quintana Roo</option>
<option value="SIN">Sinaloa</option>
<option value="SLP">San Luis Potosí</option>
<option value="SON">Sonora</option>
<option value="TAB">Tabasco</option>
<option value="TAM">Tamaulipas</option>
<option value="TLA">Tlaxcala</option>
<option value="VER">Veracruz</option>
<option value="YUC">Yucatán</option>
<option value="ZAC">Zacatecas</option>
</select>'''
        self.assertHTMLEqual(f.render('state', 'MIC'), out)

    def test_MXZipCodeField(self):
        error_format = ['Enter a valid zip code in the format XXXXX.']
        valid = {
            '58120': '58120',
            '58502': '58502',
            '59310': '59310',
            '99999': '99999',
        }
        invalid = {
            '17000': error_format,
            '18000': error_format,
            '19000': error_format,
            '00000': error_format,
        }
        self.assertFieldOutput(MXZipCodeField, valid, invalid)

    def test_MXRFCField(self):
        error_format = ['Enter a valid RFC.']
        error_checksum = ['Invalid checksum for RFC.']
        valid = {
            'MoFN641205eX5': 'MOFN641205EX5',
            'ICa060120873': 'ICA060120873',
            'eUcG751104rT0': 'EUCG751104RT0',
            'GME08100195A': 'GME08100195A',
            'AA&060524KX5': 'AA&060524KX5',
            'CAÑ0708045P7': 'CAÑ0708045P7',
            'aaa000101aa9': 'AAA000101AA9',
        }
        invalid = {
            'MED0000000XA': error_format,
            '0000000000XA': error_format,
            'AAA000000AA6': error_format,
            # Dates
            'XXX880002XXX': error_format,
            'XXX880200XXX': error_format,
            'XXX880132XXX': error_format,
            'XXX880230XXX': error_format,
            'XXX880431XXX': error_format,
            # Incorrect checksum
            'MOGR650524E73': error_checksum,
            'HVA7810058F1': error_checksum,
            'MoFN641205eX2': error_checksum,
            'ICa060120871': error_checksum,
            'eUcG751104rT7': error_checksum,
            'GME081001955': error_checksum,
            'AA&060524KX9': error_checksum,
            'CAÑ0708045P2': error_checksum,
        }
        self.assertFieldOutput(MXRFCField, valid, invalid)

    def test_MXCURPField(self):
        error_format = ['Enter a valid CURP.']
        error_checksum = ['Invalid checksum for CURP.']
        valid = {
            'AaMG890608HDFLJL00': 'AAMG890608HDFLJL00',
            'BAAd890419HMNRRV07': 'BAAD890419HMNRRV07',
            'VIAA900930MMNClL08': 'VIAA900930MMNCLL08',
            'HEGR891009HMNRRD09': 'HEGR891009HMNRRD09',
            'MARR890512HMNRMN09': 'MARR890512HMNRMN09',
            'MESJ890928HMNZNS00': 'MESJ890928HMNZNS00',
            'BAAA890317HDFRLL03': 'BAAA890317HDFRLL03',
            'TOMA880125HMNRRNO2': 'TOMA880125HMNRRNO2',
            'OOMG890727HMNRSR06': 'OOMG890727HMNRSR06',
            'AAAA000101HDFCCC09': 'AAAA000101HDFCCC09',
        }
        invalid = {
            'AAAA000000HDFCCC09': error_format,
            'AAAA000000HDFAAA03': error_format,
            'AAAA000000HXXCCC08': error_format,
            'AAAA000000XMNCCC02': error_format,
            'HEGR891009HMNRRD0A': error_format,
            'MARR890512HMNRMN0A': error_format,
            'AaMG890608HDFLJL01': error_checksum,
            'BAAd890419HMNRRV08': error_checksum,
            'VIAA900930MMNClL09': error_checksum,
            'MESJ890928HMNZNS01': error_checksum,
            'BAAA890317HDFRLL04': error_checksum,
            'TOMA880125HMNRRNO3': error_checksum,
            'OOMG890727HMNRSR07': error_checksum,
        }
        self.assertFieldOutput(MXCURPField, valid, invalid)
