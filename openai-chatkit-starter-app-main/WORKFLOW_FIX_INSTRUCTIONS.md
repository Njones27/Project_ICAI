# Fix: Display Form Widget Instead of Text Prompt

## Current Issue
The workflow is currently asking users to provide information as text instead of displaying a form with a save button.

Current behavior:
```
Thanks. I've captured ID: 3423244.

To log your 3D print, please provide the following details...
Name: Jane Doe
Email: jane@example.com
...
```

Desired behavior:
- Show a form with input fields
- Display a "Save" button
- Collect structured data
- Pass data to second agent
- Second agent outputs the information as formatted text

---

## Root Cause
The `myAgent` in your OpenAI ChatKit workflow is not configured to return a **widget response**. It's returning text instead of a form widget.

---

## Solution: Update Workflow in OpenAI Platform

### Step 1: Access the Workflow Editor
1. Go to https://platform.openai.com/chatkit/workflows
2. Find workflow ID: `wf_69378a3a44e881908ee10067b28fbf3b0bb50f80a3aab519`
3. Click **Edit**

### Step 2: Configure "My agent" to Return Widgets

#### 2.1 Update Agent Instructions
Replace the current instructions with:

```
You are a helpful assistant for the Innovation Center, a 3D printing maker space.

When a user first contacts you:
1. Welcome them: "Welcome to the Innovation Center! This is a 3D printing maker space."
2. Capture their student ID from their initial message
3. IMMEDIATELY show them a form widget to log their 3D print

IMPORTANT: You MUST respond with a form widget (not text instructions).

The form widget should include:
- Text welcoming them
- Input field for Name (required)
- Input field for Email (required, type: email)
- Input field for Grams (required, type: number)
- Input field for TimeMin (required, type: number)
- Checkbox for Paid (optional)
- A "Save" button that submits the form

When the form is submitted:
- Extract all field values
- Return a structured JSON object matching this schema:
  {
    "defaultName": string,
    "defaultEmail": string,
    "defaultGrams": string,
    "defaultTimeMin": string,
    "defaultPaid": boolean
  }

If user has questions, tell them to ask a staff member.
```

#### 2.2 Enable Widget Responses
1. In the agent settings, find **"Response Type"** or **"Output Format"**
2. Change from **"Text"** to **"Widget"** or **"Structured + Widget"**
3. Enable **"Widget support"**

#### 2.3 Add Widget Template
In the agent configuration, add this widget template to be returned on first interaction:

**Copy this exact JSON:**

```json
{
  "type": "Card",
  "title": "3D Print Log",
  "children": [
    {
      "type": "Text",
      "value": "Welcome to the Innovation Center! Please fill out the form below to log your 3D print.",
      "size": "md"
    },
    {
      "type": "Form",
      "children": [
        {
          "type": "Label",
          "value": "Name *",
          "fieldName": "defaultName"
        },
        {
          "type": "Input",
          "name": "defaultName",
          "placeholder": "Enter your full name",
          "required": true
        },
        {
          "type": "Label",
          "value": "Email *",
          "fieldName": "defaultEmail"
        },
        {
          "type": "Input",
          "name": "defaultEmail",
          "inputType": "email",
          "placeholder": "your.email@example.com",
          "required": true
        },
        {
          "type": "Label",
          "value": "Material Used (grams) *",
          "fieldName": "defaultGrams"
        },
        {
          "type": "Input",
          "name": "defaultGrams",
          "inputType": "number",
          "placeholder": "Weight in grams",
          "required": true
        },
        {
          "type": "Label",
          "value": "Print Time (minutes) *",
          "fieldName": "defaultTimeMin"
        },
        {
          "type": "Input",
          "name": "defaultTimeMin",
          "inputType": "number",
          "placeholder": "Time in minutes",
          "required": true
        },
        {
          "type": "Checkbox",
          "name": "defaultPaid",
          "label": "Payment completed",
          "defaultChecked": false
        },
        {
          "type": "Button",
          "label": "Save",
          "submit": true,
          "style": "primary"
        }
      ]
    }
  ]
}
```

#### 2.4 Configure Output Schema
Ensure the agent has **Structured Output** enabled with this schema:

```json
{
  "type": "object",
  "properties": {
    "defaultName": { "type": "string" },
    "defaultEmail": { "type": "string" },
    "defaultGrams": { "type": "string" },
    "defaultTimeMin": { "type": "string" },
    "defaultPaid": { "type": "boolean" }
  },
  "required": ["defaultName", "defaultEmail", "defaultGrams", "defaultTimeMin", "defaultPaid"]
}
```

### Step 3: Update Second Agent ("Agent") Instructions

Update the second agent's instructions to format the data nicely:

