const pool = require("../config")
const express = require('express');
const router = express.Router();

router.post("/gettable", async (req,res,next) => {

    const check = req.body.check;

    if (check == 1){
        //สมาชิกหางาน
        const [row,fields] = await pool.query("select * from Employee join Personal_infomations using(emp_id) where user_status = 1")
        res.json({dat:row})
    }
    else if(check == 2){
        // สมาชิกบริษัท
        const [row,fields] = await pool.query("select * from Company join Company_infomations using(com_id) where user_status = 1")
        res.json({dat:row})
    }
    else if (check == 3){
        //สมัครหางาน
        const [row,fields] = await pool.query("select * from Employee join Personal_infomations using(emp_id) where user_status = 0")
        res.json({dat:row})
    }
    else if (check == 4){
        //สมัครบริษัท
        const [row,fields] = await pool.query("select * from Company join Company_infomations using(com_id) where user_status = 0")
        res.json({dat:row})
    }
    



})


exports.router = router;