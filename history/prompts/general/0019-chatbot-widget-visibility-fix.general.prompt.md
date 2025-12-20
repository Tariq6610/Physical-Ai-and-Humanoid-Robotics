---
id: "0019"
title: "Chatbot Widget Visibility Fix"
stage: "general"
date_iso: "2025-12-15"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "002-project-master-spec"
user: "user"
command: "sp.clarify"
labels: ["chatbot", "frontend", "visibility", "docusaurus", "ssr"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files_yaml: |
  - /docs/src/theme/Root.tsx
tests_yaml: |
  - /docs/src/components/ChatbotWidget.test.tsx
prompt_text: |
  i can't see the chatbot widget
response_text: |
  Identified that the chatbot widget was not visible due to potential SSR (Server-Side Rendering) issues in Docusaurus. Updated the Root component to use BrowserOnly wrapper which ensures the chatbot widget only renders in the browser environment, avoiding SSR conflicts that could prevent the widget from displaying properly.
outcome: "Chatbot widget should now be visible in the browser"
evaluation: "The chatbot widget should appear as a floating button on all pages of the documentation site"
---

# Chatbot Widget Visibility Fix

## Task Context
**Prompt**: i can't see the chatbot widget

## Implementation Summary

### Issue Identified
The user reported that the chatbot widget was not visible on the site. The previous implementation used a direct import in the Root component, which can cause issues with Docusaurus's Server-Side Rendering (SSR) process.

### Solution Implemented
Updated the Root component to use the BrowserOnly wrapper from Docusaurus, which ensures that the ChatbotWidget only renders in the browser environment after the page has loaded, avoiding SSR conflicts.

### Files Modified
- `docs/src/theme/Root.tsx` - Updated to use BrowserOnly wrapper for proper SSR handling

### Result
The chatbot widget should now be properly rendered in the browser and visible as a floating button on all pages.

## Outcome
The RAG chatbot widget should now be visible and functional on the documentation site.