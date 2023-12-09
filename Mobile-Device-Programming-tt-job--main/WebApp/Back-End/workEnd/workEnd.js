const pool = require("../config")
const express = require('express');
const router = express.Router();

router.post("/workend", async (req,res,next) => {

    const id = req.body.id;
   try{
    const [row,field] = await pool.query("select *,DATE_FORMAT(day_start,'%d-%m-%Y') as day_start from Jobs join Company_infomations using (com_id)  where com_id = ? and status = 0",[id]);
    console.log(row);
    res.json({data:row})
   }
   catch(err){
    console.log(err);
   }


})


exports.router = router;