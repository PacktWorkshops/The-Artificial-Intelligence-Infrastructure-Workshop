// Selecting and using database
show dbs
use fashionmart

// Creating colleciton Products
db.createCollection(“products”);

// Inserting a product document

todayDate=new Date()

products={
"p_name": "Z-1 Running shoe",
"p_manufacturer": "Z-1",
"p_buy_price": 34,
"p_created_at": todayDate,
"sales": [
  {
    "s_sale_price": 40,
    "s_profit": 6,
    "p_created_at": todayDate,
  },
  {
    "s_sale_price": 41,
    "s_profit": 7,
    "p_created_at": todayDate
   }
  ]
};

db.products.insert(products);

// Aggregation pipeline

total_sales_for_product_pipeline=[
  {
    "$match": {
      "p_name": "Z-1 Running shoe"
    }
  },
  {
    "$project": {
      "product":"$p_name",
      "total_sales": {
        "$size": "$sales"
      }
    }
  }
];

db.products.aggregate(total_sales_for_product_pipeline).pretty()

// Creating a reusable function for building aggregation pipeline

// 1. How many units of “Z-1 running shoe” are sold in this year?

function total_product_sales(match_product,
  projection_field,
  count_field) {
  var matchObject = {};
  var countObject = {};
  matchObject[projection_field] = match_product;
  countObject["$size"] = "$"+count_field;
  return [
  {
    "$match": matchObject
  },
  {
    "$project": {
      "product":"$"+projection_field,

      "total_sales": countObject
  }
 }
]
};

db.products.aggregate(total_product_sales("Z-1 Running shoe","p_name","sales")).pretty();

// 2.  How many products are there?

db.products.count();


// 3. How many products with profit greater than 6?


function gt_product_sales(gt_value, compare_field) {
      var gt_object = {};
      var match_object = {};
      gt_object["$gt"] = gt_value
      match_object[compare_field] = gt_object

  return [
      {
        "$unwind":"$sales"
      },
      {
        "$match": match_object
      },
      {
        "$project": {
           "product":"$p_name",
           "sales":"$sales"
         }
      }
     ]
 };

 db.products.aggregate(gt_product_sales(6, "sales.s_profit"));
