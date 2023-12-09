const pool = require("../config")
const express = require('express');
const router = express.Router();

router.post("/delete", async (req,res,next) => {

    const conn = await pool.getConnection()
    conn.beginTransaction()

    const id = req.body.id;
    const check = req.body.check;
    try{
        if (check == '1'){
            const [row] = await conn.query("update  Employee set user_status = 3  where emp_id=?",[id])
        }
        else if (check == '2'){
            const [row] = await conn.query("update  Company set user_status = 3 where com_id=?",[id])
        }
        conn.commit()
    }catch(err){
        console.log(err);
        conn.rollback()
    }finally{
        conn.release()
    }

})

router.post

exports.router = router;