import tempfile
from collections import namedtuple
from pathlib import Path

import pytest

import betterbib

FieldHolder = namedtuple("FieldHolder", "fields")

# the following are re-used in several tests
FULL_PNAS = (
    "Proceedings of the National Academy of Sciences of the United States of America"
)
PNAS_ABBREV = "PNAS"


this_dir = Path(__file__).resolve().parent
data_file_exists = Path(this_dir / "../src/betterbib/data/journals.json").is_file()


def make_fake_entry(journal, citekey="foo"):
    contents = FieldHolder({"journal": journal})
    return {citekey: contents}


@pytest.mark.skipif(not data_file_exists, reason="Data file missing")
def test_standard_abbrev():
    journals = [FULL_PNAS]
    abbrevs = [PNAS_ABBREV]
    for journal, abbrev in zip(journals, abbrevs):
        entries = make_fake_entry(journal)
        betterbib.journal_abbrev(entries)
        assert entries["foo"].fields["journal"] == abbrev


@pytest.mark.skipif(not data_file_exists, reason="Data file missing")
def test_custom_abbrev():
    infile = tempfile.NamedTemporaryFile().name
    super_short = '{"PNAS": "' + PNAS_ABBREV + '"}'
    with open(infile, "w") as f:
        f.write(super_short)

    entries = make_fake_entry("PNAS")
    betterbib.journal_abbrev(entries, custom_abbrev=infile)
    assert entries["foo"].fields["journal"] == PNAS_ABBREV

    super_short = '{"' + FULL_PNAS + '": "PNAS"}'
    with open(infile, "w") as f:
        f.write(super_short)

    entries = make_fake_entry(FULL_PNAS)
    betterbib.journal_abbrev(entries, custom_abbrev=infile)
    assert entries["foo"].fields["journal"] == "PNAS"


@pytest.mark.skipif(not data_file_exists, reason="Data file missing")
def test_standard_abbrev_long():
    journals = [FULL_PNAS]
    abbrevs = [PNAS_ABBREV]
    for journal, abbrev in zip(journals, abbrevs):
        entries = make_fake_entry(abbrev)
        betterbib.journal_abbrev(entries, long_journal_names=True)
        assert entries["foo"].fields["journal"] == journal


@pytest.mark.skipif(not data_file_exists, reason="Data file missing")
def test_custom_abbrev_long():
    infile = tempfile.NamedTemporaryFile().name
    super_short = '{"' + FULL_PNAS + ': "PNAS"}'
    with open(infile, "w") as f:
        f.write(super_short)

    entries = make_fake_entry(PNAS_ABBREV)
    betterbib.journal_abbrev(entries, long_journal_names=True)
    assert entries["foo"].fields["journal"] == FULL_PNAS
