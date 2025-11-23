# Workflow, Project and Task Management

## Action items 

Incomplete **action items**, any action that must be completed, are reflected in the note body as `- [ ] action item description`.  Complete action items are reflected in the note body as `- [x] action item description`.

Comments, modifiers and results can be associated with an action item using the `<comments>` tag.  For example - 

```markdown
Things to do 
- [ ] update the readme file
<comments>
    Remember first draft needed more detail about how to find action items.
</comments>
- [ ] 2026-02-03 approve time sheets before cut off
- [x] 2026-02-03 start release preparation
<comments>
Done, dev manager reports that the release manager is prepared and ready for Thursday's release
</comments>
```
In the above example, the feedback about the release manager will be associated with the "start release preparation" action item.


## Finding Incomplete action items 

Use the `get-actionItems` command to return incomplete action items.


