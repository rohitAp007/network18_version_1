document.getElementById('verifyCreatorBtn').addEventListener('click', verifyCreator);
document.getElementById('embedMetadataBtn').addEventListener('click', embedMetadata);
document.getElementById('runTamperingBtn').addEventListener('click', runTamperingDetection);

function verifyCreator() {
    const creatorId = document.getElementById('creatorId').value;
    const creatorName = document.getElementById('creatorName').value;

    if (creatorId === "" || creatorName === "") {
        alert("Please enter creator ID and name");
        return;
    }

    // Here you would send the creator info to the backend
    fetch('/verifyCreator', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ creatorId, creatorName })
    })
    .then(response => response.json())
    .then(data => {
        const statusElement = document.getElementById('creatorVerificationStatus');
        if (data.verified) {
            statusElement.innerHTML = <p>Creator Verified: ${creatorName}</p>;
        } else {
            statusElement.innerHTML = <p>Creator Verification Failed</p>;
        }
    });
}

function embedMetadata() {
    const videoFile = document.getElementById('videoInput').files[0];
    const creatorId = document.getElementById('creatorId').value;
    const originalSource = document.getElementById('originalSource').value;

    if (!videoFile || !creatorId || !originalSource) {
        alert("Please upload a video, and provide creator ID and source.");
        return;
    }

    const formData = new FormData();
    formData.append('video', videoFile);
    formData.append('creatorId', creatorId);
    formData.append('originalSource', originalSource);

    fetch('/embedMetadata', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const metadataElement = document.getElementById('attributionMetadata');
        metadataElement.innerHTML = <p>Metadata embedded: ${JSON.stringify(data.metadata)}</p>;
    });
}

function runTamperingDetection() {
    const videoFile = document.getElementById('videoInput').files[0];

    if (!videoFile) {
        alert("Please upload a video.");
        return;
    }

    const formData = new FormData();
    formData.append('video', videoFile);

    fetch('/detectTampering', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const tamperingResultsElement = document.getElementById('tamperingResults');
        if (data.tampered) {
            tamperingResultsElement.innerHTML = <p>Tampering Detected at frames: ${data.frames}</p>;
        } else {
            tamperingResultsElement.innerHTML = <p>No Tampering Detected</p>;
        }
    });
}