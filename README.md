# Plastic-Detection

## Description
During summer, beaches are filled with people, but also with plastic waste like chocolate wrappers, plastic bags, and bottles.
Even though the government has taken steps to reduce pollution, plastic waste is still a big problem.

Some beaches have robots to separate waste, but they cannot specifically identify and remove plastic.
To solve this, I built a machine learning model that can detect plastic objects in images.
I trained this model using Google Images and the Open Images Dataset V7 and created an end-to-end machine learning pipeline in AWS. 
The goal is to detect plastic waste and draw bounding boxes, helping robots and waste management systems separate plastic more effectively.

#### DataSet : [Plastic-Detection Dataset](https://storage.googleapis.com/openimages/web/visualizer/index.html?type=detection&set=train&c=%2Fm%2F05gqfk)

## Project Architecture

![6](https://github.com/user-attachments/assets/31420db6-32fc-4dca-8b3d-aedcd793216f)

## Tasks

- Step 1 : Created a Service: Used AWS SageMaker to build and implement the machine learning model for detecting plastic in images. SageMaker made it easier to develop and deploy the model.

- Step 2 : Data Cleaning: Cleaned the raw image data by removing unwanted or poor-quality images to make sure the model gets good quality data.

- Step 3 : Data Augmentation: Used techniques like rotating and flipping images along the y-axis to create more training data, helping the model perform better.

- Step 4 :Data Engineering: Changed the train/test images into RecordIO (.rec) files and stored them in an S3 Bucket for easy access during training.

- Step 5 : Model Training: Trained the model using ResNet-50, a strong deep learning model, and saved the best version in an S3 Bucket.

- Step 6 : Step Function Setup: Set up an AWS Step Function to automate and manage the training process.

- Step 7 : Lambda Function for Job Submission: Created a Lambda function to submit the training job and track its progress.

- Step 8 : Result Storage Lambda: Made another Lambda function to save the results (like detected plastic objects) in an S3 Bucket.

- Step 9 : Automated Scheduling: Used EventBridge to schedule and automatically run the pipeline at specific times.

- Step 10 : Bounding Box Drawing: After the process completes, a Python script draws bounding boxes around the plastic objects in the images.

### Model Training

-The process starts by converting images into RecordIO format using im2rec.py and uploading them to an S3 bucket. The training environment is set up on AWS SageMaker using a ml.p3.2xlarge instance, with data organized into train and validation folders in S3.
-For the model, ResNet-50 is used as a pre-trained CNN for object detection. Hyperparameters like epochs, learning rate, and weight decay are fine-tuned for better accuracy.
-To find the best configuration, Hyperparameter Tuning is performed, testing different learning rates, mini-batch sizes, and optimizer types. A total of 8 training jobs were run, and the model took around 8 hours to train.
-Finally, the model is trained using data from S3, and the results are saved back into the S3 bucket, ready for use.

### Deployment

- After successfully training the model, the next step was to deploy it for real-time predictions. The trained model, stored as a .tar.gz file in S3, needed to be accessed and deployed to an endpoint for inference.
- First, we created a SageMaker model by pointing to the S3 path where the trained model was stored. This model used the pre-built object detection container from SageMaker, which provides the necessary setup to run the model and make predictions.
- Next, we deployed the model to an endpoint by specifying the instance type and the number of instances. This deployment allowed us to interact with the model and get predictions in real-time.
- Once the model was deployed, we could send images to the endpoint for inference. The model would process the images and return predictions, such as detecting plastic objects in the images by drawing bounding boxes around them.
- In this way, the trained plastic detection model was successfully deployed, and real-time predictions became available for use in solving the problem of plastic waste detection.

### AWS Step Function

- Start
- Submit Job: It starts by submitting a job using a Lambda function, which returns a unique job ID (guid).
- Wait: It waits for 60 seconds to allow the job to run.
- Check Job Status: It checks if the job is "Completed" or "Failed".
If "Completed", it moves to the next step.
If "Failed", the process ends with a failure.
- Clean Output: If the job is completed, it cleans the output using a Lambda function, with retries in case of failure.
- Final Job Status: Finally, it checks the job status again and ends the process.
- Stop 
