#--Create database
use fashionmart

#-Set variable for current date
todayDate=new Date()

#--Create Products
products=[{
"p_name": "XIMO Trek shirt",
"p_manufacturer": "XIMO",
"p_buy_price": 15,
"p_created_at": todayDate,
"sales": [
  {
    "s_sale_price": 30,
    "s_profit": 15,
    "p_created_at": todayDate,
  },
  {
    "s_sale_price": 18,
    "s_profit": 3,
    "p_created_at": todayDate
   },
  {
    "s_sale_price": 20,
    "s_profit": 5,
    "p_created_at": todayDate
   },
  {
    "s_sale_price": 15,
    "s_profit": 0,
    "p_created_at": todayDate
   }
  ]
},
{
"p_name": "XIMO Trek shorts",
"p_manufacturer": "XIMO",
"p_buy_price": 18,
"p_created_at": todayDate,
"sales": [
  {
    "s_sale_price": 22,
    "s_profit": 4,
    "p_created_at": todayDate,
  },
  {
    "s_sale_price": 18,
    "s_profit": 0,
    "p_created_at": todayDate
   },
  {
    "s_sale_price": 20,
    "s_profit": 2,
    "p_created_at": todayDate
   }
  ]
},
{
"p_name": "NY cap",
"p_manufacturer": "NY",
"p_buy_price": 18,
"p_created_at": todayDate,
"sales": [
  {
    "s_sale_price": 20,
    "s_profit": 2,
    "p_created_at": todayDate,
  },
  {
    "s_sale_price": 21,
    "s_profit": 3,
    "p_created_at": todayDate
   },
  {
    "s_sale_price": 19,
    "s_profit": 1,
    "p_created_at": todayDate
   }
  ]
}
]

#---Insert data
db.products.insert(products);

db.products.find().pretty();

#---Create Users
users=[
  {
    "name":"Max",
    "u_created_at":todayDate
  },
  {
    "name":"John Doe",
    "u_created_at":todayDate
  },
  {
    "name":"Roger smith",
    "u_created_at":todayDate
  },
];

#--Create User Logs
user_logs=[
  {
    user_id:"Max",
    product_id:"XIMO Trek shirt",
    action:"bought",
    ul_crated_at:todayDate
  },
  {
    user_id:"John Doe",
    product_id:"NY cap",
    action:"bought",
    ul_crated_at:todayDate

  },
  {
    user_id:"Roger smith",
    product_id: "XIMO Trek shorts",
    action:"bought",
    ul_crated_at:todayDate

  }
];

#--Insert Users
db.users.insert(users);


#--Insert User Logs
db.user_logs.insert(user_logs);


#---Create Function for Join
var user_logs_aggregate_pipeline = [
    { $lookup:
        {
		   from: "users",
		   localField: "user_id",
		   foreignField: "name",
		   as: "users"
        }
    },
    {
      $lookup:
        {
           from: "products",
           localField: "product_id",
           foreignField: "p_name",
           as: "products"
        }
    },
    {
        "$unwind":"$users"
    },   
    {
        "$project": {
           "user":"$users.name",
           "product":"$products.p_name",
           "action":"$action"

         }
      }
];


#---Select the data
db.user_logs.aggregate(user_logs_aggregate_pipeline).pretty()