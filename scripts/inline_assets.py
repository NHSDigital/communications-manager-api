#!/usr/bin/env python3
"""
inline_assets.py

Reads an openapi spec on stdin, replaces asset tokens with base64 `data:`
URIs so documentation download links are self-contained (no external
hosting), then prints the spec on stdout.
"""
import sys
import os
import json
import base64

# Maps a token found in the spec (typically within info.description) to the
# repo-relative asset whose base64-encoded contents replace it at build time.
ASSET_TOKENS = {
    "{{NONPROD_CA_B64}}": "specification/documentation/certs/nonprod-ca.crt",
    "{{PROD_CA_B64}}": "specification/documentation/certs/prod-ca.crt",
}


def _repo_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def embed_inline_assets(spec):
    """Replace asset tokens anywhere in the spec with base64 of the asset.

    A token is only resolved if it is present in the serialised spec. If a
    referenced asset file is missing, the build fails loudly.
    """
    serialised = json.dumps(spec)
    for token, rel_path in ASSET_TOKENS.items():
        if token not in serialised:
            continue
        path = os.path.join(_repo_root(), rel_path)
        with open(path, "rb") as asset:
            encoded = base64.b64encode(asset.read()).decode("ascii")
        serialised = serialised.replace(token, encoded)
    return json.loads(serialised)


def main():
    """Main entrypoint"""
    data = json.loads(sys.stdin.read())
    data = embed_inline_assets(data)
    sys.stdout.write(json.dumps(data, indent=2))
    sys.stdout.close()


if __name__ == "__main__":
    main()
