# Grab a fresh copy of the image and install dependencies
FROM public.ecr.aws/lambda/python:3.8

# Copy the application files into the image
COPY app/   ./
CMD ["lambda_function.lambda_handler"]