const pool = require("../config")
const express = require('express');
const router = express.Router();

router.post("/peend", async (req,res,next) => {


    const id = req.body.id;

    try{
        const [row,fields] = await pool.query("select * from Job_registor join Personal_infomations using (emp_id) where job_id = ?",[id])
        
        console.log(row);
        res.json({people:row})
    }

    catch(err){
        console.log(err);
    }
})


exports.router = router;