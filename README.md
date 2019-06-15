

Some dates are very regular in their occurrences.
Like the western Christmas,
which is the 25th of December every year.
Others are more complicated,
like Easter, or bank holidays,
but their definitions are well supported,
so it's not difficult to add them to your code.

But there are plenty of national events that occur
every year which are not predictable like that.
Their dates are decided by committees.
This repository collects a bunch of them,
so you can programmatically refer to them.

Primarily this handles watercooler moments.
The stuff happening around the country which probably
doesn't directly impact your life,
but you'd like to know about them because everybody else
will be talking about them.

## File Format

The data files are in the DOS "INI" format.
As there are ambiguities over edge cases the official arbiter
of the format will be the `configparser` module from Python.

All files must have a `[general]` section which must contain
a human readable `title` key.

    [general]
    title = Welly Wanging World Cup Final

For each year there is a section.
The section must contain either a `date` key formatted
as an ISO 8601 date for a single-day event,
or a `start` key and `end` key (also ISO 8601) to define
the inclusive range of a multi-day event.
An optional `title` key will override the general one.

    [1997]
    date = 1997-07-04

A year without a corresponding section is assumed to
represent a lack of data.
If the event never happened that year then a section
for the year must still be created,
and the `date` key must be set to `None`.

## Licence

The data in the files is licensed under
Creative Commons Attribution & Share-Alike.
This matches Wikipedia,
which happens to be a source for much of it.

The code in the scripts is licensed under
the GNU General Public Licence version 3.

