const pool = require("../config")
const express = require('express');
const router = express.Router();

router.post("/1", async (req,res,next) => {
    const conn =await pool.getConnection();
    conn.beginTransaction();

   try{
    const id = req.body.id
    const [row] = await conn.query("select * from Reviews where emp_id = ? and reviewer = 'com'", [id])
    const [row2] = await conn.query("select * from Personal_infomations where emp_id=?",[id])
    conn.commit()
    res.json({review:row,profile:row2[0]})
   }
   catch(err){
    console.log(err);
    conn.rollback()
   }finally{
    conn.release()
   }
})

router.post("/2", async (req,res,next) => {
    const conn = await pool.getConnection()
    conn.beginTransaction()

try{
    const id = req.body.id
    const [row] = await conn.query("select * from Reviews where emp_id = ? and reviewer = 'emp'", [id])
    const [row2] = await conn.query("select * from Company_infomations where com_id=?",[id])
    conn.commit()
    res.json({review:row,profile:row2[0]})
}
catch(err){
    console.log(err);
    conn.rollback()
}
finally{
    conn.release()
}
})

router.post("/3", async (req,res,next) => {
    const conn = await pool.getConnection();
    conn.beginTransaction()
    
    const id = req.body.id
    try{
        const [row2] = await conn.query("select *,date_format(date_of_birth, '%d-%M-%Y') as date_of_birth from Personal_infomations join Employee using(emp_id) join Emp_address using(emp_id) where emp_id=?",[id])


        conn.commit()
        res.json({profile:row2[0]})
    }catch(err){
        console.log(err);
        conn.rollback()
    }finally{
        conn.release()
    }

})

router.post("/4", async (req,res,next) => {
    const conn = await pool.getConnection();
    conn.beginTransaction()
    
    const id = req.body.id
    try{
        const [row2] = await conn.query("select * from Company_infomations join Company using(com_id) join Com_address using(com_id) where com_id=?",[id])
    
        conn.commit()
        res.json({profile:row2[0]})
    }catch(err){
        console.log(err);
        conn.rollback()
    }finally{
        conn.release()
    }
})


exports.router = router;