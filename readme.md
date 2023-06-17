## Datacredito Experian WSDL
Get all your reports in Datacredito by soap service.

## Installation

1. Clone the project and create a .env file with the env vars according to the .env.example file

2. In order to create a container, on the root folder run:

```
$ docker-compose up -d
```

3. the api will run in [http://127.0.0.1:5000/api/status](http://127.0.0.1:5000/api/status)

4. can access the container by running:

```
$ docker exec -it soapIntegration /bin/bash
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
