import { useMemo, useCallback } from "react";
import { ChatKit, useChatKit } from "@openai/chatkit-react";
import { createClientSecretFetcher, workflowId } from "../lib/chatkitSession";

export function ChatKitPanel() {
  const getClientSecret = useMemo(
    () => createClientSecretFetcher(workflowId),
    []
  );

  // Handle custom widget actions
  const handleAction = useCallback(async (action: any) => {
    const actionType = action?.type;

    console.log("[DEBUG] Action received:", JSON.stringify(action, null, 2));

    if (actionType === "order.submit") {
      // Extract form data from the action payload
      const formData = action.payload || {};
      console.log("[DEBUG] Form data:", JSON.stringify(formData, null, 2));
      console.log("[DEBUG] Action keys:", Object.keys(action));
      console.log("[DEBUG] Payload keys:", Object.keys(formData));

      try {
        // Send to backend API
        const response = await fetch("/api/actions/order.submit", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ payload: formData }),
        });

        const result = await response.json();

        if (!response.ok) {
          console.error("Failed to submit print job:", result.error);
          return {
            success: false,
            message: result.error || "Failed to submit print job",
          };
        }

        console.log("Print job submitted successfully:", result);

        // Return the widgets from the backend response
        return result;
      } catch (error) {
        console.error("Error submitting print job:", error);
        return {
          success: false,
          message: "Network error while submitting print job",
        };
      }
    }

    // Return default response for unhandled actions
    return { success: true };
  }, []);

  console.log("[INIT] ChatKitPanel mounted, handler registered");

  const chatkit = useChatKit({
    api: { getClientSecret },
    widgets: {
      onAction: handleAction,
    },
  });

  console.log("[INIT] ChatKit initialized with action handler");

  return (
    <div className="flex h-[90vh] w-full rounded-2xl bg-white shadow-sm transition-colors dark:bg-slate-900">
      <ChatKit control={chatkit.control} className="h-full w-full" />
    </div>
  );
}
