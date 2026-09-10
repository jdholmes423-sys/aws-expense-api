resource "aws_iam_role" "lambda_execution_role" {
        name = "track-expenses-lambda-role"
        assume_role_policy = jsonencode({
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
    )
}


resource "aws_iam_policy" "lambda_policy" {
    name = "track-expenses-lambda-policy"

    policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
      {
        Action = [
          "dynamodb:PutItem",
          "dynamodb:Scan",
          "dynamodb:GetItem",
          "dynamodb:DeleteItem"
        ]
        Effect = "Allow"
        Resource = aws_dynamodb_table.expenses.arn
      },
      
    ]
  })
}


resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
     role =  aws_iam_role.lambda_execution_role.name
     policy_arn = aws_iam_policy.lambda_policy.arn
}