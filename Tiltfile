load('ext://restart_process', 'docker_build_with_restart')

# Configuration
config.define_string_list("to-edit")
config.define_bool("persistence")

cfg = config.parse()
to_edit = cfg.get('to-edit', [])
persistence = cfg.get('persistence', True)

# Backing Services and Components
load('ext://helm_resource', 'helm_resource', 'helm_repo')

helm_repo('bitnami', 'https://charts.bitnami.com/bitnami', labels=['helm'])
helm_repo('kedacore', 'https://kedacore.github.io/charts', labels=['helm'])

watch_file("manifests/mongo_values.yaml")

helm_resource(
    'mongo',
    'bitnami/mongodb',
    flags=["--set","image.tag=7.0.5-debian-12-r5", "-f", "manifests/mongo_values.yaml", "--set", "persistence.enabled={}".format(persistence)],
    port_forwards=[27017],
    labels=['data']
)

helm_resource(
    'postgresql',
    'bitnami/postgresql',
    flags=["--set", "image.tag=15.4.0-debian-11-r47","--set", "auth.username=virtool", "--set", "auth.password=virtool", "--set", "auth.database=virtool", "--set", "primary.persistence.enabled={}".format(persistence)],
    port_forwards=[5432],
    labels=['data']
)

helm_resource(
    'redis',
    'bitnami/redis',
    flags=['--set','image.tag=7.2.1-debian-11-r0', '--set', 'architecture=standalone', '--set', 'auth.password=virtool', "--set", "master.disableCommands=null", "--set", "master.persistence.enabled={}".format(persistence)],
    labels=['data'],
    port_forwards=[6379],
)

helm_resource('keda', 'kedacore/keda', labels=['keda'])

k8s_yaml('manifests/ingress.yaml')

nfs_resources = read_yaml_stream('manifests/nfs.yaml')
if not persistence:
    for resource in nfs_resources:
        if resource["metadata"]["name"] == "nfs-server":
            resource["spec"]["containers"][0].pop("volumeMounts")

k8s_yaml(encode_yaml_stream(nfs_resources))
k8s_resource('nfs-server', labels=['data'], new_name='nfs')

k8s_yaml('manifests/openfga-migration.yaml')
k8s_resource("openfga-migration", labels=['migration'], resource_deps=["postgresql"])

k8s_yaml('manifests/openfga.yaml')
k8s_resource('openfga', labels=['data'], resource_deps=["openfga-migration"], port_forwards=[8080, 3000])

if 'migration' in to_edit:
    docker_build('ghcr.io/virtool/migration', '../virtool-migration/')

k8s_yaml('manifests/migration.yaml')
k8s_resource('virtool-migration', labels=['migration'], resource_deps=["mongo", "nfs", "openfga","postgresql"], trigger_mode=TRIGGER_MODE_MANUAL)

docker_prune_settings(max_age_mins=1)

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
k8s_resource('virtool-ui', port_forwards=[9900], labels=['virtool'])

if 'backend' in to_edit:
    docker_build(
        'ghcr.io/virtool/virtool',
        '../virtool/',
    )

api_resource_deps=["mongo", "postgresql", "openfga", "nfs", "redis", "virtool-migration"]

k8s_yaml('manifests/api-web.yaml')
k8s_resource(
    'virtool-api-web',
    labels=['virtool'],
    port_forwards=[9950],
    resource_deps=api_resource_deps,
    trigger_mode=TRIGGER_MODE_MANUAL
)

k8s_yaml('manifests/api-jobs.yaml')
k8s_resource('virtool-api-jobs', port_forwards=["9960:9950"], labels=['virtool'], resource_deps=api_resource_deps, trigger_mode=TRIGGER_MODE_MANUAL)

k8s_yaml('manifests/task-runner.yaml')
k8s_resource('virtool-task-runner', port_forwards=["9970:9950"], labels=['virtool'], resource_deps=api_resource_deps, trigger_mode=TRIGGER_MODE_MANUAL)

k8s_yaml('manifests/task-spawner.yaml')
k8s_resource('virtool-task-spawner', labels=['virtool'], resource_deps=api_resource_deps, trigger_mode=TRIGGER_MODE_MANUAL)

"""
Jobs
"""
jobs = ['shared.yaml', 'build-index.yaml','create-sample.yaml']

if "build-index" in to_edit:
    docker_build(
        'ghcr.io/virtool/build-index',
        '../workflow-build-index/',
        target='base'
    )

if "create-sample" in to_edit:
    docker_build(
        'ghcr.io/virtool/create-sample',
        '../workflow-create-sample/',
        target='base'
    )

if "create-subtraction" in to_edit:
    docker_build(
        'ghcr.io/virtool/create-subtraction',
        '../workflow-create-subtraction/',
        target='base'
    )

if "iimi" in to_edit:
    docker_build('ghcr.io/virtool/iimi', '../workflow-iimi/', target='base')

if "nuvs" in to_edit:
    docker_build(
        'ghcr.io/virtool/nuvs',
        '../workflow-nuvs/',
        target='base'
    )

if "pathoscope" in to_edit:
    docker_build(
        'ghcr.io/virtool/pathoscope',
        '../workflow-pathoscope/',
        target='base'
    )

k8s_kind('ScaledJob', image_json_path='{.spec.jobTargetRef.template.spec.containers[0].image}')

k8s_yaml('manifests/jobs/shared.yaml')
k8s_resource(objects=['virtool-jobs-config'], labels=["jobs"], new_name="shared-config")

k8s_yaml('manifests/jobs/build-index.yaml')
k8s_resource("virtool-job-build-index", labels=["jobs"], new_name="build-index", resource_deps=['keda'])

k8s_yaml('manifests/jobs/create-sample.yaml')
k8s_resource('virtool-job-create-sample', labels=["jobs"], new_name="create-sample", resource_deps=['keda'])

k8s_yaml('manifests/jobs/create-subtraction.yaml')
k8s_resource('virtool-job-create-subtraction', labels=["jobs"], new_name="create-subraction", resource_deps=["keda"])

k8s_yaml('manifests/jobs/iimi.yaml')
k8s_resource('virtool-job-iimi', labels=["jobs"], new_name="iimi", resource_deps=["keda"])

k8s_yaml('manifests/jobs/nuvs.yaml')
k8s_resource('virtool-job-nuvs', labels=["jobs"], new_name="nuvs", resource_deps=["keda"])

k8s_yaml('manifests/jobs/pathoscope.yaml')
k8s_resource('virtool-job-pathoscope', labels=["jobs"], new_name="pathoscope", resource_deps=["keda"])
