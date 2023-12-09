const pool = require("../config")
const express = require('express');
const router = express.Router();

router.post("/detailList", async (req,res,next) => {
    const id = req.body.id;
    console.log(id);
    try{
        const [row,fields] = await pool.query("select *,date_format(date_of_birth, '%d-%m-%Y') as date_of_birth from Personal_infomations join Employee using (emp_id) join Emp_address using (emp_id) where personal_infoID = ?",[id])
        // console.log(row);
        res.json({list:row[0]})
    }
    catch(err){
        console.log(err);
    }


    



})


exports.router = router;