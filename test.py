import pytest

from utils import score_band


@pytest.mark.parametrize(
    "scores,expected",
    (
        ([], None),
        ([10], "Low"),
        ([30], "Low"),
        ([31], "Medium"),
        ([70], "Medium"),
        ([71], "High"),
        ([10, 0, 20], "Low"),
        ([30, 0, 10], "Low"),
        ([10, 20, 70], "Medium"),
        ([0, 35, 71], "High"),
    ),
)
def test_score_band_bands_correctly(scores, expected):
    assert score_band(scores) == expected
