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

    if (actionType === "lab.job.save") {
      // Extract form data from the action payload
      const formData = action.payload || {};

      try {
        // Send to backend API
        const response = await fetch("/api/actions/lab.job.save", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ form_data: formData }),
        });

        const result = await response.json();

        if (!response.ok) {
          console.error("Failed to save print job:", result.error);
          return {
            success: false,
            message: result.error || "Failed to save print job",
          };
        }

        console.log("Print job saved successfully:", result);
        return {
          success: true,
          message: result.message,
        };
      } catch (error) {
        console.error("Error saving print job:", error);
        return {
          success: false,
          message: "Network error while saving print job",
        };
      }
    }

    // Return default response for unhandled actions
    return { success: true };
  }, []);

  const chatkit = useChatKit({
    api: { getClientSecret },
    widgets: {
      onAction: handleAction,
    },
  });

  return (
    <div className="flex h-[90vh] w-full rounded-2xl bg-white shadow-sm transition-colors dark:bg-slate-900">
      <ChatKit control={chatkit.control} className="h-full w-full" />
    </div>
  );
}
