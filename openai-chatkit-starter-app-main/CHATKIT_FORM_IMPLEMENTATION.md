# ChatKit Form Implementation Guide

## Overview
This guide explains how to implement a form with a save button in your ChatKit workflow that passes data to the agents defined in `workflowCode.py`.

## Workflow Data Structure

Your workflow expects the following data structure from the form (as defined in `workflowCode.py:4`):

```typescript
{
  defaultName: string,      // User's name
  defaultEmail: string,     // User's email
  defaultGrams: string,     // Weight in grams
  defaultTimeMin: string,   // Time in minutes
  defaultPaid: boolean      // Payment status
}
```

## ChatKit Widget Configuration

### 1. Form Widget Structure

In your OpenAI ChatKit workflow editor, configure the first agent (`myAgent`) to return a widget with this structure:

```json
{
  "type": "Card",
  "children": [
    {
      "type": "Text",
      "value": "Welcome to the Innovation Center! Please fill out the form to log your 3D print."
    },
    {
      "type": "Form",
      "children": [
        {
          "type": "Label",
          "value": "Name",
          "fieldName": "defaultName"
        },
        {
          "type": "Input",
          "name": "defaultName",
          "placeholder": "Enter your name",
          "required": true
        },
        {
          "type": "Label",
          "value": "Email",
          "fieldName": "defaultEmail"
        },
        {
          "type": "Input",
          "name": "defaultEmail",
          "inputType": "email",
          "placeholder": "Enter your email",
          "required": true
        },
        {
          "type": "Label",
          "value": "Weight (grams)",
          "fieldName": "defaultGrams"
        },
        {
          "type": "Input",
          "name": "defaultGrams",
          "inputType": "number",
          "placeholder": "Enter weight in grams",
          "required": true
        },
        {
          "type": "Label",
          "value": "Time (minutes)",
          "fieldName": "defaultTimeMin"
        },
        {
          "type": "Input",
          "name": "defaultTimeMin",
          "inputType": "number",
          "placeholder": "Enter time in minutes",
          "required": true
        },
        {
          "type": "Label",
          "value": "Payment Status",
          "fieldName": "defaultPaid"
        },
        {
          "type": "Checkbox",
          "name": "defaultPaid",
          "label": "Paid",
          "defaultChecked": false
        },
        {
          "type": "Button",
          "label": "Save",
          "submit": true,
          "style": "primary",
          "onClickAction": {
            "type": "submit_form"
          }
        }
      ]
    }
  ]
}
```

### 2. Agent Instructions Update

Your `myAgent` instructions should guide it to:
1. Welcome the user
2. Present the form widget
3. Capture the form submission
4. Return the structured data matching `MyAgentSchema`

Example agent instruction addition:

```
When the user submits the form, extract the following fields:
- defaultName: from the "defaultName" input
- defaultEmail: from the "defaultEmail" input
- defaultGrams: from the "defaultGrams" input
- defaultTimeMin: from the "defaultTimeMin" input
- defaultPaid: from the "defaultPaid" checkbox

Return this data as a structured JSON object that will be passed to the next agent.
```

### 3. Form Submission Handling

When the save button is clicked:
1. The form data is automatically captured by ChatKit
2. The data is sent back to your workflow as structured output
3. The `myAgent` processes this and outputs data matching `MyAgentSchema`
4. This output is then available in `conversationHistory` for the next agent

### 4. Data Flow

```
User Input → Form Widget → Submit Action → myAgent Output → conversationHistory → agent (final output)
```

The workflow code (lines 77-80) shows how the data flows:

```typescript
const myAgentResult = {
  output_text: JSON.stringify(myAgentResultTemp.finalOutput),
  output_parsed: myAgentResultTemp.finalOutput  // This contains your form data
};
```

This data is then added to `conversationHistory` (line 71) and passed to the second agent.

## Implementation Steps in OpenAI ChatKit Workflow Editor

### Step 1: Configure myAgent Widget Response
1. Go to your workflow in OpenAI ChatKit dashboard
2. Edit the `myAgent` configuration
3. In the agent's response configuration, add the form widget JSON structure above
4. Ensure the `outputType` is set to match `MyAgentSchema`

### Step 2: Configure Form Action Handler
1. Set the form's `onSubmitAction` to capture form data
2. The action should extract all form fields and structure them according to `MyAgentSchema`
3. Ensure the action type matches what your workflow expects

### Step 3: Test the Flow
1. Deploy your updated workflow
2. Test by entering data in the form
3. Click the "Save" button
4. Verify the data is passed to the second agent
5. Check the final output includes the form data

## Field Mapping

| Form Field Name | Schema Field | Type | Required |
|----------------|--------------|------|----------|
| defaultName | defaultName | string | Yes |
| defaultEmail | defaultEmail | string | Yes |
| defaultGrams | defaultGrams | string | Yes |
| defaultTimeMin | defaultTimeMin | string | Yes |
| defaultPaid | defaultPaid | boolean | No |

## Validation

The form includes basic HTML5 validation:
- **Name**: Required text field
- **Email**: Required email field with format validation
- **Grams**: Required number field
- **Time**: Required number field
- **Paid**: Optional checkbox (defaults to false)

## Troubleshooting

### Issue: Data not passing to second agent
**Solution**: Ensure `myAgent` has `outputType: MyAgentSchema` set and returns structured data matching the schema.

### Issue: Form not submitting
**Solution**: Check that the button has `submit: true` and the form has proper `name` attributes on all inputs.

### Issue: Data format mismatch
**Solution**: Verify that `defaultGrams` and `defaultTimeMin` are strings (not numbers) as defined in the schema, even though they use number inputs.

## Example Workflow State After Form Submission

```typescript
{
  studentid: "12345",  // From initial input
  setdata: {
    Name: "John Doe",           // From defaultName
    Email: "john@example.com",  // From defaultEmail
    TimeMin: "45",              // From defaultTimeMin
    Grams: "150",               // From defaultGrams
    Paid: true                  // From defaultPaid
  }
}
```

## Additional Resources

- [OpenAI ChatKit Documentation](https://platform.openai.com/docs/guides/chatkit)
- [ChatKit Widgets Reference](https://platform.openai.com/docs/guides/chatkit/widgets)
- [Agent Builder Guide](https://platform.openai.com/docs/guides/agents)

## Notes

- The form widget configuration must be done in the OpenAI ChatKit workflow editor, not in this codebase
- The frontend (`managed-chatkit/frontend`) automatically renders whatever widgets the workflow returns
- The `workflowCode.py` file defines the data structure but the actual form is configured server-side in OpenAI
- The workflow ID in your deployment matches the one in `workflowCode.py` line 62
