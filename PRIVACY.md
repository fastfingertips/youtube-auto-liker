<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/fastfingertips/youtube-auto-liker/main/docs/store/promo_marquee_dark.png">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/fastfingertips/youtube-auto-liker/main/docs/store/promo_marquee_light.png">
  <img alt="YouTube Auto Like" src="https://raw.githubusercontent.com/fastfingertips/youtube-auto-liker/main/docs/store/promo_marquee_light.png">
</picture>

# Privacy Policy for YouTube Auto Like

**Created: December 26, 2025**
**Last updated: December 26, 2025**

## Overview

YouTube Auto Like is a browser extension that helps users automatically like or dislike YouTube videos based on their channel preferences. This privacy policy explains how we handle your data.

## Data Collection

**We do not collect any personal data.**

All data is stored locally on your device using Chrome's built-in storage API. No data is ever transmitted to external servers.

### Data Stored Locally

The extension stores the following information locally on your device:

- **Whitelist**: Channel names you choose to auto-like
- **Blacklist**: Channel names you choose to auto-dislike
- **Settings**: Your preferences (timing, humanize option, etc.)
- **Activity Log**: Recent actions performed by the extension

## Data Sharing

**We do not share any data with third parties.**

- No analytics or tracking
- No external API calls
- No data transmission of any kind

## Permissions Used

The extension requires the following permissions:

| Permission | Purpose |
|------------|---------|
| `storage` | To save your preferences and channel lists locally |
| `activeTab` | To detect the current YouTube channel and interact with like/dislike buttons |
| `scripting` | To run the content script on YouTube pages |
| `host_permissions (youtube.com)` | To access YouTube pages for functionality |

## Data Security

All data remains on your local device and is never transmitted externally. Chrome's storage API provides secure local storage.

## Changes to This Policy

We may update this privacy policy from time to time. Any changes will be reflected in the "Last updated" date above.

## Contact

If you have any questions about this privacy policy, please open an issue on our GitHub repository:

https://github.com/fastfingertips/youtube-auto-liker/issues

## Open Source

This extension is open source. You can review the complete source code at:

https://github.com/fastfingertips/youtube-auto-liker
