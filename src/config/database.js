require('dotenv').config();
const { MongoClient } = require('mongodb');

const uri = process.env.MONGODB_URI;

const connection = new MongoClient(uri);

async function connectToDatabase() {
    await connection.connect();
    console.log('Connected to the database');
    return connection.db(process.env.DB_NAME);
  }
module.exports = connectToDatabase;
