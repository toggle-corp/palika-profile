
# Palika Profile Report Generation

### Requirements

- Cairo: https://pycairo.readthedocs.io/en/latest/getting_started.html

- PyG: https://pygobject.readthedocs.io/en/latest/getting_started.html

- libffi: https://sourceware.org/libffi/

- drafter: https://github.com/bibekdahal/drafter

- maps: https://github.com/eoglethorpe/hrrp-maps


### Docker [Development]
```
docker-compose pull # pull images (you can use this instead of build)
docker-compose build # build images
docker-compose up # start the containers
```

#### Develop with local drafter and hrrp-maps code
- create new `docker-compose-custom.yml` using `docker-compose.yml`
- update `server` **volumes** entry with **drafter** or **hrrp-maps** code path
```
        volumes:
            - ./:/code
            - ..path_to_drafter/:/dep/drafter
            - ..path_to_hrrp-maps:/dep/hrrp-maps
```
- and start the server
```
docker-compose -f docker-compose-custom.yml up
```

### Docker [Production]
```
docker-compose -f production.yml up -d # start containers in daemon mode
docker-compose -f production.yml logs -f # follow logs
docker-compose -f production.yml stop # stop containers
docker-compose -f production.yml down # stop and delete containers
```
