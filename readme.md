# MasterWang-SensorDataCollection

This repo provide a data collection server for Master Wang Project. Server is based on Flask and MongoDB. We use docker-compose to package all functions together. 


## Quick tart

### Lunch the server

Start the server running on localhost:8081. To change the port, you can modify [docker-compose.yml](./docker-compose.yml)

```
docker-compose up --build
```

**To make sure MasterWang ios app can access this server, you can connect the sever and an iPhone in a same local network. Or you can run Cloudflard Tunnel with a public domain for this server.**


### Export data into csv files

```
pip install -r requirements.txt
python export
```

Then you can find collected data in [data](./data/)



### How to stop the server
```
docker-compose down
```

