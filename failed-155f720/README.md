# PR 158 failed revision evidence

Source: `155f7209008e17edc9b68c4d1a9af3f6b7ad36a1`.
Workflow: https://github.com/c933103/AN-Paint/actions/runs/39550555972
Synthetic merge checkout: `47b39c742f37893167aa10aa38716e4dd8b20f60`.

The four failing JVM suite XML files are copied unchanged from artifact
12323728107. `jvm-summary.json` totals every original JVM XML, with the 17 failed
identities and original messages. API35 phase XML/summaries and collection logs
are copied unchanged from artifact 12324476648. The adbd file is explicitly a
filtered excerpt of the original logcat, not its complete log. It shows
host-17 write failure/offline at 06:00:10.317 and host-18 reconnect at .758.
The underlying disconnect trigger is not established by these logs.
No installed screenshot files were recovered; instrumentation success cannot
substitute for the failed mandatory collection.

Original downloaded ZIP SHA-256:

- JVM: `13195d6b178ce1c7973e3c2116cf2887bf40ede41f49d2681384ac919f2134f5`
- API35 core: `4eec4c5a6ee8d69b018204903485baed0cba6e392f3baaaf516ca910390b273f`

These failed receipts are not acceptance evidence for a later revision.
