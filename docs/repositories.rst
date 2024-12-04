Repositories
############

``virtool/virtool``
===================

`Github <https://github.com/virtool/virtool>`_ | `Docs <https://virtool.github.io>`_

This is the primary repository for the whole project.

It contains code for services including the API server.

- Servers for web and job API requests.
- A service the spawns periodic background tasks at regular intervals.
- A service the runs tasks on demand.
- CLI commands for creating, running, and managing data migrations.

`virtool-core <https://github.com/virtool/virtool-core>`_
=========================================================

This repository is contains code reused in multiple other repositories.

Most importantly, it contains Pydantic models for all of our data resources. These allow
us to validate and shape data leaving the API in HTTP responses as well as validating
data being ingested into ``virtool-workflow``.

It also contains reusable code for initializing logs, connecting to databases, and other
shared functionality.

`ui <https://github.com/virtool/ui>`_
=====================================================

This repository contains the code for the web client.

`virtool-workflow <https://github.com/virtool/virtool-workflow>`_
=================================================================

A framework for running workflows.

- Includes code for for defining workflow steps and accessing data.
- Fetches and pushes data to and from the server.
- Calls external tools as subprocesses.
- Handles and reports errors in workflows to the API.

