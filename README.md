# Pritunl API Client for Python 3

This is a simple API Client written in Python 3. 

You need to refer Pritunl [API Documentationl](https://docs.pritunl.com/docs/api) to get an idea of how to use this. This API client uses almost the same command as in the [API Handlers](https://github.com/pritunl/pritunl-web/tree/master/handlers).

## Installation

Install from our [PyPI Project Repository](https://pypi.org/project/pritunl-api/)

```bash
pip install pritunl-api
```

## API Usage

```python
import os
from pritunl_api import Pritunl

pritunl = Pritunl(
  url=os.environ.get('PRITUNL_BASE_URL'),
  token=os.environ.get('PRITUNL_API_TOKEN'),
  secret=os.environ.get('PRITUNL_API_SECRET')
)

# Your Pritunl API Client Object is now ready to use!
pritunl.<FEATURE>.<METHOD>
```

## Example

* __Example 1:__

  [(in source)](https://github.com/pritunl/pritunl-web/blob/master/handlers/server.go#L9-L30) `GET /server`

  ```python
  pritunl.server.get()
  ```

* __Example 2:__

  [(in source)](https://github.com/pritunl/pritunl-web/blob/master/handlers/server.go#L140-L150) `PUT /server/:server_id/organization/:organization_id`

  ```python
  pritunl.server.put(srv_id='', org_id='')
  ```

* __Example 3:__

  [(in source)](https://github.com/pritunl/pritunl-web/blob/master/handlers/user.go#L142-L152) `DELETE /user/:organization_id/:user_id`

  ```python
  pritunl.user.delete(org_id='', usr_id='')
  ```

* __Example 4:__

  [(in source)](https://github.com/pritunl/pritunl-web/blob/master/handlers/server.go#L81-L97) `POST /server**`

  ```python
  pritunl.server.post(data={
    'name': 'new server name'})
  ```

   \* _If there is data available, you must pass it through the data parameter._

   \* _The command above works_ well because there are templates available for
   creating a new server._

* __Example 5:__

  [(in source)](https://github.com/pritunl/pritunl-web/blob/master/handlers/user.go#L122-L140) `PUT /user/:organization_id/:user_id`

  ```python
  api.user.put(org_id='', usr_id='', data={
    'name': 'modified org name',
    'disabled': True})
  ```


## API Development

### Using Virtual Environment

```bash
pip install -e .
```

Include REPL Tools

```bash
pip install -e .[repl]
ptipython
```

### Using Docker Environment

Building a Development Container
```bash
docker buildx build . \
  --progress plain \
  --file dev.Dockerfile \
  --tag pritunl-api:development
```

Running a Development Container
```bash
docker run --rm -it \
  --volume $(PWD):/pritunl-api \
  --env-file .env \
  pritunl-api:development poetry shell
```

This API client is not fully complete. There are some features missing,
feel free to fork and pull requests to add new features.

Tested working on **`Pritunl v1.30.3354.99`**.
