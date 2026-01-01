/**
 * Options page script
 * Uses shared BackupUtils for import/export
 */

const statusEl = document.getElementById('status');
const btnExport = document.getElementById('btnExport');
const fileInput = document.getElementById('fileInput');

function showStatus(message, isError = false) {
    statusEl.textContent = message;
    statusEl.className = isError ? 'error' : 'success';
    setTimeout(() => {
        statusEl.className = '';
        statusEl.textContent = '';
    }, CONFIG.TIMING.notificationDuration);
}

async function handleExport() {
    try {
        await BackupUtils.exportBackup();
        showStatus("Backup exported successfully!");
    } catch {
        showStatus("Export failed.", true);
    }
}

async function handleImport(event) {
    const file = event.target.files[0];
    if (!file) return;

    try {
        await BackupUtils.importBackup(file);
        showStatus("Settings imported! Reload the extension popup to see changes.");
    } catch (err) {
        showStatus("Import failed: " + (err.message || "Unknown error"), true);
    }
    event.target.value = '';
}

btnExport.addEventListener('click', handleExport);
fileInput.addEventListener('change', handleImport);
