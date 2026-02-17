---
title: [Project Name] Hub
id: [YYYYMMDDHHMMSS] 
type: project-hub
created: [YYYY-MM-DD HH:MM:SS] 
modified: [YYYY-MM-DD HH:MM:SS]
start date: [YYYY-MM-DD HH:MM:SS] 
end date: [YYYY-MM-DD HH:MM:SS]  
retention: Long
archived: False
tags: [tags]
keywords: 
project: [Project Name]
author: [Author]
private: No
---

# [Project Name] 

## Authorization

**Business Sponsor:**

**Project Manager:**

**Team Resources:**

## Executive Summary

**Business Need:**

**Objectives:**

**Success Criteria:**

## Scope

### In Scope:

### Out of Scope:

## Stakeholders
<div style="font-size: small;">

| Name | Contact Info | Position | Role | Expectations | Classification |
| --- | --- | --- | --- | --- | --- |
|   |   |   |   |   |   |

</div>

<!-- Hidden hints
Position vs. Role: Position is usually a job title, role is the stakeholder's role in the project.

Roles:
    Project Sponsor: The person or group who provides the resources and financial support for the project.
    Stakeholders: Individuals, groups, or organizations who may affect, be affected by, or perceive themselves to be affected by a decision, activity, or outcome of a project.
    Project Team Members: Individuals who report directly to the Project Manager and perform the work necessary to produce the project's deliverables.
    Functional Manager: The person who has management authority over an organizational unit (like an IT or marketing department) and is often the one who assigns staff to the project team.


Classification: Monitor, Keep Informed, Keep Satisfied, Manage Closely

-->

<!-- Hidden Section

### Glossary of Common Terms

- term 1
- term 2

-->


## Schedule

**Start Date:**

**Projected Completion Date:**

**Actual Completion Date:**



## Budget

**Budget Amount:** $1000.00

**Budget Hours:** 40

**Contingency:** 10%

**Actual Hours:** tbd

**Time Tracker Code:** tbd


<div style="break-after: page;"></div>

```mermaid
---
config:
  themeVariables:
    xyChart:
      plotColorPalette: "#1ABC9C, #FF8C33, #3357FF, #F333FF"
---
xychart-beta
    title "Budget, Actual and Progress Hours Burn Down"
    x-axis [Jan-1, Jan-15, Jan-26, Feb-1, Feb-9, Feb-16, Mar-1, Mar-15, Apr-1]
    y-axis "Available Hours" 0 --> 240
    line "Budget Hours" [231, 200, 180, 160, 141, 23, 5, 0]
    line "Actual Hours" [231, 225, 221, 205.46, 192.44 ]
    line "Earned Value Inverse" [231,231,220, 146.5 ]
```
<span style="color: #1ABC9C; font-size: 10px">budget hours</span> - <span style="color: #FF8C33; font-size: 10px">actual hours</span> - <span style="color: #3357FF; font-size: 10px">progress hours</span>


# Risks

<div style="font-size: small;">

| **Risk Description** | **Likelihood** | **Impact** | **Response Action(s)** | **Owner** |
| --- | --- | --- | -- |-- |
| Requirements expansion during build | Possible | Major | Define and sign off on scope document before build | Analyst |

<!-- Hidden hints
Likelihood - Unlikely, Possible, Likely, Almost Certain
Impact - Minor, Moderate, Major, Significant
-->

</div>

# Transition Plan

<!-- hidden mermaid example

- Document and Transfer Knowledge/Assets
- Execute the Handover / Cutover
- Evaluate and Ensure Ongoing Value Realization

-->

# Milestones:

<!-- hidden mermaid example

```mermaid
gantt
    title       Timeline
    dateFormat  YYYY-MM-DD
    tickInterval 1month
    excludes    weekends
    
    section Planned
    kickoff                             :milestone, kickoff, 2014-06-02, 1d
    Business Case                       :p1, 2014-06-06, 10d
    Project Charter                     :p2, after p1, 4d
    Analysis and Planning               :p3, after p2, 15d
    Implementation                      :p4, after p3, 25d
    Testing                             :p5, after p4, 5d
    Deployment                          :p6, after p5, 2d
    Transition                          :p7, after p5, 5d
    Maintenance                         :crit,p7, after p6, 10d

    section Actual
    kickoff                             :milestone, kickoff, 2014-06-02, 10d
    Business Case                       :done, a1, 2014-06-15, 10d
    Project Charter                     :active, 2014-06-15, 2014-06-25
    Analysis and Planning               :a3, 2014-06-25, 15d
    Implementation                      :a4, after p3, 25d
    Testing                             :a5, after p4, 5d
    Deployment                          :a6, after p5, 2d
    Transition                          :a7, after p5, 2d
    Maintenance                         :crit,p7, after p6, 10d


```
-->


