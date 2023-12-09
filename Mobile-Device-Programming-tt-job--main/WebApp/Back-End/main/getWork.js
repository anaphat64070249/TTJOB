const pool = require("../config")
const express = require('express');
const router = express.Router();

router.post("/main", async (req,res,next) => {

    const id = req.body.id;
    try{
       const [row,field] = await pool.query("select *,DATE_FORMAT(day_start,'%d-%m-%Y') as day_start from Jobs where com_id = ? and status=1",[id]);

       const [row2,field2] = await pool.query("select companyName,image_juristic from Company_infomations where com_id = ?",[id]);
       
       res.json({ork:row,name:row2[0]})
    }catch(err){
        console.log(err);
    }
    



})


exports.router = router;