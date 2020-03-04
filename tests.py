# -*- coding: utf-8 -*-

import unittest

from utils.containers import RecordDict


class TestRecordDictMethods(unittest.TestCase):
    text_dict = {
        'name': 'Report Summaries Departement',
        'lang': {
            'label': 'en',
            'name': 'English'
        },
        "place": {
            "id": "85632997",
            "placetype": "country",
            "name": "Belgium",
            "belongsto": ["Europe"],
            "location": {
                "lon": 4.66092,
                "lat": 50.640991
            }
        }
    }
    test_list_of_dicts = [
        {'label': 'GPE', 'text': 'Philippines'},
        {'label': 'GPE', 'text': 'Nigeria'},
        {'label': 'GPE', 'text': 'Turkey'},
        {'label': 'ORG', 'text': 'FSC'},
        {'label': 'ORG', 'text': 'EAGF'}
    ]
    test_list_if_nested_dicts = [
        {'element': 'akash', 'consort': {'id': 'Bhumi', 'sense': 'sound'}},
        {'element': 'vayu', 'consort': {'id': 'Lehari', 'sense': 'touch'}},
        {'element': 'agni', 'consort': {'id': 'Swaha', 'sense': 'sight'}},
        {'element': 'varuna', 'consort': {'id': 'Varuni', 'sense': 'taste'}},
        {'element': 'bhumi', 'consort': {'id': 'Dyaus', 'sense': 'smell'}},
    ]

    def test_init(self):
        obj = RecordDict(**self.text_dict)
        self.assertEqual(obj.lang.name, self.text_dict['lang']['name'])
        self.assertTrue(isinstance(obj.place, RecordDict))
        
    def test_flatten(self):
        flat = {
            'name': 'Report Summaries Departement',
            'lang_label': 'en',
            'lang_name': 'English',
            'place_id': '85632997',
            'place_placetype': 'country',
            'place_name': 'Belgium',
            'place_belongsto': ['Europe'],
            'place_location_lon': 4.66092,
            'place_location_lat': 50.640991
        }
        obj = RecordDict(**self.text_dict)
        obj.flatten()
        self.assertEqual(obj, flat)
        self.assertTrue(isinstance(obj, RecordDict))
        self.assertEqual(obj.place_location_lat, 50.640991)

        obj = RecordDict(**self.text_dict)
        obj.flatten(separator='.')
        self.assertEqual(obj['place.name'], 'Belgium')
        self.assertEqual(obj['place.location.lat'], 50.640991)
        with self.assertRaises(KeyError):
            obj['lang']

        with self.assertRaises(AttributeError):
            obj.lang

        with self.assertRaises(KeyError):
            obj['place.location']

        with self.assertRaises(KeyError):
            obj['place_location_lon']

    def test_lookup(self):
        obj = RecordDict(**self.text_dict)
        self.assertEqual(obj.lookup('name'), 'Report Summaries Departement')
        self.assertEqual(obj.lookup('place.location.lat'), 50.640991)
        self.assertEqual(obj.lookup('lang/name', delimiter='/'), 'English')
        paths = ['place.location.xyz', 'gorgonzola', 'place.belongsto', 'wu']
        self.assertEqual(obj.lookup(*paths), ["Europe"])

    def test_from_list(self):
        obj = RecordDict.from_list(self.test_list_if_nested_dicts,
                                   key='element',
                                   val='consort')
        converted = {
            'akash': {'id': 'Bhumi', 'sense': 'sound'},
            'vayu': {'id': 'Lehari', 'sense': 'touch'},
            'agni': {'id': 'Swaha', 'sense': 'sight'},
            'varuna': {'id': 'Varuni', 'sense': 'taste'},
            'bhumi': {'id': 'Dyaus', 'sense': 'smell'}
        }
        self.assertEqual(obj, converted)
        self.assertEqual(obj.akash, {'id': 'Bhumi', 'sense': 'sound'})
        self.assertEqual(obj.agni.id, 'Swaha')
        self.assertEqual(obj.bhumi.sense, 'smell')

    def test_from_list_aggregate(self):
        converted = {
            'GPE': ['Philippines', 'Nigeria', 'Turkey'],
            'ORG': ['FSC', 'EAGF']
        }
        obj = RecordDict.from_list_aggregate(self.test_list_of_dicts,
                                             key='label',
                                             val='text')
        self.assertEqual(obj, converted)
        self.assertTrue(isinstance(obj.ORG, list))
        self.assertEqual(len(obj.GPE), 3)
        with self.assertRaises(AttributeError):
            obj.gpe

        with self.assertRaises(KeyError):
            obj['gpe']


if __name__ == '__main__':
    unittest.main()
