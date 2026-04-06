# Tea Cabinet Snapshot — Product Requirements

## Problem

Serious tea collectors (30+ varieties) need a way to know what's in their
collection and what needs attention because they lose track as the collection
outgrows memory, leading to waste and redundant purchases.

## Target User

Maya — a tea collector with 30-50 varieties across loose leaf, compressed
cakes, and sachets. Buys 2-3 new teas per month from online vendors and
local shops. Cares about freshness (especially for green and white teas)
but relies on memory to track open dates and quantities. Has tried
spreadsheets but doesn't maintain them.

## Hypothesis

We believe that giving tea collectors a visual, at-a-glance inventory with
automated freshness tracking will reduce wasted tea by 50% and eliminate
duplicate purchases, because the core pain is not lack of knowledge about
tea care but lack of visibility into what they own.

## Solution

A collection tracker that gives tea collectors an at-a-glance view of what
they own, what's aging, and what needs attention. The core shift: the cabinet
becomes a managed collection instead of a mystery. Adding a tea takes seconds
(scan or snap), and the system surfaces timely nudges rather than requiring
the user to remember to check.

## Core Interaction

Opening the app and immediately seeing which teas need attention — the
"what should I brew today?" moment.

## What This Is NOT

- Not a social platform for sharing collections
- Not a tea education or brewing guide
- Not a marketplace or vendor integration

## Scope

**Building:** collection-overview, add-tea-form, tea-detail

**Not building:** Search/filter within collection, Notification/reminder system for drink_soon teas, Import from spreadsheet, Image upload for tea packaging

## Success Criteria

- Spec package passes all validation checks
- Implementation agent builds a working prototype without clarifying questions
