# Configuration
config.define_string_list("to-edit")

cfg = config.parse()
to_edit = cfg.get('to-edit', [])

# Backing Services and Components
load('ext://helm_resource', 'helm_resource', 'helm_repo')

helm_repo('bitnami', 'https://charts.bitnami.com/bitnami', labels=['helm'])
helm_repo('kedacore', 'https://kedacore.github.io/charts', labels=['helm'])

watch_file("manifests/mongo_values.yaml")

helm_resource(
    'mongo',
    'bitnami/mongodb',
    flags=["-f", "manifests/mongo_values.yaml"],
    port_forwards=[27017],
    labels=['data']
)

helm_resource(
    'postgresql',
    'bitnami/postgresql',
    flags=["--set", "auth.username=virtool", "--set", "auth.password=virtool", "--set", "auth.database=virtool"],
    port_forwards=[5432],
    labels=['data']
)

helm_resource(
    'redis',
    'bitnami/redis',
    flags=['--set', 'architecture=standalone', '--set', 'auth.password=virtool', "--set", "master.disableCommands=null"],
    labels=['data'],
    port_forwards=[6379],
)


helm_resource('keda', 'kedacore/keda', labels=['keda'])

k8s_yaml('manifests/ingress.yaml')


k8s_yaml('manifests/nfs.yaml')
k8s_resource('nfs-server', labels=['data'], new_name='nfs')

k8s_yaml('manifests/openfga-migration.yaml')
k8s_resource("openfga-migration", labels=['migration'], resource_deps=["postgresql"])

k8s_yaml('manifests/openfga.yaml')
k8s_resource('openfga', labels=['data'], resource_deps=["openfga-migration"], port_forwards=[8080])

k8s_yaml('manifests/migration.yaml')
k8s_resource('virtool-migration', labels=['migration'], resource_deps=["postgresql", "mongo"])

# Actual Virtool stuff.
if 'ui' in to_edit:
    docker_build(
      'ghcr.io/virtool/ui',
      '../virtool-ui/',
      entrypoint='npx vite serve --host 0.0.0.0 --port 9900',
      target='dev',
      live_update=[
        fall_back_on(['../virtool-ui/package.json', '../virtool-ui/package-lock.json']),
        sync('../virtool-ui/src', '/build/src')
      ]
    )

k8s_yaml('manifests/ui.yaml')
k8s_resource('virtool-ui', port_forwards=[3000, 9900], labels=['virtool'])

if 'backend' in to_edit:
    docker_build('ghcr.io/virtool/virtool', '../virtool/')

api_resource_deps=["mongo", "postgresql", "openfga", "nfs", "redis", "virtool-migration"]

k8s_yaml('manifests/api.yaml')
k8s_resource('virtool-api-web', port_forwards=[9950], labels=['virtool'], resource_deps=api_resource_deps)

k8s_yaml('manifests/jobs_api.yaml')
k8s_resource('virtool-api-jobs', port_forwards=["9960:9950"], labels=['virtool'], resource_deps=api_resource_deps)

k8s_yaml('manifests/tasks_runner.yaml')
k8s_resource('virtool-tasks-runner', port_forwards=["9970:9950"], labels=['virtool'], resource_deps=api_resource_deps)

k8s_yaml('manifests/tasks/AddSubtractionFiles.yaml')
k8s_resource('add-subtraction-files', resource_deps=api_resource_deps)

"""
Jobs
"""
jobs = ['shared.yaml', 'build-index.yaml','create-sample.yaml']

if 'create-sample' in to_edit:
    docker_build('ghcr.io/virtool/create-sample', '../workflow-create-sample/')

k8s_kind('ScaledJob', image_json_path='{.spec.jobTargetRef.template.spec.containers[0].image}')

k8s_yaml('manifests/jobs/shared.yaml')
k8s_resource(objects=['virtool-jobs-config'], labels=["jobs"], new_name="shared-config")

k8s_yaml('manifests/jobs/build-index.yaml')
k8s_resource("virtool-job-build-index", labels=["jobs"], new_name="build-index", resource_deps=['keda'])

k8s_yaml('manifests/jobs/create-sample.yaml')
k8s_resource('virtool-job-create-sample', labels=["jobs"], new_name="create-sample", resource_deps=['keda'])

k8s_yaml('manifests/jobs/create-subtraction.yaml')
k8s_resource('virtool-job-create-subtraction', labels=["jobs"], new_name="create-subraction", resource_deps=["keda"])

k8s_yaml('manifests/jobs/nuvs.yaml')
k8s_resource('virtool-job-nuvs', labels=["jobs"], new_name="nuvs", resource_deps=["keda"])

k8s_yaml('manifests/jobs/pathoscope.yaml')
k8s_resource('virtool-job-pathoscope', labels=["jobs"], new_name="pathoscope", resource_deps=["keda"])
