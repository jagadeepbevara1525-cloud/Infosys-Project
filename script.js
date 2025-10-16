 fileInput = document.getElementById('file');
const fileName = document.getElementById('fileName');
const form = document.getElementById('uploadForm');
const statusDiv = document.getElementById('status');

// Display selected file name
fileInput.addEventListener('change', () => {
    if(fileInput.files.length > 0){
        fileName.textContent = fileInput.files[0].name;
    } else {
        fileName.textContent = "No file chosen";
    }
});

// Handle form submission
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    if(fileInput.files.length === 0){
        statusDiv.textContent = "Please choose a file first!";
        statusDiv.style.color = 'red';
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    statusDiv.textContent = "Uploading and analyzing...";
    statusDiv.style.color = 'black';

    try {
        // Replace with the actual URL of your backend when deployed
        // For running locally in Colab, you might need a service like ngrok
        // to expose your localhost to the internet.
        // Example using ngrok: const backendUrl = 'YOUR_NGROK_URL/analyze';
        const backendUrl = 'http://127.0.0.1:5000/analyze'; // <-- **IMPORTANT: Replace with your backend URL**

        const response = await fetch(backendUrl, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'An error occurred during analysis.');
        }

        const data = await response.json();
        console.log(data); // Log the results to the console

        displayResults(data.clauses); // Display the analysis results

    } catch (error) {
        console.error('Error:', error);
        statusDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    } finally {
        form.reset();
        fileName.textContent = "No file chosen";
    }
});

function displayResults(clauses) {
    statusDiv.innerHTML = '<h2>Analysis Results:</h2>';
    if (clauses.length === 0) {
        statusDiv.innerHTML += '<p>No clauses found.</p>';
        return;
    }

    clauses.forEach(clause => {
        statusDiv.innerHTML += `
            <div style="border: 1px solid #ccc; margin-bottom: 10px; padding: 10px; margin-bottom: 20px;">
                <p><strong>Clause:</strong> ${clause.text}</p>
                <p><strong>Types:</strong> ${clause.types.join(', ') || 'None'}</p>
                <p><strong>Findings:</strong></p>
                <ul>
                    ${clause.findings.map(finding => `<li>${finding.description} (Severity: ${finding.severity})</li>`).join('') || '<li>None</li>'}
                </ul>
            </div>
        `;
    });
}