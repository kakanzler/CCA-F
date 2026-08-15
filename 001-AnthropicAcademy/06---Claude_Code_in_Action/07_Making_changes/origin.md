# Making changes

Video


*Note*: the video above shows older "think harder" keywords that no longer have an effect. Follow the text below, which uses `/effort`.

When working with Claude in your development environment, you'll often need to make changes to existing projects. This guide covers practical techniques for implementing changes effectively, including visual communication with screenshots and leveraging Claude's advanced reasoning capabilities.

##  Using Screenshots for Precise Communication
One of the most effective ways to communicate with Claude is through screenshots. When you want to modify a specific part of your interface, taking a screenshot helps Claude understand exactly what you're referring to.

To paste a screenshot into Claude, use `Ctrl+V` (not `Cmd+V` on macOS). This keyboard shortcut is specifically designed for pasting screenshots into the chat interface. Once you've pasted the image, you can ask Claude to make specific changes to that area of your application.

## Planning Mode
For more complex tasks that require extensive research across your codebase, you can enable Planning Mode. This feature makes Claude do thorough exploration of your project before implementing changes.

Enable Planning Mode by typing `/plan` or by pressing `Shift + Tab` twice (or once if you're already auto-accepting edits). In this mode, Claude will:

- Read more files in your project
- Create a detailed implementation plan
- Show you exactly what it intends to do
- Wait for your approval before proceeding

This gives you the opportunity to review the plan and redirect Claude if it missed something important or didn't consider a particular scenario.

*Tip*: when reviewing the plan, you can press `Ctrl+G` to open it in your text editor. You can precise edits before approving the plan, and Claude will see the final version you submit.

## Effort level: how hard Claude thinks
By default, Claude reasons through problems before answering. You'll see hints like "still thinking" while it works. If you want to see Claude's reasoning process, press `Ctrl+O` to expand the actual reasoning steps.

You can control is how Claude reasons through a problem by setting an effort level. Run `/effort` to see your current level and adjust it: `low` is faster and cheaper, `max` reasons longest on hard problems. The default depends on your model and plan — `/effort` shows you what yours is.

If you want to signal to Claude that it should do extra thinking on a single prompt, use the keyword `ultrathink` in your prompt. This signals to Claude that it should reason more on this turn, but doesn't adjust the session's effort level.

## When to Use Planning vs Effort
These two features handle different types of complexity:

**Planning Mode is best for:**

- Tasks requiring broad understanding of your codebase
- Multi-step implementations
- Changes that affect multiple files or components

**Adjusting to a higher effort level is best for:**

- Complex logic problems
- Debugging difficult issues
- Algorithmic challenges

You can combine both modes for tasks that require both breadth and depth. Just keep in mind that both features consume additional tokens, so there's a cost consideration for using them.