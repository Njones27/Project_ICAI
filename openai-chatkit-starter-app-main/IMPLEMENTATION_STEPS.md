# Step-by-Step: Implementing the Save Button in OpenAI ChatKit Workflow

## Overview
This guide will help you configure the form widget with a working save button in your OpenAI ChatKit workflow editor to pass data from the form to your agents.

## Prerequisites
- Access to OpenAI ChatKit workflow editor
- Workflow ID: `wf_69378a3a44e881908ee10067b28fbf3b0bb50f80a3aab519`
- Your workflow code in `workflowCode.py` (TypeScript)

---

## Step 1: Access Your Workflow in OpenAI Platform

1. Go to https://platform.openai.com/chatkit/workflows
2. Find your workflow: **InnovationCenterAgentWorkflow**
3. Click **Edit** to open the workflow editor

---

## Step 2: Configure the First Agent (myAgent)

### 2.1 Update Agent Configuration

1. Click on the **"My agent"** node in the workflow editor
2. Verify the following settings:
   - **Name**: My agent
   - **Model**: gpt-5-nano
   - **Output Type**: Set to structured output with this schema:
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

### 2.2 Update Agent Instructions

Update the agent instructions to:

```
Your job is to welcome the user to the Innovation Center. This is a 3D printing maker space, and if the user has a question tell them to ask a staff member.

When the user first messages you:
1. Welcome them to the Innovation Center
2. Show them a form to log their 3D print using a Card widget
3. The form should collect: Name, Email, Weight (grams), Time (minutes), and Payment status

When the user submits the form:
1. Extract all form fields
2. Return a structured JSON object with these exact field names:
   - defaultName (string)
   - defaultEmail (string)
   - defaultGrams (string)
   - defaultTimeMin (string)
   - defaultPaid (boolean)

Always validate that the email is in proper format and all required fields are filled.
```

### 2.3 Add Widget Response

1. In the agent configuration, find the **"Widget Response"** or **"Response Template"** section
2. Set the response type to **"Widget"**
3. Copy the contents of `form_widget_template.json` and paste it into the widget configuration

**OR** manually configure the widget:

- Click **"Add Widget"** → **"Card"**
- Add a **Text** widget with your welcome message
- Add a **Form** widget
- Inside the Form, add:
  - **Input** field for Name (name: "defaultName", required: true)
  - **Input** field for Email (name: "defaultEmail", inputType: "email", required: true)
  - **Input** field for Grams (name: "defaultGrams", inputType: "number", required: true)
  - **Input** field for Time (name: "defaultTimeMin", inputType: "number", required: true)
  - **Checkbox** for Payment (name: "defaultPaid")
  - **Button** labeled "Save" (submit: true, style: "primary")

---

## Step 3: Configure Form Submission Handler

### 3.1 Set Up the Save Button Action

1. Click on the **Button** widget (Save button)
2. Set properties:
   - **Label**: "Save"
   - **Type**: Submit
   - **Style**: Primary
3. In the **On Click** section:
   - **Action Type**: "submit_form" or "custom_action"
   - **Action Name**: "save_print_log"

### 3.2 Configure Form Data Extraction

1. In the agent settings, find **"Form Handlers"** or **"Actions"**
2. Add a handler for "save_print_log" action
3. Configure it to extract form data:
   ```json
   {
     "action": "save_print_log",
     "extract_fields": [
       "defaultName",
       "defaultEmail",
       "defaultGrams",
       "defaultTimeMin",
       "defaultPaid"
     ]
   }
   ```

---

## Step 4: Configure the Second Agent (agent)

### 4.1 Update Agent Configuration

1. Click on the **"Agent"** node in the workflow editor
2. Verify settings:
   - **Name**: Agent
   - **Model**: gpt-5-nano
   - **Input**: Should receive output from "My agent"

### 4.2 Update Agent Instructions

```
Your job is to take in the data from the previous agent and output it as text.

You will receive structured data with these fields:
- defaultName: User's name
- defaultEmail: User's email
- defaultGrams: Weight of material used in grams
- defaultTimeMin: Print time in minutes
- defaultPaid: Payment status (true/false)

Format this information in a friendly confirmation message like:

"Thank you [Name]! Your 3D print has been logged with the following details:
- Email: [Email]
- Material Used: [Grams]g
- Print Time: [TimeMin] minutes
- Payment Status: [Paid/Not Paid]

Your print log has been saved successfully!"
```

