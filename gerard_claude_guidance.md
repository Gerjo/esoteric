# Global Claude Instructions

## Slang / Shorthand

- "mate a file" means open it with the `mate` CLI (TextMate editor). Run `mate <path>` — do not read/display the file contents.
- "gitx a file" means open it with the `gitx` CLI. Run `gitx <path>` — to open a git repository at the given path.
- "qfind a file" means to find the file using the filename or filename pattern. If it's a unity project, please skip the library folder.


## Rules to follow
1. At the start of each conversation, acknowledge that you have read CLAUDE.md and will adhere to it.
2. A proposal is not exempt from any rules - all rules still apply when creating and presenting proposals.
3. Ask before acting: outline what you plan to do and wait for approval before making changes, unless I explicitly said "just do it". You also don't have to check if you're just reading back what I just asked.
4. Check after builds: If a build fails, unless it's a trivial mistake, check with me before proceeding rather than trying to fix it myself. This should catch any misunderstanding.
5. Always use explicit types. Do not rely on type inference — declare types explicitly so the code is readable without IDE assistance.
6. Don't proactively explain decisions or narrate actions. If a question has a yes/no answer, lead with yes or no. Only elaborate if the user asks.
7. Context awareness: When you notice a conversation has been automatically compacted/summarized (indicated by receiving a summary instead of full message history), proactively inform me at the start of your next response with: "Note: This conversation was automatically summarized due to length. I have a compressed summary of our earlier work, but some details may have been condensed. If you need specifics from before the summary, I can read the full transcript."
8. Never run `git commit` without explicit permission. Asking "can I commit?" and receiving "yes" counts as explicit permission for that specific commit.
9. Before any operation judged to be risky or hard to reverse (large refactors, file deletions, dependency changes, navigation restructuring), suggest making a git commit first so there's a clean revert point. If permission is granted at that point, proceed with the commit.
10. "can you" is always a question about whether in theory you could do something. Respond with an action plan (or say no)
11. Speech-to-text awareness: User may submit messages via speech-to-text. If a word or phrase looks garbled or out of place, ask for clarification rather than guessing the intent.
12. When the user requests changes to a proposal, always re-propose before implementing.
