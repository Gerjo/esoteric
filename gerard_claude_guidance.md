# Global Claude Instructions


## Rules to follow
1. Always use explicit types. Do not rely on type inference — declare types explicitly so the code is readable without IDE assistance.
2. Source code comments are not a change log. Use git commits to document why changes took place.
3. Never commit without explicit permission. A "commit" instruction applies only to that one commit — do not carry it forward to later changes. Always ask before committing unless told to in the current request.
4. Questions are not implementation requests. When the user asks a question about a proposal, plan, or previous suggestion — including questions that raise concerns or give feedback — answer in text only; do NOT edit code. Discussing a proposal is not approval to implement it. Only start editing when the user explicitly asks for the change to be made (e.g. "do it", "implement that", "go ahead").
5. Simulator preference: when running/testing an app via Xcode or the iOS simulator, prefer the iPhone 17 simulator.
6. Never force push git, nor squash commits. Never create new branches without permission.
7. Deploying is not testing. "Deploy", "install", or "build and run" means build it and get it onto the device or simulator and launch it — then stop and report.
8. Never compile, build, or test without explicit permission. Make the code change and stop; only recompile, enter play mode, or run tests when asked in the current request.
9. Never write code without permission. If an error is pasted, propose solutions but do not implement a fix automatically.
10. Prefer numbered lists over plain bullet points, so we can quickly refer to the same item by number. Label every list in a reply uniquely: the first list is A1, A2, ..., the second B1, B2, and so on, so one label never means two things.
11. Prefer short output. Human cognitive load on reading AI text is high and must be avoided.
