document.addEventListener('DOMContentLoaded', () => {
    // Tab switching
    const tabBtns = document.querySelectorAll('.tab-btn');
    const forms = document.querySelectorAll('.form');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all buttons and forms
            tabBtns.forEach(b => b.classList.remove('active'));
            forms.forEach(f => f.classList.remove('active'));

            // Add active class to clicked button and corresponding form
            btn.classList.add('active');
            const formId = `${btn.dataset.tab}Form`;
            document.getElementById(formId).classList.add('active');
        });
    });

    // File upload preview
    const fileInput = document.getElementById('fileContent');
    const fileLabel = document.querySelector('.file-text');

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            fileLabel.textContent = fileInput.files[0].name;
        } else {
            fileLabel.textContent = 'Escolher arquivo';
        }
    });

    // Form submissions
    const textForm = document.getElementById('textForm');
    const fileForm = document.getElementById('fileForm');
    const result = document.getElementById('result');

    textForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const content = document.getElementById('textContent').value;
        const source = document.getElementById('textSource').value;

        if (!content) {
            alert('Por favor, insira um texto para verificar.');
            return;
        }

        try {
            const response = await fetch('/api/v1/verify', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    content,
                    content_type: 'text',
                    source_url: source || undefined
                })
            });

            if (!response.ok) {
                throw new Error('Erro ao verificar o texto');
            }

            const data = await response.json();
            displayResult(data);
        } catch (error) {
            alert('Erro ao verificar o texto: ' + error.message);
        }
    });

    fileForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const file = document.getElementById('fileContent').files[0];
        const source = document.getElementById('fileSource').value;

        if (!file) {
            alert('Por favor, selecione um arquivo para verificar.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);
        formData.append('content_type', file.type.startsWith('image/') ? 'image' : 'video');
        if (source) formData.append('source_url', source);

        try {
            const response = await fetch('/api/v1/verify/file', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Erro ao verificar o arquivo');
            }

            const data = await response.json();
            displayResult(data);
        } catch (error) {
            alert('Erro ao verificar o arquivo: ' + error.message);
        }
    });

    function displayResult(data) {
        // Update status badge
        const statusBadge = document.getElementById('statusBadge');
        statusBadge.textContent = data.classification;
        statusBadge.className = 'status-badge';
        
        switch (data.classification.toLowerCase()) {
            case 'verificado':
                statusBadge.classList.add('verified');
                break;
            case 'suspeito':
                statusBadge.classList.add('suspicious');
                break;
            case 'falso':
                statusBadge.classList.add('fake');
                break;
        }

        // Update confidence meter
        const confidenceFill = document.getElementById('confidenceFill');
        const confidenceValue = document.getElementById('confidenceValue');
        const confidence = Math.round(data.confidence * 100);
        confidenceFill.style.width = `${confidence}%`;
        confidenceValue.textContent = `${confidence}%`;

        // Update explanation
        document.getElementById('explanationText').textContent = data.explanation;

        // Update sources
        const sourcesList = document.getElementById('sourcesList');
        sourcesList.innerHTML = '';
        data.sources.forEach(source => {
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = source;
            a.textContent = source;
            a.target = '_blank';
            li.appendChild(a);
            sourcesList.appendChild(li);
        });

        // Show result
        result.classList.remove('hidden');
        result.scrollIntoView({ behavior: 'smooth' });
    }
}); 