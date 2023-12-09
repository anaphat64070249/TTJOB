const pool = require("../config")
const express = require('express');
const router = express.Router();

router.post("/applicans", async (req,res,next) => {

    const id = req.body.work_id;
    try{

        const [row,fields] = await pool.query("select * from Personal_infomations join Job_registor using (emp_id) where job_id = ?",[id])
        // console.log(row);
        const [row1,field1] = await pool.query("select *,DATE_FORMAT(day_start,'%d-%m-%Y') as day_start from Jobs join Company_infomations using (com_id) where job_id = ?",[id]);
        res.json({appli:row,work:row1})

    }catch(err){
        console.log(err);
    }
})


router.put("/confirm", async (req,res,next) => {

    const conn = await pool.getConnection();
    conn.beginTransaction()
    const emp_id = req.body.a;
    const job_id  =req.body.b;
    console.log(emp_id,job_id);
    try{
        const [row,field] = await conn.query("update Job_registor set com_confirm = 1,date_com_confirm = CURRENT_TIMESTAMP where emp_id =? and job_id = ?",[emp_id,job_id] )
        const [row1,fields1] = await conn.query("insert into Message(emp_id,message_daySend,job_id) values(?,CURRENT_TIMESTAMP,?)", [emp_id,job_id])
        console.log(row);
        conn.commit()
    }catch(err){
        conn.rollback()
        console.log(err);
    }finally{
        conn.release()
    }
})

router.put("/cancel", async (req,res,next) => {

    const conn = await pool.getConnection();
    conn.beginTransaction()
    const emp_id = req.body.a;
    const job_id  =req.body.b;
    try{
        const [row,field] = await conn.query("update Job_registor set cancel_status = 1 where emp_id =? and job_id = ?",[emp_id,job_id] )
        const [row1,fields1] = await conn.query("insert into Message(emp_id,message_daySend,job_id) values(?,CURRENT_TIMESTAMP,? )", [emp_id,job_id])
        conn.commit()
    }catch(err){
        conn.rollback()
        console.log(err);
    }finally{
        conn.release()
    }
})

router.put("/end", async (req,res,nect)  => {
    const conn = await pool.getConnection()
    conn.beginTransaction()

    const id = req.body.work;
    console.log(id);
    try{
        const [row,fields] = await conn.query("update Jobs set status = 0 where job_id = ?" ,[id])
        const [ee] = await conn.query("update Emp_job_history set job_status = 0 where job_id = ?",[id])
        const [row2] = await conn.query('select emp_id from Job_registor where job_id=? and com_confirm = 1',[id])
        const [row3] = await conn.query('select working_hours from Jobs where job_id=?',[id])


        const id2 = row2[0].emp_id
        const hours = row3[0].working_hours
        console.log(id2);

        const [hours_have] = await conn.query("select experience_hour from Personal_infomations where emp_id = ?", id2)

        const sum = Number(hours_have[0].experience_hour)+Number(hours)

        const [updat] = await conn.query("update Personal_infomations set experience_hour = ? where emp_id = ? ",[sum,id2])

        conn.commit()
    }   
    catch(err){
        console.log(err);
        conn.rollback()
    }finally{
        conn.release()
    }
})



router.put("/doing", async (req,res,next) => {
    const id = req.body.id
    const j_id = req.body.job
    try{
        const [row] = await pool.query("update Job_registor set job_doing = 1 where job_id = ? and emp_id = ?",[j_id,id])
    }
    catch(err){
        console.log(err);
    }
    
})


exports.router = router;