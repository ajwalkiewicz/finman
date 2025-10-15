# Utility scripts

Scripts should be run from the project's root directory.

## publish.sh

Used internally to publish the recent changes to the server.

Environmental variables:

| ENV    | Description                                            |
|--------|--------------------------------------------------------|
| PORT   | port for SSH connection, defaults to 22                |
| SOURCE | directory to transfer to the server                    |
| HOST   | server address                                         |
| DEST   | directory on the server to which files are transferred | 