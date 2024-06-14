const express = require('express');
const path = require('path');
const config_view_function = (web)=>{
    web.set('views',path.join('./src','views'));
    web.set('view engine','ejs');
    web.use(express.static(path.join('./src','public')));
}
module.exports = config_view_function;
