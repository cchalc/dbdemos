import json
from dbdemos.conf import Conf, DemoConf
from dbdemos.installer import Installer
from dbdemos.job_bundler import JobBundler
from dbdemos.packager import Packager
import traceback

with open("./local_conf.json", "r") as r:
    c = json.loads(r.read())
with open("./dbdemos/resources/default_cluster_config.json", "r") as cc:
    default_cluster_template = cc.read()
with open("./dbdemos/resources/default_test_job_conf.json", "r") as cc:
    default_cluster_job_template = cc.read()

conf = Conf(c['username'], c['url'], c['org_id'], c['pat_token'],
            default_cluster_template, default_cluster_job_template,
            c['repo_staging_path'], c['repo_name'], c['repo_url'], c['branch'])

def bundle():
    bundler = JobBundler(conf)
    # the bundler will use a stating repo dir in the workspace to analyze & run content.
    bundler.reset_staging_repo(skip_pull=False)
    # Discover bundles from repo:
    #bundler.load_bundles_conf()
    # Or manually add bundle to run faster:
    """
    bundler.add_bundle("product_demos/Unity-Catalog/01-Table-ACL")
    bundler.add_bundle("product_demos/Unity-Catalog/02-External-location")
    bundler.add_bundle("product_demos/Unity-Catalog/03-Data-lineage")
    bundler.add_bundle("product_demos/Unity-Catalog/04-Audit-log")
    bundler.add_bundle("product_demos/Unity-Catalog/05-Upgrade-to-UC")
    bundler.add_bundle("product_demos/DBSQL-Datawarehousing/01-FK-PK-Indentity-Data-modeling")
    bundler.add_bundle("product_demos/Data-Science/Koalas")
    bundler.add_bundle("product_demos/Delta-Live-Table/Delta-Live-Table-Unit-Test")
    bundler.add_bundle("product_demos/Delta-Live-Table/Delta-Live-Table-CDC")
    bundler.add_bundle("product_demos/Delta-Sharing")
    bundler.add_bundle("product_demos/Auto-Loader (cloudFiles)")
    bundler.add_bundle("demo-retail/lakehouse-retail-c360")
    bundler.add_bundle("product_demos/Delta-Live-Table/Delta-Live-Table-loans")
    bundler.add_bundle("product_demos/Delta-Lake")
    bundler.add_bundle("product_demos/Auto-Loader (cloudFiles)")
    bundler.add_bundle("product_demos/Unity-Catalog/03-Data-lineage")
    bundler.add_bundle("product_demos/Delta-Lake-CDC-CDF")
    bundler.add_bundle("product_demos/streaming-sessionization")
    bundler.add_bundle("product_demos/Delta-Live-Table/Delta-Live-Table-Unit-Test")
"""

    #bundler.add_bundle("product_demos/Unity-Catalog/05-Upgrade-to-UC")
    #bundler.load_bundles_conf()
    bundler.add_bundle("product_demos/Data-Science/mlops-end2end")
    #bundler.add_bundle("demo-manufacturing/lakehouse-iot-platform")
    bundler.add_bundle("demo-retail/lakehouse-retail-c360")
    #bundler.add_bundle("demo-manufacturing/lakehouse-iot-platform")
    #bundler.add_bundle("product_demos/Delta-Live-Table/Delta-Live-Table-Unit-Test")
    #bundler.add_bundle("product_demos/streaming-sessionization")


    # Run the jobs (only if there is a new commit since the last time, or failure, or force execution)
    bundler.start_and_wait_bundle_jobs(force_execution = False, skip_execution=False)

    packager = Packager(conf, bundler)
    packager.package_all()

#TODO: some demos have cross data dependencies & datasets get deleted by other demos installation. Retrying usually fix it
#Need to remove the dependency and fully isolate the demos.
def bundle_with_retry(max_retry = 3):
    retry = 0
    while retry < max_retry:
        try:
            print(f"bundle - retry {retry}")
            bundle()
            retry += max_retry
        except Exception as e:
            retry += 1
            traceback.print_exc()
            print(str(e))

#bundle_with_retry(1)

#Loads conf to install on cse2.
with open("local_conf.json", "r") as r:
    c = json.loads(r.read())

from dbdemos.installer import Installer
import dbdemos


#dbdemos.install_all("/Users/quentin.ambard@databricks.com/test_install_quentin", True, c['username'], c['pat_token'], c['url'], cloud="AWS", start_cluster = False, skip_dashboards = True)
#dbdemos.check_status_all(c['username'], c['pat_token'], c['url'], cloud="AWS")
#dbdemos.install("lakehouse-retail-c360", "/Users/quentin.ambard@databricks.com/test_install_quentin", True, c['username'], c['pat_token'], c['url'], cloud="AWS", start_cluster = False)
#installer = Installer()
#for d in installer.get_demos_available():
#    dbdemos.install(d, "/Users/quentin.ambard@databricks.com/test_dbdemos", True, c['username'], c['pat_token'], c['url'], cloud="AWS")


#dbdemos.list_demos(None)
dbdemos.install("lakehouse-retail-c360", "/Users/quentin.ambard@databricks.com/test_install_quentin", True, c['username'], c['pat_token'], c['url'], cloud="AWS")
#dbdemos.install("lakehouse-iot-platform", "/Users/quentin.ambard@databricks.com/test_install_quentin", True, c['username'], c['pat_token'], c['url'], cloud="AWS")
#dbdemos.install("streaming-sessionization", "/Users/quentin.ambard@databricks.com/test_install_quentin", True, c['username'], c['pat_token'], c['url'], cloud="AWS")
#dbdemos.install("uc-03-data-lineage", "/Users/quentin.ambard@databricks.com/test_install_quentin", True, c['username'], c['pat_token'], c['url'], cloud="AWS")
#dbdemos.install("mlops-end2end", "/Users/quentin.ambard@databricks.com/test_install_quentin", True, c['username'], c['pat_token'], c['url'], cloud="AWS", skip_dashboards=True)
#dbdemos.install("pandas-on-spark", "/Users/quentin.ambard@databricks.com/test_install_quentin", True, c['username'], c['pat_token'], c['url'], cloud="AWS")
#dbdemos.install("lakehouse-retail-churn", "/Users/ioannis.papadopoulos@databricks.com/test_install_quentin", True, c['username'], c['pat_token'], c['url'], cloud="GCP")
#dbdemos.install("delta-lake", "/Users/quentin.ambard@databricks.com/test_install_quentin", True, c['username'], c['pat_token'], c['url'], cloud="AWS")
#dbdemos.install("delta-sharing-airlines", "/Users/quentin.ambard@databricks.com/test_install_quentin", True, c['username'], c['pat_token'], c['url'])
#dbdemos.install("dlt-cdc", "/Users/quentin.ambard@databricks.com/test_install_quentin", True, c['username'], c['pat_token'], c['url'])
#dbdemos.install("dlt-loans", "/Users/quentin.ambard@databricks.com/test_install_quentin", True, c['username'], c['pat_token'], c['url'])
#dbdemos.install("dlt-unit-test", "/Users/quentin.ambard@databricks.com/test_install", True, c['username'], c['pat_token'], c['url'])
#dbdemos.install("uc-01-acl", "/Users/quentin.ambard@databricks.com/test_install_quentin", True, c['username'], c['pat_token'], c['url'])
#dbdemos.install("uc-05-upgrade", "/Users/quentin.ambard@databricks.com/test_install_quentin", True, c['username'], c['pat_token'], c['url'])
#dbdemos.create_cluster("uc-05-upgrade", c['username'], c['pat_token'], c['url'], c['current_folder'])
