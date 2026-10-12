# Platform locale binding authoring review

Source e19c766eb3eaedc1b3cd3657bb92864f81a9498a, tree dc1ba97dacc573ead73729297eb739ecb244dcf5, parent b0697fd58a2a37fb94e351f4c4ec68757b0f6b5e.

Exactly three paths change: the app manifest binds existing app_locales; the existing API33+ installed language-switch method verifies the framework resource-derived LocaleConfig status and exact current picker tags; HANDOFF corrects 81 to 108 fallback locales. All remaining 1091 leaves/modes are unchanged. Test identities/budgets and wording/fonts/rendering policy are unchanged.

Writer 27 and independent 24 relevant checks passed normally and under optimized Python. No duplicate local full aggregate or Android execution is claimed. Fresh hosted compilation, compiled manifest binding and installed framework proof are pending at run 38299305241. The new check does not establish actual system Settings UI visibility.

The original missing compiled attribute and exact official AGP 8.13 / manifest-merger 31.13 rule remain preserved at a1c90ca3ec643ee5220ff982e846b5d0e63fe7e1, verification/pr55-current-develop-ci-2026-10-12. Existing prior runtime tests passed but did not exercise that missing binding. Historical outcomes remain bound to their exact inputs. HANDOFF is included in corresponding source, so the new bundled source requires fresh delivery binding too.
