# Pritunl API Client for Python 3

This is a simple [Pritunl](https://pritunl.com/) API Client written in Python 3.

You need to refer to Pritunl [API Documentation](https://docs.pritunl.com/docs/api) to understand how to use this. This API client uses almost the same command as the [API Handlers](https://github.com/pritunl/pritunl-web/tree/master/handlers).

## Installation

Install the published package using `pip` from our [PyPI project repository](https://pypi.org/project/pritunl-api/).

```bash
pip install pritunl-api
```

Beyond the core API client library, we also added the executable distribution in this project. Add extra `cli` during the PIP installation to enable the CLI feature.

```bash
pip install pritunl-api[cli]
```

Proceed to the [CLI Usage](#cli-usage) for the complete command options and syntax.


## API Usage

Before using the API library including the use of the CLI feature, we need to provide the Pritunl API URL and administrative credentials in our environment variables.

```bash
export PRITUNL_BASE_URL="https://vpn.domain.tld/"
export PRITUNL_API_TOKEN="XXXXXXXXXXXXXXXXXXXXXX"
export PRITUNL_API_SECRET="XXXXXXXXXXXXXXXXXXXXX"
```

Initializing an API object.

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
  pritunl.server.post(
    data={
      'name': 'new server name'
    }
  )
  ```
   * _If there is data available, you must pass it through the data parameter._
   * _The command above works well because there are templates available for creating a new server._

* __Example 5:__

  [(in source)](https://github.com/pritunl/pritunl-web/blob/master/handlers/user.go#L122-L140) `PUT /user/:organization_id/:user_id`

  ```python
  pritunl.user.put(org_id='', usr_id='',
    data={
      'name': 'modified org name',
      'disabled': True
    }
  )
  ```

## CLI Usage

### Available Commands

> As of this period of development, the feature is limited.

To show the available commands, use the help option.

```bash
pritunl-api-cli --help
```

```txt
Usage: pritunl-api-cli [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create-user
  delete-user
  get-user
  update-user
```

For available command options and syntax, use the feature command help option.

```bash
pritunl-api-cli create-user --help
```

```text
Usage: pritunl-api-cli create-user [OPTIONS]

Options:
  --org-name TEXT
  --user-name TEXT
  --user-email TEXT
  --pin TEXT
  --yubikey-id TEXT
  --from-csv-file PATH
  --help                Show this message and exit.
```

#### Create User

_Example 1: Create a Single User_

```bash
pritunl-api-cli create-user \
  --org-name develop-network \
  --user-name developer_1 \
  --user-email developer_1@domain.tld
```

_Example 2: Create Users from CSV_

```bash
pritunl-api-cli create-user \
  --from-csv-file ./users.csv
```

#### Delete User

```bash
pritunl-api-cli delete-user \
  --org-name develop-network \
  --user-name developer_1
```

#### Get User Information

```bash
pritunl-api-cli get-user \
  --org-name develop-network \
  --user-name developer_1
```

> Or get (regenerate) the profile key of a user

```bash
pritunl-api-cli get-user \
  --org-name develop-network \
  --user-name developer_1 \
  --get-profile-key-only
```

#### Update a User

To disable a user

```bash
pritunl-api-cli update-user \
  --org-name develop-network \
  --user-name developer_1 \
  --disable
```

To enable a user

```bash
pritunl-api-cli update-user \
  --org-name developer-network \
  --user-name developer_1 \
  --enable
```

## API Development

### Using Virtual Environment

Create a virtual environment and activate it.

```bash
python -m venv ./venv
source ./venv/bin/activate
```

> Or simple use other Python Version Manager like [pyenv](https://github.com/pyenv/pyenv).

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
  pritunl-api:development
```

This API client is not fully complete. Some features are missing, feel free to fork and pull requests to add new features.

Tested working on **`Pritunl v1.30.3354.99`**.
