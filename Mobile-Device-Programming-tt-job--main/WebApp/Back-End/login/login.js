const pool = require("../config")
const express = require('express');
const router = express.Router();

router.post("/test", async (req,res,next) => {

    const email = req.body.email;
    const pass = req.body.pass;
    console.log(email+pass);
    try{

        const [row,field] = await pool.query("Select * from Company where email = ? and password = ? and user_status = 1",[email,pass]);
        console.log(row.length);
        if (row.length != 0){
        res.json({check:"1",row:row[0]})
        console.log("1");
        }
        else if (row.length == 0){
            res.json({check:"0"})
            console.log("0");
        }
    }catch(err){
        console.log(err);
        console.log("err");
    }


})


exports.router = router;