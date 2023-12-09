const pool = require("../config")
const express = require('express');
const router = express.Router();

router.get("/dash", async (req,res,next) => {


    try{

        const [user_all] = await pool.query("select count(emp_id) as a from Employee where user_status = 1 or user_status = 0")
        const [com_all] = await pool.query("select count(com_id) as a from Company where user_status = 1 or user_status = 0")
        const [job_all] = await pool.query("select count(job_id) as a from Jobs")


        const [user_confirm] = await pool.query("select count(emp_id) as a from Employee where user_status = 1")
        const [com_confirm] = await pool.query("select count(com_id) as a from Company where user_status = 1")
        const [jobing] = await pool.query("select count(job_id) as a from Jobs where status = 1") 



        const [user_notconfirm] = await pool.query("select count(emp_id) as a from Employee where user_status = 0")
        const [com_notconfirm] = await pool.query("select count(com_id) as a from Company where user_status = 0")
        const [job_end] = await pool.query("select count(job_id) as a from Jobs where status = 0") 

        res.json({user_all:user_all[0],com_all:com_all[0],job_all:job_all[0],user_confirm:user_confirm[0],com_confirm:com_confirm[0],jobing:jobing[0],user_notconfirm:user_notconfirm[0],com_notconfirm:com_notconfirm[0],job_end:job_end[0]})


    }catch(err){
        console.log(err);

    }


})


exports.router = router;