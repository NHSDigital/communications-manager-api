import pytest
import io
from pprint import pprint

"""
https://docs.pytest.org/en/latest/how-to/writing_plugins.html#assertion-rewriting

By default helper functions won't be subject to the assertion rewriting that pytest
uses to inform us what didn't hold true in an assertion statement

This line is important in letting pytest know where to find more functions to apply
assertion rewriting to that it hasn't discovered automatically through its test
discovery mechanism

Add similar lines if you intend to add more helper functions to more directories
"""
pytest.register_assert_rewrite('lib')


def pytest_assertrepr_compare(op, left, right):
    """
    This function overrides pytests function for representing failed assertion statements
    https://docs.pytest.org/en/6.2.x/assert.html#defining-your-own-explanation-for-failed-assertions
    """

    if op == '==' and type(left) is dict and type(right) is dict:
        # special case for comparing dictionary equivalence
        keys_in_left = set(left.keys())
        keys_in_right = set(right.keys())
        output = ['dictionary mismatch']

        # show values that we had but shouldn't
        for key in keys_in_left - keys_in_right:
            output.append(f'+   "{key}" : "{left[key]}"')

        # show values that are different
        for key in keys_in_left.intersection(keys_in_right):
            if left[key] != right[key]:
                output.append(f'~   "{key}" : "{left[key]}" should be "{right[key]}"')

        # show values that we should have but didn't
        for key in keys_in_right - keys_in_left:
            output.append(f'-   "{key}" : "{right[key]}"')

        return output

    else:
        left_strio = io.StringIO()
        right_strio = io.StringIO()
        pprint(left, indent=4, compact=True, stream=left_strio)
        pprint(right, indent=4, compact=True, stream=right_strio)

        return ['',
                *left_strio.getvalue().split('\n'),
                f'  {op}',
                *right_strio.getvalue().split('\n')]


@pytest.fixture(scope='session')
def marker_value(request):
    """
    Fixture to retrieve the marker value passed through the command line.
    """
    marker = request.config.getoption('-m')  # Get the marker value
    return marker
