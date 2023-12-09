const pool = require("../config")
const express = require('express');
const router = express.Router();

router.post("/profile", async (req,res,next) => {

    const id = req.body.id;
    console.log(id);
    try{
       const [row,field] = await pool.query("select * from Company_infomations join Company using(com_id) join Com_address using (com_id) where com_id = ?",[id]);
       res.json({profile:row[0]})
    }catch(err){
        console.log(err);
    }
    



})


exports.router = router;