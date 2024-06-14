const connectToDatabase = require('../config/database');
// Trong file services/CRUDservice.js
const { spawn } = require('child_process');

async function getAllTeachers() {
  const db = await connectToDatabase();
  const collections = await db.listCollections().toArray();
  const teachersCollections = collections.filter(collection => collection.name.endsWith('_major'));
  const teachers = [];
  for (const collection of teachersCollections) {
    const teachersInMajor = await db.collection(collection.name).find({}).toArray();
    teachers.push(...teachersInMajor);
  }
  return teachers;
}
async function getAllClasses() {
  const db = await connectToDatabase();
  const collections = await db.listCollections().toArray();
  const classesCollections = collections.filter(collection => collection.name.endsWith('_class'));
  const classes = [];
  for (const collection of classesCollections) {
    const classesInMajor = await db.collection(collection.name).find({}).toArray();
    classes.push(...classesInMajor);
  }
  return classes;
}
async function getAllCollections() {
    const db = await connectToDatabase();
    const collections = await db.listCollections().toArray();
    const collectionsWithData = [];
    for (const collection of collections) {
        const data = await db.collection(collection.name).find({}).toArray();
        collectionsWithData.push({ name: collection.name, documents: data });
    }
    return collectionsWithData;
}

async function createCollection(name) {
    const nameT = name + "_major";
    const db = await connectToDatabase();
    await db.createCollection(nameT);
}

async function insertDocuments(collectionName, documents) {
    const db = await connectToDatabase();
    const collection = db.collection(collectionName + "_major");
    await collection.insertMany(documents);
}
async function addTeacherAndSubjects(teacherName, subjects) {
    await createCollection(teacherName);
    const subjectDocuments = subjects.toString().split(",").map(subject => ({ name: subject.trim() }));
    await insertDocuments(teacherName, subjectDocuments);
    console.log('Teacher Name:', teacherName);
    console.log('Subject Documents:', subjectDocuments);
}
async function runPythonScript() {
    return new Promise((resolve, reject) => {
        const pythonProcess = spawn('python', ["E:\\WEB-GENETIC\\GENETIC ALGORITHM\\result.py"], {
            env: { ...process.env, PYTHONIOENCODING: 'utf-8' },
          });
        let scriptOutput = '';
        let scriptError = '';

        pythonProcess.stdout.on('data', (data) => {
            scriptOutput += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            scriptError += data.toString();
        });

        pythonProcess.on('error', (error) => {
            reject(`Không thể khởi động script Python: ${error}`);
        });

        pythonProcess.on('close', (code) => {
            if (code === 0) {
                resolve(scriptOutput);
            } else {
                reject(`Script Python kết thúc với mã lỗi ${code}: ${scriptError}`);
            }
        });
    });
}
module.exports = {
  getAllTeachers,addTeacherAndSubjects,getAllCollections,runPythonScript
};


