from aws_startup import (
    DWH_CLUSTER_IDENTIFIER,
    BUCKETNAME,
    DWH_IAM_ROLE_NAME,
    redshift,
    iam,
    s3,
    config,
)
from time import sleep

# ----- CODE ----

# Delete the Redshift cluster we created.
def delete_redshift():
    try:
        redshift.delete_cluster(
            ClusterIdentifier=DWH_CLUSTER_IDENTIFIER, SkipFinalClusterSnapshot=True
        )
        # Not quite sure why am I accessing this. Need to be lookat in a refractor.
        myClusterProps = redshift.describe_clusters(
            ClusterIdentifier=DWH_CLUSTER_IDENTIFIER
        )["Clusters"][0]
        sleep(5)
        delete_redshift()
    except redshift.exceptions.InvalidClusterStateFault as e:
        sleep(10)
        print("Cluster currently deleting.")
        delete_redshift()
    except redshift.exceptions.ClusterNotFoundFault as e:
        print("Cluster was successfully deleted.")


# Delete the IAM role we created
def delete_iam():
    try:
        iam.detach_role_policy(
            RoleName=DWH_IAM_ROLE_NAME,
            PolicyArn="arn:aws:iam::aws:policy/AmazonS3FullAccess",
        )
        iam.delete_role(RoleName=DWH_IAM_ROLE_NAME)
        sleep(5)
        delete_iam()
    except iam.exceptions.NoSuchEntityException as e:
        print("IAM role successfully deleted.")
    except Exception as e:
        print(e)
        delete_iam()


def delete_s3():
    try:
        bucket = s3.Bucket(BUCKETNAME)
        bucket.objects.all().delete()
        bucket.delete()
        print("S3 Bucket sucessfully deleted.")
    except s3.meta.client.exceptions.NoSuchBucket as e:
        print("S3 Bucket with all content successfully deleted.")
    except Exception as e:
        print(e)
        print("Something went wrong, trying again in a bit.")
        sleep(5)
        delete_s3()


# Run all the functions if the script is called.
if __name__ == "__main__":
    try:
        delete_redshift()
    except redshift.exceptions.ClusterNotFoundFault as e:
        pass
    try:
        delete_iam()
    except iam.exceptions.NoSuchEntityException as e:
        pass
    try:
        delete_s3()
    except s3.exceptions.NoSuchBucket as e:
        pass
    print("All resources deleted.")
