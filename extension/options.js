// Saves options to chrome.storage
function save_options() {
    const mode = document.getElementById('mode').value;
    chrome.storage.sync.set({
        filterMode: mode,
    }, function () {
        const status = document.getElementById('status');
        status.textContent = 'Options saved.';
        setTimeout(function () {
            status.textContent = '';
        }, 750);
    });
}

// Restores select box and checkbox state using the preferences
// stored in chrome.storage.
function restore_options() {
    chrome.storage.sync.get([filterMode], function (items) {
        document.getElementById('mode').value = items.filterMode;
    });
}
document.addEventListener('DOMContentLoaded', restore_options);
document.getElementById('save').addEventListener('click', save_options);