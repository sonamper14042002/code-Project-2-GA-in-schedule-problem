require('dotenv').config();
const express = require('express');
const web = express();
const port = process.env.PORT;
const hostname = process.env.HOSTNAME;
const config_view_function = require('./config/viewengine');
const webroutes = require('./routes/web');
const connectToDatabase = require('./config/database');
const bodyParser = require('body-parser');

web.use(express.json());
web.use(express.urlencoded({ extended: true }));


web.use(bodyParser.urlencoded({ extended: true }));
web.use(bodyParser.json());
async function startServer() {
  try {
    // Connect to MongoDB
    const db = await connectToDatabase();

    // Set up view engine
    config_view_function(web);

    // Set up routes
    web.use(webroutes);

    // Start server
    web.listen(port, hostname, () => {
      console.log('Server is running at', port);
    });
  } catch (error) {
    console.error('Error starting server:', error);
    process.exit(1); // Exit process with error code
  }
}

startServer();
