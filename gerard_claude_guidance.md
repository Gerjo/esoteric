# Global Claude Instructions


## Rules to follow
1. Always use explicit types. Do not rely on type inference — declare types explicitly so the code is readable without IDE assistance.
2. Speech-to-text awareness: User may submit messages via speech-to-text. If a word or phrase looks garbled or out of place, ask for clarification rather than guessing the intent.
3. Never commit without explicit permission. A "commit" instruction applies only to that one commit — do not carry it forward to later changes. Always ask before committing unless told to in the current request.
4. Questions are not implementation requests. When the user asks a question about a proposal, plan, or previous suggestion — including questions that raise concerns or give feedback — answer in text only; do NOT edit code. Discussing a proposal is not approval to implement it. Only start editing when the user explicitly asks for the change to be made (e.g. "do it", "implement that", "go ahead").
5. Simulator preference: when running/testing an app via Xcode or the iOS simulator, prefer the iPhone 17 simulator.
6. Never force push git, nor squash commits.
7. When fixing bugs, don't refer to the old bug in code or comments unless expressly useful. Git history should be the general diary — put the reasoning in the commit message, not the code.
