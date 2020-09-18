# s3-poc
Simple integration with AWS S3
```
Implementation ONE
1. Producer generates some files randomly and uploads to S3
2. Producer calls the consumer's API to inform the Consumer that a file needs to be processed
3. Consumer gets the file from S3, processes it and uploads it back to S3
4. Consumer calls the producer's API to inform the Producer that file processing is complete
5. Producer displays the contents of the zip folder
```
```
Implementation TWO
1. Producer generates some file randomly and uploads to S3
2. Producer publishes the file metadata on a message queue
3. Consumer gets the file metadata from the message queue, queries S3 for it and processes it
4. Consumer publishes the processed file metadata on the message queue
5. Producer gets the file from the message queue and displays its contents
```