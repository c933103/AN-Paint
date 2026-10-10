# PR30 search accessibility review correction

Finding: [P2 inline review](https://github.com/c933103/AN-Paint/pull/30#discussion_r4229810347)
against `fdab3d80e1f831ceaeee09581c34bd28389dc9fc`. The inline review explicitly
identifies itself as Security review; the aggregate bot summary labels its row
Code Review. Preserve both facts rather than treating the labels as interchangeable.

The new EditText had a constant localized `contentDescription`. That can mask the
live editable query for assistive technology. Remove that property. Horizontal
locales retain the field hint; vertical locales retain the visible column caption
and its `labelFor` relationship. The native edit buffer and search action are
unchanged. This follows the Android [Views editable-element and labelFor guidance](https://developer.android.com/guide/topics/ui/accessibility/views/principles-views#editable_elements).

Regression additions require a null field content description and check actual
accessibility-node text against the current query after successive edits, as well
as existing native editability, hint/label association, Search action and layout
assertions. The all-catalogue matrix also checks live node text for the entered
long query. These Android assertions are prepared for fresh CI, not locally run.

All 326 combined local Python tests pass in 53.586 seconds; the raw log is
`logs/host-python-search-accessibility.log`. No resource, translation key, font or
additional Android execution count is introduced by this correction.

PR #29 has merged at `8a75b825131f0b24c55a40a3636e9e70792037a8`, with the same
`293708639d4bc3382c4f3de8cf35cc0164257b91` base tree as the original stacked PR.
PR30 was retargeted to develop and its pre-correction 13-file diff was verified
identical by path, blob SHA and status. The two original finding commits remain
in history; this review correction is a separate follow-up commit. Fresh CI and
review are required, and final merge authority remains with the parent.
