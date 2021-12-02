import cv2
import boto3

client = boto3.client('sqs')

currentFrame = 0

while(True):

    response = client.receive_message(
        QueueUrl='string',
        ReceiveRequestAttemptId = str(currentFrame)
    )

    print(response)


    # start_point = (5, 5) 
    # end_point = (220, 220) 
    
    # color = (255, 0, 0) 

    # thickness = 2
    
    # frame = cv2.rectangle(image, start_point, end_point, color, thickness) 

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # if currentFrame:
    #     cv2.imshow('Video Stream', gray)
    #     if cv2.waitKey(1) == ord('q'):
    #         break

    currentFrame += 1