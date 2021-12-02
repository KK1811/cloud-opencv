import cv2
import numpy as np
import boto3
import base64
import imutils

cap = cv2.VideoCapture(0)

currentFrame = 0

entries = []

sum_entry = 0

client = boto3.client('sqs')

while(True):
    ret, frame = cap.read()

    # frame = imutils.resize(frame, width=520, height=420)

    frame = cv2.flip(frame,1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if currentFrame:
        cv2.imshow('Video Stream', gray)
        if cv2.waitKey(1) == ord('q'):
            break
 
    retval, buffer = cv2.imencode('.jpg', frame)

    jpg_as_text = base64.b64encode(buffer).decode()

    if len(jpg_as_text) > 127000:
        continue

    print("frame size - ", len(jpg_as_text))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    entries.append(
        {
                    'Id': str(currentFrame),
                    'MessageBody': jpg_as_text,
                    'MessageDeduplicationId': str(currentFrame),
                    'MessageGroupId': 'frames'
                }  
    )

    if len(entries) > 1:

        # for entry in entries:
        #     sum_entry += len(str(i))

        # print("sum entry = ", sum_entry)

        # if sum_entry > 256000:
        #     entries.pop(2)

        response = client.send_message_batch(
            QueueUrl='https://sqs.us-west-2.amazonaws.com/720650668093/frame-queue.fifo',
            Entries = entries
        )

        print(response)

        entries = []

        sum_entry = 0

    currentFrame += 1

cap.release()
cv2.destroyAllWindows()


