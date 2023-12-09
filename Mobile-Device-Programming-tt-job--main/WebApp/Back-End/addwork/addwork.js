const pool = require("../config");
const express = require("express");
const router = express.Router();

router.post("/addwork", async (req, res, next) => {
    const id = req.body.id;
    const position = req.body.position;
    const apply_type = req.body.apply_type;
    const pay = req.body.pay;
    const hours = req.body.hours;
    const date_start = req.body.date_start;
    const date_end = req.body.date_end;
    const time_start = req.body.time_start;
    const time_end = req.body.time_end;
    const amount = req.body.amount;
    const contact = req.body.contact;
    const boundary = req.body.boundary;
    const detail = req.body.detail;
    const name = req.body.name;
    


    try {

        const [row, fields] = await pool.query(
            "insert into Jobs(com_id,position,job_scope,job_infomation,job_date_declear,day_start,day_end,time_start,time_end,working_hours,day_work,pay,status,emp_amount,apply_type,manager_name) values (?,?,?,?,CURRENT_TIMESTAMP,?,?,?,?,?,DATEDIFF(?,?),?,1,?,?,?)",
            [
                id,position,boundary,detail,date_start,date_end,time_start,time_end,hours,date_end,date_start,pay,amount,apply_type,name
            ]
        );


    } catch (err) {
        console.log(err);
    }
});

exports.router = router;
