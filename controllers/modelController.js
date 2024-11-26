const { spawn } = require('child_process');
const path = require('path');

exports.trainModel = (req, res) => {
    const pythonProcess = spawn('python3', [path.join(__dirname, '../utils/model_training.py'), 'uploads/cleaned_data.csv']);

    pythonProcess.stdout.on('data', (data) => {
        const output = JSON.parse(data.toString());
        res.json({ message: 'Model training complete', results: output });
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Error: ${data}`);
        res.status(500).json({ error: 'Failed to train model' });
    });
};
