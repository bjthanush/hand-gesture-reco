        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const result = document.getElementById('result');
        const resultCard = document.getElementById('result-card');
        const loading = document.querySelector('.loading');
        const captureBtn = document.querySelector('.capture-btn');
        const context = canvas.getContext('2d');
        
        // Stats tracking
        let predictionsCount = 0;
        let lastGesture = '--';
        let currentAccuracy = '--';

        // Initialize camera
        navigator.mediaDevices.getUserMedia({ 
            video: { 
                width: { ideal: 1280 },
                height: { ideal: 720 }
            } 
        })
        .then(stream => {
            video.srcObject = stream;
            createFloatingElements();
        })
        .catch(err => {
            console.error('Error accessing camera:', err);
            result.innerText = 'Camera access denied';
        });

        function capture() {
            // Show loading state
            loading.classList.add('active');
            captureBtn.disabled = true;
            resultCard.classList.remove('has-result');
            
            // Set canvas dimensions
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            const dataUrl = canvas.toDataURL('image/png');

            // Simulate prediction (replace with your actual API call)
            setTimeout(() => {
                // Replace this with your actual fetch call
                fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ image: dataUrl })
                })
                .then(response => response.json())
                .then(data => {
                    displayResult(data.prediction);
                })
                
            }, 1000);
        }

        function displayResult(prediction) {
            loading.classList.remove('active');
            captureBtn.disabled = false;
            
            result.innerText = prediction;
            resultCard.classList.add('has-result');
            
            // Update stats
            predictionsCount++;
            lastGesture = prediction;
            
            
            updateStats();
        }

        function updateStats() {
            document.getElementById('predictions-count').innerText = predictionsCount;
            document.getElementById('last-gesture').innerText = lastGesture;
        }

        function createFloatingElements() {
            const container = document.querySelector('.floating-elements');
            
            for (let i = 0; i < 15; i++) {
                const element = document.createElement('div');
                element.className = 'floating-element';
                element.style.left = Math.random() * 100 + '%';
                element.style.animationDelay = Math.random() * 20 + 's';
                element.style.animationDuration = (15 + Math.random() * 10) + 's';
                container.appendChild(element);
            }
        }

        // Add keyboard shortcut for capture
        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space' && !captureBtn.disabled) {
                e.preventDefault();
                capture();
            }
        });

        // Add visual feedback for video stream
        video.addEventListener('loadedmetadata', () => {
            video.style.opacity = '1';
        });