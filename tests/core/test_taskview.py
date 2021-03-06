# -----------------------------------------------------------------------------
# Getting Things GNOME! - a personal organizer for the GNOME desktop
# Copyright (c) - The GTG Team
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------

import re
from unittest import TestCase
from GTG.gtk.editor.taskview import TaskView, TAG_REGEX


class TestTaskView(TestCase):
    def test_detect_tags(self):
        """Check that tags are being detected correctly."""

        content = 'mmmm @aaaa @aaa-bbbb @ @ccc @これはタグ @1234'
        matches = re.finditer(TAG_REGEX, content)

        target_tags = ['@aaaa', '@aaa-bbbb', '@ccc', '@これはタグ', '@1234']

        for index, match in enumerate(matches):
            self.assertEqual(match.group(0), target_tags[index])


    def test_no_detect_tags(self):
        """Check that things that aren't tags aren't being detected."""

        content = 'mmmm an@email.com xxxx@ @--- no@tag'
        matches = re.findall(TAG_REGEX, content)

        self.assertEqual([], matches)


    def test_convert_subtask(self):
        """Check subtask conversion."""

        source = '→   <subtask>b3f65b40-cf32-44d8-8d94-e4a1ed7199c3</subtask>'
        target = '   {! b3f65b40-cf32-44d8-8d94-e4a1ed7199c3 !}'

        self.assertEqual(target, TaskView.format_update(source))


    def test_convert_tags(self):
        """Make sure tags are being deleted."""

        source = '<tag>@one_tag</tag>, <tag>@another_tag</tag>,'
        target = '@one_tag, @another_tag,'

        self.assertEqual(target, TaskView.format_update(source))


    def test_convert_full_task(self):

        source = '''
<tag>@tag</tag>, <tag>@something-else</tag>
Some text here and there
To spice things up

→   <subtask>3454c8fe-21b7-41e1-abec-8060223a1a63</subtask>
→   <subtask>92766ac9-1711-4163-ab7c-8a0f1fdfe3c0</subtask>
→   <subtask>f0c11f1e-76cb-47c3-b840-9378157cf022</subtask>
→   <subtask>3a805a54-f9f0-43b2-8d38-7f66b59fc8e5</subtask>
→   <subtask>28528f83-0e7f-4774-b887-499bfa3ef2a7</subtask>'''

        target = '''
@tag, @something-else
Some text here and there
To spice things up

   {! 3454c8fe-21b7-41e1-abec-8060223a1a63 !}
   {! 92766ac9-1711-4163-ab7c-8a0f1fdfe3c0 !}
   {! f0c11f1e-76cb-47c3-b840-9378157cf022 !}
   {! 3a805a54-f9f0-43b2-8d38-7f66b59fc8e5 !}
   {! 28528f83-0e7f-4774-b887-499bfa3ef2a7 !}'''

        self.assertEqual(target, TaskView.format_update(source))
