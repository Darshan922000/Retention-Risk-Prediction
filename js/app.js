document.addEventListener('DOMContentLoaded', function() {
    // Tab functionality
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    // Base API URL
    const API_BASE_URL = 'http://localhost:8000';

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.getAttribute('data-tab');
            
            // Remove active class from all buttons and content
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked button and corresponding content
            button.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });

    // Risk score button selection
    const riskButtons = document.querySelectorAll('.risk-btn');
    const riskScoreInput = document.getElementById('risk_score');

    riskButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove selected class from all buttons
            riskButtons.forEach(btn => btn.classList.remove('selected'));
            
            // Add selected class to clicked button
            button.classList.add('selected');
            
            // Update hidden input value
            riskScoreInput.value = button.getAttribute('data-value');
        });
    });

    // Function to convert markdown to HTML
    function formatEmailContent(text) {
        if (!text) return '';
        
        // Remove quotes at beginning and end if present
        if (text.startsWith('"') && text.endsWith('"')) {
            text = text.substring(1, text.length - 1);
        }
        
        // Replace markdown newline patterns with HTML line breaks
        text = text
            .replace(/\\n\\n/g, '\n\n')  // Double newlines to paragraph breaks
            .replace(/\\n/g, '\n')        // Single newlines
            .replace(/\\\\/g, '\\');      // Escaped backslashes
        
        // Process the text by paragraphs to maintain structure
        const paragraphs = text.split('\n\n');
        const processedParagraphs = paragraphs.map(paragraph => {
            // Skip empty paragraphs
            if (!paragraph.trim()) return '';
            
            // Process headers
            if (paragraph.startsWith('# ')) {
                return `<h1>${paragraph.substring(2).trim()}</h1>`;
            } else if (paragraph.startsWith('## ')) {
                return `<h2>${paragraph.substring(3).trim()}</h2>`;
            } else if (paragraph.startsWith('### ')) {
                return `<h3>${paragraph.substring(4).trim()}</h3>`;
            }
            
            // Process lists - this is simplistic, would need more logic for nested lists
            if (paragraph.includes('\n- ') || paragraph.startsWith('- ')) {
                const listItems = paragraph.split('\n').filter(line => line.trim().startsWith('- '));
                if (listItems.length > 0) {
                    const listContent = listItems
                        .map(item => `<li>${item.substring(2).trim()}</li>`)
                        .join('');
                    return `<ul>${listContent}</ul>`;
                }
            }
            
            // Process normal paragraphs
            // First apply inline formatting
            let formattedParagraph = paragraph
                // Bold
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/__(.*?)__/g, '<strong>$1</strong>')
                // Italic
                .replace(/\*(.*?)\*/g, '<em>$1</em>')
                .replace(/_(.*?)_/g, '<em>$1</em>')
                // Links
                .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2">$1</a>');
            
            // Wrap in paragraph tags
            return `<p>${formattedParagraph}</p>`;
        });
        
        return processedParagraphs.join('');
    }

    // Form validation and submission for Email Generator
    const emailForm = document.getElementById('email-form');
    const emailContent = document.getElementById('email-content');

    emailForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Check if risk score is selected
        if (!riskScoreInput.value) {
            alert('Please select a risk score');
            return;
        }
        
        // Create request data object
        const formData = new FormData(emailForm);
        const requestData = {};
        
        formData.forEach((value, key) => {
            // Convert number fields to actual numbers
            if (key === 'annual_premium') {
                requestData[key] = parseFloat(value);
            } else if (key === 'claims_last_3_years' || key === 'client_tenure_years') {
                requestData[key] = parseInt(value, 10);
            } else {
                requestData[key] = value;
            }
        });
        
        try {
            // Show loading state
            emailContent.innerHTML = 'Generating email...';
            
            // Send API request with full URL
            const response = await fetch(`${API_BASE_URL}/generate_email`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            // Parse response
            const result = await response.text();
            
            // Format and display markdown response
            emailContent.innerHTML = formatEmailContent(result);
            
            // Scroll to result
            document.getElementById('email-result').scrollIntoView({ behavior: 'smooth' });
        } catch (error) {
            console.error('Error generating email:', error);
            emailContent.innerHTML = `<div class="error">Error: ${error.message}</div>`;
        }
    });

    // Form submission for Company Enrichment
    const enrichmentForm = document.getElementById('enrichment-form');
    const companyData = document.getElementById('company-data');

    enrichmentForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Get LinkedIn URL
        const linkedinUrl = document.getElementById('company_linkedin_url').value;
        
        try {
            // Show loading state
            companyData.textContent = 'Loading company data...';
            
            // Send API request with full URL
            const response = await fetch(`${API_BASE_URL}/enrich_company`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ company_linkedin_url: linkedinUrl })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            // Parse response
            const result = await response.json();
            
            // Format and display JSON data
            companyData.textContent = JSON.stringify(result, null, 2);
            
            // Scroll to result
            document.getElementById('enrichment-result').scrollIntoView({ behavior: 'smooth' });
        } catch (error) {
            console.error('Error enriching company data:', error);
            companyData.textContent = `Error: ${error.message}`;
        }
    });
}); 