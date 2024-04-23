**SQL Queries for Managing Amazon Redshift DataShare**

**Introduction**</br>
Amazon Redshift DataShare enables users to share data across different Redshift clusters without the need for data replication. This document lists the necessary SQL commands for setting up and managing Redshift DataShare.

**1. Creating a Data Share** </br>
To create a new data share, use the following SQL command:

```sql
CREATE DATASHARE my_data_share;
```

**2. Adding Comments to Data Share** </br>
To add a comment to a data share for better description or documentation, use:

```sql
ALTER DATASHARE my_data_share ADD COMMENT 'This is a shared data repository';
```

**3. Adding Objects to Data Share** </br>
You can include entire schemas or specific tables in your data share.

- **Add Schema:**</br>
  ```sql
  ALTER DATASHARE my_data_share ADD SCHEMA public;
  ```
- **Add Table:**
  ```sql
  ALTER DATASHARE my_data_share ADD TABLE public.my_table;
  ```

**4. Describing a Data Share** </br>
To view the properties and the objects of a data share, execute:

```sql
DESCRIBE DATASHARE my_data_share;
```

**5. Listing Data Shares** </br>
To list all data shares on your Redshift cluster:

```sql
SELECT * FROM SVV_DATASHARES;
```

**6. Authorizing a Consumer** </br>
To authorize a specific account to access the data share:

```sql
ALTER DATASHARE my_data_share AUTHORIZE ACCOUNT consumer_account_id;
```

**7. De-Authorizing a Consumer** </br>
To revoke access from a previously authorized account:

```sql
ALTER DATASHARE my_data_share DEAUTHORIZE ACCOUNT consumer_account_id;
```

**8. Associating Data Share (As Consumer)** </br>
To associate a data share from another account for use on a consumer cluster:

```sql
ASSOCIATE DATASHARE my_data_share OF ACCOUNT producer_account_id;
```

**9. Using Data Share (As Consumer)** </br>
Once associated, create a schema to access the data share:

```sql
CREATE SCHEMA my_consumer_schema FROM DATASHARE my_data_share OF ACCOUNT producer_account_id;
```

**10. Dropping Data Share Association (As Consumer)** </br>
To disassociate a data share from your cluster:

```sql
DISASSOCIATE DATASHARE my_data_share OF ACCOUNT producer_account_id;
```

**11. Dropping Objects from Data Share** </br>
To remove objects from a data share:

- **Drop Schema:** </br>
  ```sql
  ALTER DATASHARE my_data_share DROP SCHEMA public;
  ```
- **Drop Table:** </br>
  ```sql
  ALTER DATASHARE my_data_share DROP TABLE public.my_table;
  ```

**12. Dropping a Data Share** </br>
To completely remove a data share from the system:

```sql
DROP DATASHARE my_data_share;
```

**Conclusion**
The provided SQL queries facilitate the effective management of Redshift DataShare, from creation and modification to sharing and consuming data across different Redshift clusters.
