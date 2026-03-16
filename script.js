const fileInput = document.getElementById('file-input');
const output = document.getElementById('output');

fileInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // 1. Validation Logic
    const isPython = file.name.endsWith('.py');
    const isBlend = file.name.endsWith('.blend');

    if (!isPython && !isBlend) {
        alert('Please upload a .py or .blend file.');
        return;
    }

    // 2. Dissection Logic
    const reader = new FileReader();

    reader.onload = (e) => {
        const content = e.target.result;
        
        if (isPython) {
            // Basic "Dissection" example: Count how many functions are defined
            const functionCount = (content.match(/def /g) || []).length;
            const importCount = (content.match(/import /g) || []).length;

            output.innerHTML = `
                <p style="color: #f5792a;"><strong>Analysis Complete:</strong></p>
                <ul>
                    <li>File: ${file.name}</li>
                    <li>Functions found: ${functionCount}</li>
                    <li>Libraries imported: ${importCount}</li>
                </ul>
                <p><em>Preview:</em></p>
                <pre style="background: #1d1d1d; padding: 10px; border-radius: 4px;">${content.substring(0, 200)}...</pre>
            `;
        } else {
            output.innerHTML = `<p>Detected Blender Binary (.blend). Binary parsing requires a specialized decoder.</p>`;
        }
    };

    // Read the file as text
    if (isPython) {
        reader.readAsText(file);
    } else {
        // .blend files are binary, so we handle them differently
        output.innerHTML = `Preparing to dissect binary file: ${file.name}`;
    }
});
