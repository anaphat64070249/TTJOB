const pool = require("../config")
const express = require('express');
const router = express.Router();

router.post("/con", async (req,res,next) => {
    const id = req.body.id
    const check = req.body.check

    try{
        if (check == '3'){
            const [row] = await pool.query("update Employee set user_status = 1 where emp_id = ?",[id] )
        }
        else if (check == "4"){
            const [row] = await pool.query("update Company set user_status = 1 where com_id = ?",[id] )
        }

    }catch(err){
        console.log(err);
    }
  
})

router.post

exports.router = router;