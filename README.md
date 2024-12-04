# Dev

## Dependencies

- Docker Engine
- `git`
- Helm
- `kubectl`
- Minikube
- Tilt

## Quick Start

1. Clone the repository to your local machine
   ```
   git clone https://github.com/virtool/dev.git
   ```

2. Create a Cluster

   ```shell
   bash scripts/init.sh
   ```
   
   This:

   * Deletes any existing cluster.
   * Creates a cluster using preset resource limits.
   * Enables the ingress and metrics addons for Minikube.
   
   You can run commands from `init.sh` individually if you want to customize the
   cluster.

3. Add the cluster IP to `/etc/hosts`:

   ```shell
   bash scripts/hosts.sh
   ```
   
   This puts the IP for the Minikube cluster in `/etc/hosts` for `virtool.local`. This
   will make requests to `virtool.local` on your machine route to the cluster.

4. Start Tilt

   ```shell
   tilt up
   ```
   
   Tilt manages the Kubernetes development environment. It starts all necessary services
   (KEDA, MongoDB, OpenFGA, PostgreSQL, Redis) and the Virtool workloads and services.

## Tilt

### Stopping

You can bring all resources down with `tilt down` and bring them back up with `tilt up`.

We find it is necessary to run `tilt down` before `minikube stop` for the cluster to
stop cleanly.

### Live Editing

Use the `tilt up -- --to-edit <resource>` command to live edit a resource.

This substitutes the image with one built from a local Dockerfile.

For it to work, you must have the repository cloned as a sibling directory to the `dev`
repository. Your parent directory should look like this and include clones of any
repositories you want to live edit:

```
├── dev
├── virtool
├── virtool-ui
├── workflow-create-sample
├── workflow-iimi
└── workflow-pathoscope
```

_Some repositories are not shown in this example._

**`virtool/virtool`**

```shell
tilt up -- --to-edit backend
```

For `virtool/virtool` resources, you have to manually update the resources in Tilt to
trigger an image build.

Resources affected by the image and `--to-edit backend` flag:

* `api-jobs`
* `api-web`
* `migration`
* `task-runner`
* `task-spawner`

**`virtool/virtool-ui`**

```shell
tilt up -- --to-edit ui
```

Changes to code in the `virtool/virtool-ui` repository will be immediately reflected
in the running UI.

Only the `ui` resource is affected by the `--to-edit ui` flag.

**Workflows**

Any workflow repository can be live edited with the following command:

```shell
tilt up -- --to-edit <workflow>
```

Where `workflow` is one of:

* `build-index`
* `create-sample`
* `create-subtraction`
* `iimi`
* `pathoscope`
* `nuvs`

Every time the repository changes, the image will be rebuilt.

```shell

## Update images

We provide an easy way to update the Virtool container images in the cluster.

### Tilt

Click the 'Pull' button in the top-right of the navigation bar in the Tilt UI.

### Bash

```shell
bash scripts/pull.sh
```

## Wiping the Cluster

If you need to start fresh, you can just run `init.sh` again:

```shell
bash scripts/init.sh
```