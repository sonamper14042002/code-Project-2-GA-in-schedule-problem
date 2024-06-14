const {  getAllCollections,addTeacherAndSubjects,runPythonScript } = require('../services/CRUDservice');

const getHomepage = async (req, res) => {
  // Lấy danh sách giáo viên, lớp học và collections từ cơ sở dữ liệu
  const collections = await getAllCollections();
  // Render trang chủ với danh sách giáo viên, lớp học và collections
  res.render('homepage.ejs', { Collections: collections });
};
const GetCreatePage =(req,res)=>{
    res.render('create.ejs')
}
const createUser = async (req, res) => {
    const { teacherName, subjects } = req.body; 
    await addTeacherAndSubjects(teacherName, subjects);
    res.redirect('/');
}

const GetUpdatePage =(req,res)=>{
    res.render('update.ejs');
}
const GetCreateSchedule = async (req, res) =>{
    return res.render('createschedule.ejs');  
}

const GenerateSchedule = async (req, res) => {
    const jsonResult = await runPythonScript();
    console.log(jsonResult);
    res.render('schedule-result.ejs', { result: jsonResult });
};


module.exports = {
  getHomepage,GetCreatePage,createUser,GetUpdatePage,GetCreateSchedule,GenerateSchedule
};


// const GetUpdatePage =async(req,res)=>{
//     const UserId = req.params.id;
//     let user = await GetUserbyId(UserId);
//     res.render('update.ejs',{UserEdit:user})
// }
// const UpdateUser = async(req,res)=>{
//     let UserId = req.body.id;
//     let email = req.body.email;
//     let name = req.body.name;
//     let city = req.body.city;
//     await UpdateUserSer(UserId,email,name,city);
//         res.redirect('/');
// };
// const Getdetelepage =async(req,res)=>{
//     const UserId = req.params.id;
//     let user = await GetUserbyId(UserId);
//     res.render('detele.ejs',{UserDetele:user})
// }
// const Delete_user =async(req,res)=>{
//     let UserId = req.body.id;
//     await GetdeteleUser(UserId);
//     res.redirect('/');
// };

