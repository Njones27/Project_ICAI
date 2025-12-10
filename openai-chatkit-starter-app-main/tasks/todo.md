# Task: Fix Form Submission - Empty Data Issue

## Problem
Form submission returns empty data: `{"name":"","email":"","grams":"","time":"","paid":false}`
The form is not capturing user input when Submit is clicked.

## Root Cause Found ✓
From logs: The action has `"handler":"server"` and goes through `threads.custom_action`.
This means the form action is being handled by the **OpenAI workflow directly**, NOT by our frontend/backend handlers.

The issue: The form needs `handler: "client"` in the onSubmitAction config to route to our custom handler.

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
- [ ] Fix payload extraction - data is empty in action.payload
- [ ] Check browser console for DEBUG logs to see actual payload structure

## Changes To Make
1. Update form widget in Agent Builder workflow to add `handler: "client"`
2. Clean up workflow - remove unnecessary nodes
