const pool = require("../config")
const express = require('express');
const router = express.Router();

router.post("/review", async (req,res,next) => {

   
        const id = req.body.id;
        const com_id = req.body.com_id;
        try{
            const [row,fields] = await pool.query("select * from Reviews join Personal_infomations using (emp_id) where emp_id = ?",[id])


            const [row2,fields2] = await pool.query("select * from Company_infomations where com_id = ?",[com_id])

            

            const [row3,fields3] = await pool.query("select * from Jobs join Reviews using (job_id) join Company_infomations using (com_id) join (Emp_job_history) using (job_id) where Reviews.emp_id = ?",
            [id])
            console.log(row3);
            res.json({re:row,com_name:row2[0],review:row3})
        }
        catch(err){
            console.log(err);
        }



})


exports.router = router;