import { z } from "zod";
import { Agent, AgentInputItem, Runner, withTrace } from "@openai/agents";

const AgentSchema = z.object({ name: z.string(), email: z.string(), grams: z.string(), time: z.string(), paid: z.boolean() });
const AgentSchema1 = z.object({ defaultName: z.string(), defaultEmail: z.string(), defaultGrams: z.string(), defaultTime: z.string(), defaultPaid: z.boolean() });
const AgentSchema2 = z.object({ defaultName: z.string(), defaultEmail: z.string(), defaultGrams: z.string(), defaultTime: z.string(), defaultPaid: z.boolean() });
const agent = new Agent({
  name: "Agent",
  instructions: `The user just submitted the print job form with the order.submit action.

Extract the submitted form data and output it as clean JSON:
{
  \"name\": \"<value from order.name field>\",
  \"email\": \"<value from order.email field>\",
  \"grams\": \"<value from order.grams field>\",
  \"time\": \"<value from order.time field>\",
  \"paid\": <value from order.paid field>
}`,
  model: "gpt-5-nano",
  outputType: AgentSchema,
  modelSettings: {
    reasoning: {
      effort: "minimal",
      summary: "auto"
    },
    store: true
  }
});

const agent1 = new Agent({
  name: "Agent",
  instructions: `#Role 
You are a helpful assistant for the Innovation Center, a 3D printing maker space. Collect the data from the widget`,
  model: "gpt-5-nano",
  outputType: AgentSchema1,
  modelSettings: {
    reasoning: {
      effort: "low",
      summary: "auto"
    },
    store: true
  }
});

const agent2 = new Agent({
  name: "Agent",
  instructions: "You receive validated print job data as JSON from the previous agent into your widget",
  model: "gpt-5-nano",
  outputType: AgentSchema2,
  modelSettings: {
    reasoning: {
      effort: "low",
      summary: "auto"
    },
    store: true
  }
});

const approvalRequest = (message: string) => {

  // TODO: Implement
  return true;
}

type WorkflowInput = { input_as_text: string };


// Main code entrypoint
export const runWorkflow = async (workflow: WorkflowInput) => {
  return await withTrace("InnovationCenterAgentWorkflow", async () => {
    const state = {
      studentid: null,
      results: {
        defaultName: "",
        defaultEmail: "",
        defaultGrams: "",
        defaultTime: "",
        defaultPaid: false
      }
    };
    const conversationHistory: AgentInputItem[] = [
      { role: "user", content: [{ type: "input_text", text: workflow.input_as_text }] }
    ];
    const runner = new Runner({
      traceMetadata: {
        __trace_source__: "agent-builder",
        workflow_id: "wf_69378a3a44e881908ee10067b28fbf3b0bb50f80a3aab519"
      }
    });
    const agentResultTemp = await runner.run(
      agent1,
      [
        ...conversationHistory
      ]
    );
    conversationHistory.push(...agentResultTemp.newItems.map((item) => item.rawItem));

    if (!agentResultTemp.finalOutput) {
        throw new Error("Agent result is undefined");
    }

    const agentResult = {
      output_text: JSON.stringify(agentResultTemp.finalOutput),
      output_parsed: agentResultTemp.finalOutput
    };
    const approvalMessage = "";

    if (approvalRequest(approvalMessage)) {
        const agentResultTemp1 = await runner.run(
          agent,
          [
            ...conversationHistory
          ]
        );
        conversationHistory.push(...agentResultTemp1.newItems.map((item) => item.rawItem));

        if (!agentResultTemp1.finalOutput) {
            throw new Error("Agent result is undefined");
        }

        const agentResult1 = {
          output_text: JSON.stringify(agentResultTemp1.finalOutput),
          output_parsed: agentResultTemp1.finalOutput
        };
        const agentResultTemp2 = await runner.run(
          agent2,
          [
            ...conversationHistory
          ]
        );
        conversationHistory.push(...agentResultTemp2.newItems.map((item) => item.rawItem));

        if (!agentResultTemp2.finalOutput) {
            throw new Error("Agent result is undefined");
        }

        const agentResult2 = {
          output_text: JSON.stringify(agentResultTemp2.finalOutput),
          output_parsed: agentResultTemp2.finalOutput
        };
    } else {

    }
  });
}
