import pytest
import io
from pprint import pprint

pytest.register_assert_rewrite('lib')


def pytest_assertrepr_compare(op, left, right):
    left_strio = io.StringIO()
    right_strio = io.StringIO()
    pprint(left, indent=4, compact=True, stream=left_strio)
    pprint(right, indent=4, compact=True, stream=right_strio)

    return ['',
            *left_strio.getvalue().split('\n'),
            f'  {op}',
            *right_strio.getvalue().split('\n')]
