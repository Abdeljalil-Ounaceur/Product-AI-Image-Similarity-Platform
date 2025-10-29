# Product similarity platform
This plateform serves one main task at the moment: searching for products based on the image of the product itself, but deployed using modern microservice architecture

_currently the only way to make this app work is by installing minio and Oracle 23ai or 26ai locally and creating the tables and buckets by manually executing the script files (will dockerize everything soon for a more portabe experience)_

TODO:
- [x] Create the MVP of the app
- [ ] Create a Dockerfile for every microservice in the app
- [ ] Create a docker-compose.yaml to make the app portable anywhere