---

## Step 5: Configure Data Flow Between Agents

### 5.1 Connect the Agents

1. Ensure there's a connection line from **"My agent"** to **"Agent"**
2. Click on the connection line
3. Configure data passing:
   - **Source**: My agent → output_parsed
   - **Destination**: Agent → input
   - **Format**: JSON

### 5.2 Set Up Conversation History

1. Ensure both agents have access to conversation history
2. In workflow settings, enable **"Store conversation history"**
3. This ensures the second agent can see the form data from the first agent

---

## Step 6: Test the Workflow

### 6.1 Use Workflow Test Panel

1. In the workflow editor, click **"Test"** or **"Preview"**
2. Enter a test message like: "Hello, I'd like to log my print"
3. The form should appear
4. Fill in the form:
   - Name: "John Doe"
   - Email: "john@example.com"
   - Grams: "150"
   - Time: "45"
   - Paid: ✓
5. Click **"Save"**
6. Verify:
   - Form submits without errors
   - Second agent receives the data
   - Final output includes all form values

### 6.2 Check Data Flow

In the test panel, you should see:
1. **My agent output**:
   ```json
   {
     "defaultName": "John Doe",
     "defaultEmail": "john@example.com",
     "defaultGrams": "150",
     "defaultTimeMin": "45",
     "defaultPaid": true
   }
   ```
2. **Agent output**:
   ```
   Thank you John Doe! Your 3D print has been logged...
   ```

---

## Step 7: Deploy the Workflow

1. Click **"Save"** in the workflow editor
2. Click **"Publish"** or **"Deploy"**
3. The workflow will be deployed with workflow ID: `wf_69378a3a44e881908ee10067b28fbf3b0bb50f80a3aab519`
4. Your Vercel app will automatically use the updated workflow

---

## Step 8: Test in Production

1. Go to your live app: https://agentkit-amazing.vercel.app
2. Start a conversation
3. Fill out the form
4. Click **"Save"**
5. Verify the data flows correctly through both agents

---

## Troubleshooting

### Issue: Form doesn't appear
**Solution**:
- Check that "My agent" is set to return a widget response
- Verify the widget JSON is valid
- Check agent instructions include widget rendering

### Issue: Save button doesn't work
**Solution**:
- Verify button has `submit: true` property
- Check that all form inputs have unique `name` attributes
- Ensure form is properly configured with action handler

### Issue: Data not reaching second agent
**Solution**:
- Check that "My agent" has `outputType` set to the schema
- Verify the agents are connected in the workflow
- Check conversation history is enabled
- Review the data flow configuration

### Issue: Type mismatch errors
**Solution**:
- Ensure `defaultGrams` and `defaultTimeMin` are strings (not numbers)
- Verify `defaultPaid` is boolean
- Check all required fields are present

### Issue: Form validation not working
**Solution**:
- Add `required: true` to mandatory form fields
- Use proper `inputType` for email ("email")
- Test with invalid data to ensure validation triggers

---

## Data Structure Reference

### Expected Form Output (MyAgentSchema)
```typescript
{
  defaultName: string,      // "John Doe"
  defaultEmail: string,     // "john@example.com"
  defaultGrams: string,     // "150" (as string, not number!)
  defaultTimeMin: string,   // "45" (as string, not number!)
  defaultPaid: boolean      // true or false
}
```

### Workflow State Structure
```typescript
{
  studentid: string | null,
  setdata: {
    Name: string,          // Maps from defaultName
    Email: string,         // Maps from defaultEmail
    TimeMin: number | null, // Maps from defaultTimeMin (converted)
    Grams: number | null,   // Maps from defaultGrams (converted)
    Paid: boolean | null    // Maps from defaultPaid
  }
}
```

---

## Additional Resources

- Form widget template: `form_widget_template.json`
- Implementation guide: `CHATKIT_FORM_IMPLEMENTATION.md`
- Workflow code: `workflowCode.py`
- OpenAI ChatKit Docs: https://platform.openai.com/docs/guides/chatkit
- Widget Reference: https://platform.openai.com/docs/guides/chatkit/widgets

---

## Support

If you encounter issues:
1. Check the OpenAI ChatKit documentation
2. Review the workflow test logs
3. Check browser console for errors (F12)
4. Verify environment variables are set correctly in Vercel
5. Test the workflow in the OpenAI platform first before testing in production
