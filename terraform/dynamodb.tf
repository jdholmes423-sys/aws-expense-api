resource "aws_dynamodb_table" "expenses" {
  name           = "Expenses"
  billing_mode   = "PAY_PER_REQUEST"
  
  hash_key       = "expense_id"
  
  attribute {
    name = "expense_id"
    type = "S"
  }
}