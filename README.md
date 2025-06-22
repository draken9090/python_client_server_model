a simple client server module using python and created with sqlite as db and edited with help of curl 
curl -X POST http://localhost:8000/add_record \
     -H "Content-Type: application/json" \
     -d '{"roll_number":1,"name":"Alice"}' as example
