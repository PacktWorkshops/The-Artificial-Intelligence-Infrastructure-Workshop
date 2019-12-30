use fashionmart

todayDate=new Date()

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

db.products.insert(products);

db.products.find().pretty();

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

user_logs=[
  {
    user_id:ObjectId("5e038e15211649ccef9a742d"),
    product_id:ObjectId("5e037d5c211649ccef9a7429"),
    action:"bought",
    ul_crated_at:todayDate
  },
  {
    user_id:ObjectId("5e038e15211649ccef9a742d"),
    product_id:ObjectId("5e037d4b211649ccef9a7428"),
    action:"bought",
    ul_crated_at:todayDate

  },
  {
    user_id:ObjectId("5e038e15211649ccef9a742e"),
    product_id:ObjectId("5e037d5c211649ccef9a7429"),
    action:"bought",
    ul_crated_at:todayDate

  }
];

db.users.insert(users);
db.user_logs.insert(user_logs);

var user_logs_aggregate_pipeline = [
    { $lookup:
        {
           from: "users",
           localField: "user_id",
           foreignField: "_id",
           as: "users"
        }
    },
    {
      $lookup:
        {
           from: "products",
           localField: "product_id",
           foreignField: "_id",
           as: "products"
        }
    },
    {
        "$unwind":"$users"
    },
    {
        "$unwind":"$products"
    },
    {
        "$project": {
           "user":"$users.name",
           "product":"$products.p_name",
           "action":"$action"

         }
      }
];
db.user_logs.aggregate(user_logs_aggregate_pipeline).pretty()







