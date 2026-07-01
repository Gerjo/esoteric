# Global Claude Instructions


## Rules to follow
1. Always use explicit types. Do not rely on type inference — declare types explicitly so the code is readable without IDE assistance.
2. Speech-to-text awareness: User may submit messages via speech-to-text. If a word or phrase looks garbled or out of place, ask for clarification rather than guessing the intent.
3. Never commit without explicit permission. A "commit" instruction applies only to that one commit — do not carry it forward to later changes. Always ask before committing unless told to in the current request.
