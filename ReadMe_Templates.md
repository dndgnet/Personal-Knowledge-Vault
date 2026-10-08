# ReadMe_Templates.md

This document describes every template available in the `_templates/` folder. These templates are used by the various `add-*.py` and `project-*.py` scripts when creating new notes in the Personal Knowledge Vault.

Templates fall into two main categories:
- **General / PKV templates** — used for personal, journal, meeting, and vault-level notes.
- **Project templates** — used inside a `_Projects/<Project Name>/` folder. Most start with `project_`.

## Templates

## atomic_template.markdown
Small atomic notes used as building blocks. Good for quick facts, definitions, or reusable snippets that can be linked from other notes.

## pkv_chat_template.markdown
Quick chat or instant-message style notes. Useful for capturing informal conversations.

## pkv_email_template.markdown
Template for archiving or summarizing emails. Includes fields for sender, recipients, subject, and body.

## pkv_event_template.markdown
Calendar-style event or reminder notes. Includes start/end dates and can be used for both personal and project events.

## pkv_hub_template.markdown
Personal hub or index note. Acts as a central dashboard for your vault or daily work.

## pkv_idea_template.markdown
Personal ideas and brainstorming notes. Good for capturing thoughts that are not yet tied to a specific project.

## pkv_journal_template.markdown
Daily journal entry. Automatically includes the OS username in the title (e.g. "Daily Journal david 2026-10-07") so multiple users can have their own journals.

## pkv_meeting_template.markdown
General meeting notes. Includes agenda, attendees, discussion points, and action items.

## project_assumption_template.markdown
Project assumption or constraint documentation. Part of a typical RAID log.

## project_backlogcomment_template.markdown
Comments or updates on a project backlog item.

## project_budget_template.markdown
Budget tracking, cost estimates, and financial notes for a project.

## project_changerequest_template.markdown
Formal change request documentation for projects.

## project_chat_template.markdown
Project-specific chat or informal discussion log.

## project_decision_lite_template.markdown
Lightweight decision record. Simpler version of the full decision template.

## project_decision_template.markdown
Full decision record including rationale, options considered, and outcome.

## project_dependency_template.markdown
Project dependencies, blockers, and external dependencies.

## project_determination_template.markdown
Formal determinations or rulings made during a project.

## project_documentation_template.markdown
Project documentation, specifications, or reference material.

## project_email_template.markdown
Project-related email archive or summary.

## project_event_template.markdown
Project calendar event or milestone-related event.

## project_executive_summary_template.markdown
High-level executive summary for a project. Designed to be unique per project.

## project_hub_template.markdown
Main project hub note / single source of truth. Usually named "Project Brief.md". Designed to be unique per project.

## project_idea_template.markdown
Project-specific ideas and innovation tracking.

## project_introduction_template.markdown
Project charter, kick-off notes, or introduction summary.

## project_issue_template.markdown
Project issues (part of RAID logging).

## project_meeting_template.markdown
Structured project meeting notes with agenda, attendees, and outcomes.

## project_milestones_template.markdown
Milestone tracking and status table for a project.

## project_progress_template.markdown
Weekly or periodic progress updates. Uses a `sub id` (001, 002, …) so multiple progress notes can exist per project.

## project_report_template.markdown
Formal project status or final reports.

## project_risk_template.markdown
Project risks (part of RAID logging).

## project_roi_template.markdown
Return on Investment analysis and financial justification.

## project_schedule_template.markdown
Project schedule, timeline, and Gantt-related notes.

## project_scope_template.markdown
Project scope definition and change control documentation.

## project_task_template.markdown
Individual project tasks or to-dos. Uses a `sub id`.

## project_transition_plan_template.markdown
Project close-out, handover, or transition planning.

## Usage Notes

- Most templates contain placeholder tokens such as `[YYYYMMDDHHMMSS]`, `[sub id]`, `[Project Name]`, `[Current User]`. These are replaced automatically by the Python scripts when a note is created.
- **Journal notes** include the OS username in the title to support multiple users.
- **Progress, task, risk, issue, decision, assumption,** and similar notes use a `sub id` field to allow multiple related entries per project.
- The `project_hub_template` and `project_executive_summary_template` are intended to be **unique** per project.

See `ReadMe.md` and `ReadMe_ProjectManagement.md` for overall usage and how to create notes.

---

**Last updated**: 2026-10-07
