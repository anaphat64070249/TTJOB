const pool = require("../config")
const express = require('express');
const router = express.Router();

router.post("/addreview", async (req,res,next) => {

    const conn = await pool.getConnection()
    conn.beginTransaction()

    const id = req.body.id;
    const reviewer = req.body.reviewer;
    const score = req.body.score;
    const comm = req.body.comment;
    const report = req.body.report;
    const work_id = req.body.work_id;

    try{
        // const [row1] = await pool.query("ALTER TABLE Reviews DROP CONSTRAINT reviews_ibfk_1")

        // const [row2] = await pool.query("ALTER TABLE Reviews DROP CONSTRAINT reviews_ibfk_2")

        // const [row] = await pool.query("ALTER TABLE Reviews DROP primary key")
        
        const [row4,fields] = await conn.query("insert into Reviews(emp_id,job_id,reviewer_name,score,comments,report,reviewer) values (?,?,?,?,?,?,'com')",[id,work_id,reviewer,score,comm,report])
        const [row] = await conn.query("select count(emp_id) as a,sum(score) as s from Reviews where emp_id = ?",[id])
        const avg1 = Number(row[0].a)
        const avg2 = Number(row[0].s)+Number(score)
        
        const avg = Number(avg2/avg1)

        const [neww] = await conn.query("select experience_hour from Personal_infomations where emp_id=?",[id])
        const [newwww] = await conn.query("select working_hours from Jobs where job_id = ?",[work_id])
        console.log(newwww);
        console.log(neww);
        const aaaa = Number(neww[0].experience_hour)+Number(newwww[0].working_hours)
        console.log(aaaa);
        const [update] = await conn.query("update Personal_infomations set avg_score = round(?,2),experience_hour = ? where emp_id =?",[avg,aaaa,id])



        
        conn.commit()
    }
    catch(err){
        conn.rollback()
        console.log(err);
    }finally{
        conn.release()
    }

})

router.post("/peopleName", async (req,res,next) => {


    const id = req.body.id; 
    try{

        const [row,fields] = await pool.query("select * from Personal_infomations where personal_infoID = ?",[id])
        res.json({name:row[0]})
    }

    catch(err){
        console.log(err);
    }

})


exports.router = router;