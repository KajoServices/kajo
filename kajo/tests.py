# -*- coding: utf-8 -*-

import unittest

from utils.containers import *
from decorators import *


TEXT_DICT = {
    "name": "Report Summaries Departement",
    "lang": {
        "label": "en",
        "name": "English"
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


class TestUtilsRecordDictMethods(unittest.TestCase):
    text_dict = TEXT_DICT.copy()
    test_list_of_dicts = [
        {"label": "GPE", "text": "Philippines"},
        {"label": "GPE", "text": "Nigeria"},
        {"label": "GPE", "text": "Turkey"},
        {"label": "ORG", "text": "FSC"},
        {"label": "ORG", "text": "EAGF"}
    ]
    test_list_if_nested_dicts = [
        {"element": "akash", "consort": {"id": "Bhumi", "sense": "sound"}},
        {"element": "vayu", "consort": {"id": "Lehari", "sense": "touch"}},
        {"element": "agni", "consort": {"id": "Swaha", "sense": "sight"}},
        {"element": "varuna", "consort": {"id": "Varuni", "sense": "taste"}},
        {"element": "bhumi", "consort": {"id": "Dyaus", "sense": "smell"}},
    ]

    def test_init(self):
        obj = RecordDict(**self.text_dict)
        self.assertEqual(obj.lang.name, self.text_dict["lang"]["name"])
        self.assertTrue(isinstance(obj.place, RecordDict))

    def test_flatten(self):
        flat = {
            "name": "Report Summaries Departement",
            "lang_label": "en",
            "lang_name": "English",
            "place_id": "85632997",
            "place_placetype": "country",
            "place_name": "Belgium",
            "place_belongsto": ["Europe"],
            "place_location_lon": 4.66092,
            "place_location_lat": 50.640991
        }
        obj = RecordDict(**self.text_dict)
        obj.flatten()
        self.assertEqual(obj, flat)
        self.assertTrue(isinstance(obj, RecordDict))
        self.assertEqual(obj.place_location_lat, 50.640991)

        obj = RecordDict(**self.text_dict)
        obj.flatten(separator=".")
        self.assertEqual(obj["place.name"], "Belgium")
        self.assertEqual(obj["place.location.lat"], 50.640991)
        with self.assertRaises(KeyError):
            obj["lang"]

        with self.assertRaises(AttributeError):
            obj.lang

        with self.assertRaises(KeyError):
            obj["place.location"]

        with self.assertRaises(KeyError):
            obj["place_location_lon"]

    def test_update(self):
        test_dict = {
            "name": "Ministry of Silly Walks",
            "curvature": "flat",
            "place": {"location": {"lon": 12.5, "lat": 50.640991}}
        }
        obj = RecordDict(**self.text_dict)
        obj.update(test_dict)
        self.assertTrue("curvature" in obj)
        self.assertTrue(obj.curvature, "flat")
        self.assertEqual(obj["name"], "Ministry of Silly Walks")
        self.assertEqual(obj.place.location.lon, 12.5)

    def test_lookup(self):
        obj = RecordDict(**self.text_dict)
        self.assertEqual(obj.lookup("name"), "Report Summaries Departement")
        self.assertEqual(obj.lookup("place.location.lat"), 50.640991)
        self.assertEqual(obj.lookup("lang/name", delimiter="/"), "English")
        paths = ["place.location.xyz", "gorgonzola", "place.belongsto", "wu"]
        self.assertEqual(obj.lookup(*paths), ["Europe"])

    def test_from_list(self):
        obj = RecordDict.from_list(self.test_list_if_nested_dicts,
                                   key="element",
                                   val="consort")
        converted = {
            "akash": {"id": "Bhumi", "sense": "sound"},
            "vayu": {"id": "Lehari", "sense": "touch"},
            "agni": {"id": "Swaha", "sense": "sight"},
            "varuna": {"id": "Varuni", "sense": "taste"},
            "bhumi": {"id": "Dyaus", "sense": "smell"}
        }
        self.assertEqual(obj, converted)
        self.assertEqual(obj.akash, {"id": "Bhumi", "sense": "sound"})
        self.assertEqual(obj.agni.id, "Swaha")
        self.assertEqual(obj.bhumi.sense, "smell")

    def test_from_list_aggregate(self):
        converted = {
            "GPE": ["Philippines", "Nigeria", "Turkey"],
            "ORG": ["FSC", "EAGF"]
        }
        obj = RecordDict.from_list_aggregate(self.test_list_of_dicts,
                                             key="label",
                                             val="text")
        self.assertEqual(obj, converted)
        self.assertTrue(isinstance(obj.ORG, list))
        self.assertEqual(len(obj.GPE), 3)
        with self.assertRaises(AttributeError):
            obj.gpe

        with self.assertRaises(KeyError):
            obj["gpe"]


class TestUtilsFunctions(unittest.TestCase):
    text_dict = TEXT_DICT.copy()

    def test_deep_update(self):
        test_dict = {
            "name": "Ministry of Silly Walks",
            "place": {"location": {"lon": 12.5, "lat": 50.640991}}
        }
        deep_update(test_dict, self.text_dict)
        self.assertTrue("lang" in test_dict)
        self.assertEqual(test_dict["name"], self.text_dict["name"])
        self.assertEqual(test_dict["place"]["location"]["lon"], 4.66092)

    def test_flatten_list(self):
        self.assertEqual(flatten_list([['Sonic'], ['Youth']]), ['Sonic', 'Youth'])
        self.assertEqual(flatten_list([['Sonic', 'Youth'], ['Judas', 'Priest']]),
                                      ['Sonic', 'Youth', 'Judas', 'Priest'])
        self.assertEqual(flatten_list([('Napalm', 'Death'), ['Scorn']]),
                                      ['Napalm', 'Death', 'Scorn'])
        self.assertEqual(flatten_list([1, [3, 4], 'Darkthrone']), [1, 3, 4, 'Darkthrone'])
        self.assertEqual(flatten_list([1, [[2, 3], [4, 5]], 6]), [1, 2, 3, 4, 5, 6])

    def test_normalize_keys(self):
        input_ = {
            "Server": "Apache-Coyote/1.1",
            "Content-Type": "text/html;charset=utf-8",
            "Last-Modified": {
                "Day-Of-Week": "Sat",
                "Day": 4,
                "Month": "Apr",
                "Year": 2020,
                "Hour": "12",
                "Min": 1,
                "Sec": 29,
                "Time-Zone": "GMT"
            }
        }
        output_default = normalize_keys(input_)
        output_retain_case = normalize_keys(input_, lowercase=False)
        output_customized = normalize_keys(input_, lowercase=False, separator='')
        output_intact = normalize_keys(input_, lowercase=False, separator='-')

        self.assertTrue("content_type" in output_default)
        self.assertTrue("day_of_week" in output_default["last_modified"])
        self.assertTrue("Day_Of_Week" in output_retain_case["Last_Modified"])
        self.assertTrue("TimeZone" in output_customized["LastModified"])
        self.assertEqual(output_customized["LastModified"]["TimeZone"],
                         input_["Last-Modified"]["Time-Zone"])
        self.assertTrue("TimeZone" in output_customized["LastModified"])
        self.assertTrue(input_ == output_intact)

    def test_compress_and_sort_by_occurence(self):
        names = ['Siddhartha', 'Varuna', 'Daruma', 'Siddhartha', 'Daruma', 'Kevala', 'Siddhartha']

        res = compress_and_sort_by_occurence(names)
        self.assertEqual(res[:2], ['Siddhartha', 'Daruma'])
        self.assertTrue(all(x in res[2:4] for x in ['Varuna', 'Kevala']))

        res = compress_and_sort_by_occurence(names, reverse=False)
        self.assertTrue(all(x in res[:2] for x in ['Varuna', 'Kevala']))
        self.assertEqual(res[2:4], ['Daruma', 'Siddhartha'])

        res = compress_and_sort_by_occurence(names, values_only=False)
        self.assertEqual(res[:2], [{'elm': 'Siddhartha', 'num': 3},
                                   {'elm': 'Daruma', 'num': 2}])
        self.assertTrue(all(x['num'] == 1 for x in res[2:4]))

        res = compress_and_sort_by_occurence(names, reverse=False, values_only=False)
        self.assertEqual(res[2:4], [{'elm': 'Daruma', 'num': 2},
                                    {'elm': 'Siddhartha', 'num': 3}])
        self.assertTrue(all(x['num'] == 1 for x in res[:2]))


class TestDecorators(unittest.TestCase):
    def test_objectify(self):

        @objectify
        def test_dict():
            return {"name": "Bromba", "loc": {"X": 12, "Y": 15, "elev": .1}}

        result = test_dict()
        self.assertEqual(getattr(result, "name"), "Bromba")
        self.assertEqual(result.loc.Y, 15)
        self.assertEqual(result.loc.elev, .1)


if __name__ == "__main__":
    unittest.main()
