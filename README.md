# Pritunl API client for Python 3

This is a simple api client written in Python 3. View example in
example.py.
Python 2 is not supported. You need to refer Pritunl api doc to get the
idea on how to use this.

Basically this api client use almost same command like in the doc.
For example:


## Quick Usage

```bash
import os

from pritunl_api import Pritunl

PRITUNL_BASE_URL = os.environ.get('PRITUNL_BASE_URL')
PRITUNL_API_TOKEN = os.environ.get('PRITUNL_API_TOKEN')
PRITUNL_API_SECRET= os.environ.get('PRITUNL_API_SECRET')

pritunl = Pritunl(
    url=PRITUNL_BASE_URL,
    token=PRITUNL_API_TOKEN,
    secret=PRITUNL_API_SECRET
    )

```

## Example

* Example 1

  [(in source)](https://github.com/pritunl/pritunl-web/blob/master/handlers/server.go#L9-L30) `GET /server/:server_id`

  ```python
  pritunl.server.get()
  ```

* Example 2

  [(in source)](https://github.com/pritunl/pritunl-web/blob/master/handlers/server.go#L140-L150) `PUT /server/:server_id/organization/:organization_id`

  ```python
  pritunl.server.put(srv_id='', org_id='')
  ```

* Example 3

  [(in source)](https://github.com/pritunl/pritunl-web/blob/master/handlers/user.go#L142-L152) `DELETE /user/:organization_id/:user_id`

  ```python
  pritunl.user.delete(org_id='', usr_id='')
  ```

* Example 4

  [(in source)](https://github.com/pritunl/pritunl-web/blob/master/handlers/server.go#L81-L97) `POST /server**`

  ```python
  pritunl.server.post(data={
    'name': 'new server name'})
  ```

   \* _If there is data available, you must pass it through data parameter._

   \* _Command above works well because there are template available for
   creating a new server._

* Example 5

  [(in source)](https://github.com/pritunl/pritunl-web/blob/master/handlers/user.go#L122-L140) `PUT /user/:organization_id/:user_id`

  ```python
  api.user.put(org_id='', usr_id='', data={
    'name': 'modified org name',
    'disabled': True})
  ```


## Installation

```bash
pip install pritunl-api
```

Include REPL Tools

```bash
pip install pritunl-api[repl]
```

## API Development

### Docker Environment

Building a Development Container
```sh
docker buildx build . \
  --progress plain \
  --file dev.Dockerfile \
  --tag pritunl-api:development
```

Running a Development Container

```sh
docker run --rm -it \
  --volume $(PWD):/pritunl-api \
  --env-file .env \
  pritunl-api:development
```

***
This api client is not fully complete. There are some features missing,
feel free to fork and pull request to add new features.

Tested working on **`Pritunl v1.30.3354.99`**.
