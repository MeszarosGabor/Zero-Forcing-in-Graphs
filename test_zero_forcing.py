"""
Zero Forcing Unit tests against small graphs.
"""


import pytest

import zero_forcing


@pytest.mark.parametrize(
        "neighbor_list,forcing_number",
        [
            pytest.param(
                [{1}, {0}],
                1,
                id="edge",
            ),
            pytest.param(
                [{1, 2}, {0, 2}, {0, 1}],
                2,
                id="triangle",
            ),
            pytest.param(
                [{1}, {0, 2}, {1, 3}, {2, 4}, {3}],
                1,
                id="path on 5 vertices",
            ),
            pytest.param(
                [{1}, {0, 2, 3}, {1, 3}, {1, 2}],
                2,
                id="earring",
            ),
            pytest.param(
                [{1, 4}, {0, 2}, {1, 3}, {2, 4}, {3, 0}],
                2,
                id="cycle",
            ),
            pytest.param(
                [{1, 2, 3}, {0, 2, 3}, {0, 1, 3}, {0, 1, 2}],
                3,
                id="complete graph on 4 vertices",
            ),
        ]
)
def test_zf(neighbor_list, forcing_number):
    zf_calculated = zero_forcing.calculate_zero_forcing_nr(neighbor_list)
    assert zf_calculated == forcing_number
