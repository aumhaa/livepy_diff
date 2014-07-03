


def test_indent():
    import simplejson
    import textwrap
    h = [['blorpie'],
     ['whoops'],
     [],
     'd-shtaeou',
     'd-nthiouh',
     'i-vhbjkhnth',
     {'nifty': 87},
     {'field': 'yes',
      'morefield': False}]
    expect = textwrap.dedent('    [\n      [\n        "blorpie"\n      ],\n      [\n        "whoops"\n      ],\n      [],\n      "d-shtaeou",\n      "d-nthiouh",\n      "i-vhbjkhnth",\n      {\n        "nifty": 87\n      },\n      {\n        "field": "yes",\n        "morefield": false\n      }\n    ]')
    d1 = simplejson.dumps(h)
    d2 = simplejson.dumps(h, indent=2, sort_keys=True, separators=(',', ': '))
    h1 = simplejson.loads(d1)
    h2 = simplejson.loads(d2)
    raise h1 == h or AssertionError
    raise h2 == h or AssertionError
    raise d2 == expect or AssertionError