```
Your job is to take in the structured data from the previous agent and output it as a friendly confirmation message.

You will receive this data:
- defaultName: User's full name
- defaultEmail: User's email address
- defaultGrams: Material weight in grams
- defaultTimeMin: Print time in minutes
- defaultPaid: Payment status (true/false)

Format the output as:

"✅ Print Log Saved Successfully!

Here's what we recorded:
• Name: [defaultName]
• Email: [defaultEmail]
• Material Used: [defaultGrams] grams
• Print Time: [defaultTimeMin] minutes
• Payment Status: [Paid ✓ / Not Paid ✗]

Thank you for logging your 3D print at the Innovation Center!"

Use a friendly, professional tone.
```

### Step 4: Configure Agent Connection

1. Verify the workflow flow:
   ```
   User Input → myAgent (returns widget + captures form) → agent (formats output as text)
   ```

2. Ensure data flows correctly:
   - **myAgent output** → Goes into conversation history
   - **agent input** → Receives conversation history including myAgent's structured output
   - **agent output** → Final text response to user

### Step 5: Test in Workflow Editor

1. Click **"Test"** in the workflow editor
2. Enter test input: "Hi, my student ID is 12345"
3. **Expected Result**: You should see a form with fields and a Save button
4. Fill out the form and click **"Save"**
5. **Expected Result**: Second agent should output formatted text with the form data

**If the form doesn't appear**: The agent is still in text mode, not widget mode. Go back to Step 2.2 and ensure widget responses are enabled.

### Step 6: Publish and Deploy

1. Click **"Save"** in the workflow editor
2. Click **"Publish"** or **"Deploy"**
3. Wait for deployment to complete (~1 minute)
4. Test at: https://agentkit-amazing.vercel.app

---

## Verification Checklist

After making changes, verify:

- [ ] "My agent" has **Widget Response** enabled
- [ ] "My agent" instructions mention returning a form widget
- [ ] Form widget JSON is properly configured
- [ ] All form fields have correct `name` attributes matching schema
- [ ] Save button has `submit: true`
- [ ] "My agent" has structured output schema configured
- [ ] Second agent ("Agent") receives data from first agent
- [ ] Second agent formats output as text
- [ ] Workflow is published/deployed
- [ ] Testing in production shows the form (not text prompt)

---

## Expected User Experience After Fix

### Step 1: User starts conversation
```
User: "Hi, my ID is 3423244"
```

### Step 2: Workflow displays form
The user sees:
- Welcome message
- Form with fields:
  - Name (text input)
  - Email (email input)
  - Grams (number input)
  - Time (number input)
  - Paid (checkbox)
  - **Save button**

### Step 3: User fills and submits form
User enters:
- Name: "John Doe"
- Email: "john@example.com"
- Grams: 150
- Time: 45
- Paid: ✓

User clicks **"Save"**

### Step 4: Second agent outputs formatted text
```
✅ Print Log Saved Successfully!

Here's what we recorded:
• Name: John Doe
• Email: john@example.com
• Material Used: 150 grams
• Print Time: 45 minutes
• Payment Status: Paid ✓

Thank you for logging your 3D print at the Innovation Center!
```

---

## Troubleshooting

### Issue: Still seeing text prompt instead of form
**Cause**: Widget response not enabled
**Fix**:
1. In OpenAI workflow editor, click on "My agent"
2. Find "Response Type" or "Output Format"
3. Change to "Widget" or enable "Widget support"
4. Save and republish

### Issue: Form appears but Save button doesn't work
**Cause**: Button not configured as submit
**Fix**:
1. In form widget JSON, ensure button has: `"submit": true`
2. Ensure form has proper action handler

### Issue: Data not reaching second agent
**Cause**: Output schema not configured
**Fix**:
1. Ensure "My agent" has structured output with MyAgentSchema
2. Verify conversation history is enabled
3. Check agent connection in workflow

### Issue: Form fields don't match expected data
**Cause**: Field names don't match schema
**Fix**:
1. Verify all input `name` attributes match schema exactly:
   - defaultName
   - defaultEmail
   - defaultGrams
   - defaultTimeMin
   - defaultPaid
2. Save and republish

---

## Key Configuration Points

| Setting | Location | Value |
|---------|----------|-------|
| Agent Response Type | My agent → Settings | Widget / Structured + Widget |
| Widget Template | My agent → Widget Response | form_widget_template.json |
| Output Schema | My agent → Structured Output | MyAgentSchema |
| Instructions | My agent → Instructions | Must mention returning widget |
| Second Agent Instructions | Agent → Instructions | Format data as text |
| Workflow Mode | Workflow Settings | Conversational |
| Store History | Workflow Settings | Enabled |

---

## Additional Help

If you continue to see text prompts instead of the form after following these steps:

1. **Check agent logs** in OpenAI platform for errors
2. **Clear browser cache** and test again
3. **Create a new test** in the workflow editor to see widget rendering
4. **Review widget JSON** for syntax errors using a JSON validator
5. **Contact OpenAI support** if widget responses are not available for your account tier

The key issue is that the agent needs to be configured to return **widgets**, not just **text**. This configuration happens in the OpenAI ChatKit workflow editor.
