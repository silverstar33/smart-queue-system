import redis

redis_client = redis.Redis(host="localhost", port=6379, db=0)

for key in redis_client.scan_iter("task:*"):
    data = redis_client.hgetall(key)
    print(f"\nKey: {key}")
    for k, v in data.items():
        print(f"  {k.decode()}: {v.decode()}")
