# Task: Fix Form Submission - Empty Data Issue

## Problem
Form submission returns empty data: `{"name":"","email":"","grams":"","time":"","paid":false}`
The form is not capturing user input when Submit is clicked.

## Root Cause Found ✓ (UPDATED)
The app uses **managed-chatkit** which renders through OpenAI's workflow system.

Issue: Form data isn't accessible to client-side handlers in managed ChatKit workflows. The form submission action is triggered but WITHOUT the form field values.

Real solution: The workflow itself needs to handle the form data using User Approval node or the form needs to use updateState to save values.

## Solution
The form in Agent Builder needs to specify client-side handling:
```tsx
<Form onSubmitAction={{ type: "order.submit", handler: "client" }}>
```

Instead of (which defaults to server/workflow handling):
```tsx
<Form onSubmitAction={{ type: "order.submit" }}>
```

## Action Items
- [x] Identify root cause - form routing to workflow instead of client handler
- [x] Update form in Agent Builder to use `handler: "client"`
- [x] Test form submission - now reaching client handler!
- [x] Form data IS being captured! Nested under payload.order
- [x] Fix backend to extract from payload.order.name instead of payload["order.name"]
- [ ] Deploy and test final solution

## Current Workflow Issue
Agent1 is configured to "collect data from widget" but isn't outputting a widget.
Agent1 needs to output the form widget as its response.

## Changes To Make
1. In Agent Builder: Configure Agent1 to output the form widget
2. Add updateState to form's onSubmitAction
3. Update frontend to read from action.state.formData
