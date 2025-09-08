import json


def clean_dict(obj, mappings):
    new_obj = {}
    for k, v in obj.items():
        should_remove = False
        for m in mappings:
            if k == m[0] and (m[1] is None or v == m[1]):
                should_remove = True
        if not should_remove:
            new_obj[k] = scan_and_remove(v, mappings)
    return new_obj


def clean_list(obj, mappings):
    new_list = []
    for i in obj:
        new_list.append(scan_and_remove(i, mappings))
    return new_list


def scan_and_remove(obj, mappings):
    t = type(obj)

    if t is dict:
        return clean_dict(obj, mappings)
    elif t is list:
        return clean_list(obj, mappings)
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
                ("personalisation", None),
                ("/<client-provided-message-status-URI>", None),
                ("/<client-provided-channel-status-URI>", None),
            )
        ),
        f
    )
