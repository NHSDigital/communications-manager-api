import json


def scan_and_remove(obj, mappings):
    t = type(obj)

    if t is dict:
        new_obj = {}
        for k, v in obj.items():
            found = False
            for m in mappings:
                if k == m[0] and (m[1] is None or v == m[1]):
                    found = True
            if not found:
                new_obj[k] = scan_and_remove(v, mappings)
        return new_obj
    elif t is list:
        new_list = []
        for i in obj:
            new_list.append(scan_and_remove(i, mappings))
        return new_list

    return obj


specification = None

with open('build/communications-manager.json') as f:
    specification = json.load(f)

with open('build/communications-manager-zap.json', 'w') as f:
    json.dump(
        scan_and_remove(
            specification,
            (
                ("format", "date"),
                ("personalisation", None)
            )
        ),
        f
    )
