const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
app.use(bodyParser.json());
app.use(cors());

const mongoPort = '55000';
const mongoURL = 'mongodb://localhost:${mongoPort}/prof-ai-local-database'

// MongoDB connection
mongoose.connect(mongoUrl, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  }).then(() => {
    console.log('Connected to MongoDB');
  }).catch(err => {
    console.error('Failed to connect to MongoDB', err);
  });

// User schema
const UserSchema = new mongoose.Schema({
  email: String,
  password: String,
  school: String,
  grade: String,
  major: String,
});

const User = mongoose.model('User', UserSchema);

// API endpoint to register user
app.post('/api/register', async (req, res) => {
  const { email, password, school, grade, major } = req.body;
  const user = new User({ email, password, school, grade, major });
  await user.save();
  res.send({ message: 'User registered successfully' });
});

app.listen(5000, () => {
  console.log('Server is running on port 5000');
});
