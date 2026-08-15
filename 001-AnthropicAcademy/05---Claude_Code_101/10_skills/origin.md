# Skills

Video

[What are skills?](https://www.youtube.com/watch?v=bjdBVZa66oU)

Transcription:
> Every  time you explain your team's coding standards to Claude, you're repeating yourself.
> Every PR review, you re-describe how you want feedback structured.
> Every commit message, you remind Claude of your preferred format.
>
> And skills fix this.
> A skill is a markdown file that teaches Claude how to do something once, and Claude applies that knowledge automatically whenever it's relevant.
>
> Agent skills are folders of instructions, scripts, and resources that agents can discover and use to do things more accurately and efficiently.
> With Claude Code, we have the `skill.md` file.
> The description is how Claude decides whether to use the skill.
> When you ask Claude to review this PR, it matches your request against available skill descriptions and finds this one.
> Claude reads your request, compares it to all available skill descriptions, and activates the ones that match.
>
> You can store skills in a few places depending on who needs them.
> Personal skills go in the home directory `.claude/skills` and follow you across all your project.
> These are your preferences, you commit message style, your documentation format, how you like code explained.
> Project skills go in the `.claude/skills` inside of the root directory of your repository.
> Anyone who clones the repository gets these skills automotically.
> This is where team standards live, like your company's brand guidelines, preffered fonts and colors that you use for web design.
>
> Claude Code has several ways to customize behavior.
> Skills are unique because they're automatic and task-specific.
> `CLAUDE.md` files load into every conversation.
> if you want Claude to always use TypeScript strict mode, that goes in your `CLAUDE.md` file.
> Skills, on the other hand, load on demand when they match your request.
> It only loads in the name and description, so it doesnt't fill up your entire context window.
> Your PR review checklist doen't need to be in the context when you're debugging.
> It loads when you actually ask for a review.
> Slash commands require you to type them.
> Skills don't. Claude applies them when it recognizes the situation.
>
> Skills work best for specialized knowledge that applies to specific tasks.
> Code review standards your team follows, comit message formats that you prefer, brand guidelines of your organization.
>
> if you find yourself explaining the same thing to Claude repeatedly, well, that's a skill waiting to be written.


## Article
Want to go deeper? Check out our dedicated course: [Introduction to agent skills](https://anthropic.skilljar.com/introduction-to-agent-skills)