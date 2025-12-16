// Chrome Extension MV3 Service Worker

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "updateIcon") {
        const tabId = sender.tab.id;

        switch (request.status) {
            case "like":
                // Green Badge for LIKE
                chrome.action.setBadgeText({ text: "LIKE", tabId: tabId });
                chrome.action.setBadgeBackgroundColor({ color: "#00E676", tabId: tabId });
                break;

            case "dislike":
                // Red Badge for DISLIKE
                chrome.action.setBadgeText({ text: "DIS", tabId: tabId });
                chrome.action.setBadgeBackgroundColor({ color: "#FF5252", tabId: tabId });
                break;

            case "neutral":
                // Gray Badge for NEUTRAL (only if enabled)
                chrome.action.setBadgeText({ text: "...", tabId: tabId });
                chrome.action.setBadgeBackgroundColor({ color: "#9AA0A6", tabId: tabId });
                break;

            case "disabled":
                // Explicitly disabled
                chrome.action.setBadgeText({ text: "OFF", tabId: tabId });
                chrome.action.setBadgeBackgroundColor({ color: "#666666", tabId: tabId });
                break;

            case "none":
            default:
                // Clear Badge
                chrome.action.setBadgeText({ text: "", tabId: tabId });
                break;
        }
    }
});