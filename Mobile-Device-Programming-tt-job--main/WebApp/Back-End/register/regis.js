const path = require("path");
const pool = require("../config")
const express = require('express');
const router = express.Router();
const multer = require("multer");


var admin = require("firebase-admin");
var serviceAccount = require("./mobile-image-com-firebase-adminsdk-1c6sa-d34470338f.json");


const firebase = admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    storageBucket: "gs://mobile-image-com.appspot.com"
  });

  const auth = firebase.auth();
  

var bucket = firebase.storage().bucket();


// SET STORAGE
var storage = multer.diskStorage({
  destination: function (req, file, callback) {
    callback(null, "./static/uploads");
  },
  filename: function (req, file, callback) {
    callback(
      null,
      file.fieldname + "-" + Date.now() + path.extname(file.originalname)
    );
  },
});
const upload = multer({ storage: storage });


router.post("/register3",upload.array("myImage",5), async (req,res,next) => {
  const conn = await pool.getConnection();
  conn.beginTransaction();
  // console.log(req.files[0]);
  // console.log(req.files[1]);
  // console.log(req.body.email);

  //login
  const email = req.body.email;
  const phone = req.body.tel;
  const pass = req.body.pass;

  // address
  const district = req.body.amphur
  const tumbon = req.body.tambon
  const province = req.body.province
  const zipcode = req.body.code
  const address = req.body.address


  //information
  const name = req.body.name
  const juristic_id = req.body.num
  const bussines_type = req.body.type
  const descriptions = req.body.about

  try{
        // img 1
        bucket.upload(req.files[0].path)
        const file = req.files[0].filename;
        const options = {
            version: 'v2',
            action: 'read',
            expires: Date.now() + 1000 * 60 * 60
        }

        const [Url] = await bucket.file(file).getSignedUrl(options);

        // img 2
        bucket.upload(req.files[1].path)
        const file2 = req.files[1].filename;
        const options2 = {
            version: 'v2',
            action: 'read',
            expires: Date.now() + 1000 * 60 * 60
        }
 
        const [Url2] = await bucket.file(file2).getSignedUrl(options2);
        

    //login
    const [row] = await conn.query("insert into Company(email,phone,user_status,password) values(?,?,0,?)", [email,phone,pass])
    const id = row.insertId;

    //address
    const [row2] = await conn.query("insert into Com_address(com_id,district,tumbon,province,zipCode,address) values(?,?,?,?,?,?)",[id,district,tumbon,province,zipcode,address])
    const id2 = row2.insertId
   
    //information
    const [row3] = await conn.query("insert into Company_infomations(com_id,companyName,juristic_id,image_juristic,bussines_type,address_code,descriptions,image_company,avg_score) values(?,?,?,?,?,?,?,?,0)",[id,name,juristic_id,Url,bussines_type,id2,descriptions,Url2])
    res.json({data:id})
    await conn.commit();
  }
  catch(err){
    await conn.rollback();
    console.log(err);
  }finally{
    conn.release();
  }
})

// router.post("/register",upload.array("myImage",5),async (req,res,next) => {

//   const conn = await pool.getConnection();
//   conn.beginTransaction();
//   const id = req.body.id.data;
//      try{
//       console.log(id);
        // bucket.upload(req.files[0].path)
        // const file = req.files[0].filename;
        // const options = {
        //     version: 'v2',
        //     action: 'read',
        //     expires: Date.now() + 1000 * 60 * 60
        // }

        // const [Url] = await bucket.file(file).getSignedUrl(options);
        
//         // const [max] = await conn.query("select max(com_id) as max from Company")
//         // const max_x = max[0].max+1;

//         const [row] = await conn.query("update Company_infomations set image_juristic = ? where com_id = ? ",[Url,id] )
        
        
//       await conn.commit();

//      }
//      catch(err){
//         await conn.rollback();
//      }finally{
//       await conn.release();
//      }
// })



// router.post("/register2",upload.array("myImage2",5),async (req,res,next) => {
//   const conn = await pool.getConnection();
//   conn.beginTransaction();
//   const id = req.body.id.data;
//     try{
//       console.log(id);
      //  bucket.upload(req.files[0].path)
      //  const file = req.files[0].filename;
      //  const options = {
      //      version: 'v2',
      //      action: 'read',
      //      expires: Date.now() + 1000 * 60 * 60
      //  }

      //  const [Url] = await bucket.file(file).getSignedUrl(options);


//       //  const [max] = await conn.query("select max(com_id) as max from Company")
//       //  const max_x = max[0].max+1;
      
//        const [row] = await conn.query("update Company_infomations set image_company = ? where com_id = ? ",[Url,id] )

//       await conn.commit();
//     }
//     catch(err){
//       await conn.rollback();
//     }finally{
//       await conn.release()
//     }
   

// })



exports.router = router;