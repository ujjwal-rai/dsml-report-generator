const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const fetch = (...args) => import('node-fetch').then(({ default: fetch }) => fetch(...args));

function removeDoubleAsterisk(input) {
    return input.replace(/\*\*/g, ''); // Use regex to match all occurrences of '**'
}

exports.processData = async (req, res) => {
    const datasetFile = req.files['dataset'][0].path;
    const featureDescFile = req.files['featureDesc'][0].path;

    try {
        // Run the Python script for data processing
        const pythonProcess = spawn('python', ['data_analysis.py', datasetFile, featureDescFile]);

        let output = '';
        pythonProcess.stdout.on('data', (data) => {
            output += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            console.error('Python script error:', data.toString());
        });

        pythonProcess.on('close', async (code) => {
            if (code !== 0) {
                return res.status(500).json({ error: 'Python script failed.' });
            }

            const analysisResult = JSON.parse(output);
            const featureList = analysisResult.feature;
            const featureStatistics = analysisResult.statistics;

            // Questions for Groq API based on feature description
            const questions = [
                `What are the most important features among '${featureList}' these in the dataset and why?`,
                `Provide insights in these feature statistics '${JSON.stringify(featureStatistics)}'.`,
                `What are the common characteristics observed in the features '${featureList}'?`
            ];

            try {
                const groqResponses = [];
                
                for (const question of questions) {
                    const response = await fetch('https://api.groq.com/openai/v1/chat/completions', {
                        method: 'POST',
                        headers: {
                            'Authorization': `Bearer ${process.env.GROQ_API_KEY}`,
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            model: "llama3-8b-8192",
                            messages: [{ role: "user", content: question }],
                            max_tokens: 150,
                        }),
                    });
                    const data = await response.json();
                    groqResponses.push(data.choices[0].message.content);
                }

                // Respond with analysis results and Groq insights
                res.json({
                    analysis: analysisResult,
                    insights: groqResponses,
                });
            } catch (error) {
                console.error('Groq API error:', error);
                res.status(500).json({ error: 'Failed to fetch insights from Groq API.' });
            }
        });
    } catch (error) {
        console.error('Error processing data:', error);
        res.status(500).json({ error: 'Server error during data processing.' });
    }
};
