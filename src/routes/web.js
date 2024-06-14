const express = require('express');
const { getHomepage,GetCreatePage,createUser,GetUpdatePage,GetCreateSchedule,GenerateSchedule } = require('../controllers/homeController');
const router = express.Router();
router.get('/',getHomepage);

router.get('/create',GetCreatePage);
router.post('/create-user',createUser);

router.get('/update-subject/:id',GetUpdatePage);
// router.post('/update_user',UpdateUser);

// router.post('/getdelete/:id',Getdetelepage);
// router.post('/Delete_user/:id',Delete_user);

router.get('/createschedule/',GetCreateSchedule);
router.post('/generate-schedule',GenerateSchedule);




module.exports = router