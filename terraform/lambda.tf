data "archive_file" "lambda_code" {
  type        = "zip"
  source_file = "${path.module}/../lambda/app.py"
  output_path = "${path.module}/../lambda/lambda.zip"
}

resource "aws_lambda_function" "lambda_expenses" {
  filename         = data.archive_file.lambda_code.output_path
  function_name    = "lambda-expense-tracker"
  role             = aws_iam_role.lambda_execution_role.arn
  handler          = "app.lambda_handler"
  source_code_hash = data.archive_file.lambda_code.output_base64sha256

  runtime = "python3.12"

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.expenses.name      
    }
  }
}

resource "aws_lambda_permission" "gateway_to_lambda" {
  statement_id  = "AllowAPIGatewayInvocation"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_expenses.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.expenses_api.execution_arn}/*/*"
}
