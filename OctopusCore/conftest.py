import json
import random
import string
import time

import pytest

import api


def pytest_addoption(parser):
    parser.addoption('--quick', '-Q', dest="quick", action='store_true', help='disables autogenerated tests')


@pytest.fixture
def app():
    api.app.debug = True
    return api.app


# noinspection PyUnusedLocal,SpellCheckingInspection
@pytest.fixture
def auth_headers(client):
    # Dynamically get the token (slow [has to confirm pw with db on every test]):

    # response = client.post(url_for('login'), data = '{"email":"d","password":"c"}', content_type='application/json')
    # assert 200 == response.status_code
    # return {'Authorization': 'Bearer ' + response.get_data(), 'Content-Type': 'application/json'}

    # Use static, everlasting token (dangerous[ish] {Since it is a fake user with no rights, real data}):

    # noinspection SpellCheckingInspection
    return {'Authorization': 'Bearer ' +
                             "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9." +
                             "eyJ1aWQiOiI1YTQyYzYzZDQ4MzA2MDIyNzhkMGE3Y2EifQ." +
                             "3dDnXsRoDLTOh7VJkXT3LBJ46ZMm07zx-1CBF-DlkiQ",
            'Content-Type': 'application/json'}


import subprocess


@pytest.fixture
def server():
    server = subprocess.Popen(['python', '-m', 'api'])
    time.sleep(1)
    yield server
    server.terminate()

def get_int():
    return random.randint(-3665, 3665)


def get_float():
    return random.uniform(-3665, 3665)


def get_string():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(1, 8)))


def get_everything_but_not_empty_string_list():
    return [get_int(), get_float(), "", 0, 0.0, {}, []]


def get_everything_but_int_list():
    return [get_string(), get_float(), "", 0.0, {}, []]


def get_everything_but_float_list():
    return [get_int(), get_string(), "", 0, {}, []]


def get_everything_but_list_list():
    return [get_int(), get_float(), get_string(), "", 0, 0.0, {}]


def get_everything_but_dict_list():
    return [get_int(), get_float(), get_string(), "", 0, 0.0, []]


def gen_test_dict_list(input_dict):
    # A bit more sane code follows, do keep enabled
    # Generates a list of test dicts with invalid input subbed for one of the values
    # and all the other values left valid.
    # Gens ~100+ tests

    test_list = []
    for key, value in input_dict.items():
        for testValue in value[0]:
            test_dict = {}
            orig_dict = input_dict.copy()
            del orig_dict[key]
            for untestedKey, untestedValue in orig_dict.items():
                test_dict[untestedKey] = untestedValue[1]
            test_dict[key] = testValue
            test_list.append(test_dict)
    return test_list

    # Insane code follows, DO NOT ENABLE
    # Runs through ALL possible invalid dict combinations
    # This is mostly pointless IRL, but gives much better certainty in invalid input rejection
    # THIS WILL GENERATE 90,000+ TESTS
    # adding more invalid input variations on large dicts WILL crash pytest
    #
    # import itertools as it
    #
    # variants= {}
    #
    # for key, value in inputDict.items():
    #     variants[key] = value[0]
    #
    # # The following code is magic, please do not touch
    # varNames = sorted(variants)
    # combinations = [dict(zip(varNames, prod)) for prod in it.product(*(variants[varName] for varName in varNames))]
    # return combinations


print gen_test_dict_list({"__Infrary__ID": [get_everything_but_int_list(), 52352353],
                          "__Infrary__Provider": [get_everything_but_not_empty_string_list(), "DO"]})


def autogen_tests(tup):
    tup_list = []
    for element in gen_test_dict_list(tup[0]):
        tup_list.append((json.dumps(element),) + tup[1:])
    return tup_list


def autogen_tests_raw(tup):
    tup_list = []
    for element in gen_test_dict_list(tup[0]):
        tup_list.append((element,) + tup[1:])
    return tup_list
