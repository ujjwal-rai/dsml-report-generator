const express = require('express');
const router = express.Router();
const multer = require('multer');
const dataController = require('./controllers/dataController');

// Configure multer for file upload
const upload = multer({
  dest: 'uploads/', 
});

router.post('/upload', upload.fields([{ name: 'dataset' }, { name: 'featureDesc' }]), dataController.processData);

module.exports = router;
