### potential PoC
- make a master-control-A, master-control-B, rest-A, rest-B, S3
- master-control-A and B are simple python scripts.
- master control-A could have N tasks written on its processing Q where it has to write a data zip on S3 and call rest-B
- master-control-A would start processing its Q
- master-control-A would write a data zip to S3 and then call a API on rest-B to inform about the data location, it could be added to a processing Q for master-control-B.
- master-control-B could pick up items from the Q where the location of the data in S3 storage is mentioned, 'process' it (example, randomly remove the data files by half) andf store it back in S3 (in a different location). Then it could call a API on rest-A to inform it of its location. In turn it could be added to a processing Q for master-control-A.
- If need be, master-control-A could alternate between adding data on S3 for B or processing data sent back by B (just display the contents of the zip folder)