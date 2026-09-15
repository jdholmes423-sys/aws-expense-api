resource "aws_apigatewayv2_api" "expenses_api" {
  name          = "expense-tracking-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id           = aws_apigatewayv2_api.expenses_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.lambda_expenses.invoke_arn
  
}

resource "aws_apigatewayv2_route" "create_expense" {
  api_id    = aws_apigatewayv2_api.expenses_api.id
  route_key = "POST /expenses"
  target = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_route" "list_expenses" {
  api_id    = aws_apigatewayv2_api.expenses_api.id
  route_key = "GET /expenses"
  target = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_route" "get_expense" {
  api_id    = aws_apigatewayv2_api.expenses_api.id
  route_key = "GET /expenses/{id}"
  target = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_route" "delete_expense" {
  api_id    = aws_apigatewayv2_api.expenses_api.id
  route_key = "DELETE /expenses/{id}"
  target = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_stage" "api_stage" {
  api_id = aws_apigatewayv2_api.expenses_api.id
  name   = "$default"
  auto_deploy = true
}
