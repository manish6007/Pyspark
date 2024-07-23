Sure, let's outline the design for your query builder framework in AWS, focusing on the architecture and components without diving into the code.

### Design for Query Builder Framework

#### 1. Configuration Storage in DynamoDB

**Table Name: `DataRetrievalConfigs`**

**Attributes:**
- **ConfigId (Partition Key)**: Unique identifier for each configuration.
- **ConfigType (Sort Key)**: Type of configuration (e.g., "TABLE", "COLUMN", "JOIN", "FILTER").
- **TableName**: Name of the table (for TABLE type).
- **Columns**: List of column names (for COLUMN type).
- **JoinCondition**: Map containing join details (for JOIN type).
- **FilterCondition**: String representing the filter condition (for FILTER type).
- **Description**: Optional description of the configuration.
- **LastUpdated**: Timestamp of the last update.

#### Example Items in the Table:
1. **Table Configuration:**
   ```
   {
     "ConfigId": "SALES_DATA",
     "ConfigType": "TABLE",
     "TableName": "sales_transactions",
     "Description": "Main sales data table",
     "LastUpdated": "2024-07-23T10:00:00Z"
   }
   ```

2. **Column Configuration:**
   ```
   {
     "ConfigId": "SALES_DATA",
     "ConfigType": "COLUMN",
     "Columns": ["transaction_id", "customer_id", "product_id", "sale_amount", "sale_date"],
     "Description": "Columns for sales data retrieval",
     "LastUpdated": "2024-07-23T10:05:00Z"
   }
   ```

3. **Join Configuration:**
   ```
   {
     "ConfigId": "SALES_DATA",
     "ConfigType": "JOIN",
     "JoinCondition": {
       "type": "INNER",
       "table": "customers",
       "on": "sales_transactions.customer_id = customers.id"
     },
     "Description": "Join condition for customer details",
     "LastUpdated": "2024-07-23T10:10:00Z"
   }
   ```

4. **Filter Configuration:**
   ```
   {
     "ConfigId": "SALES_DATA",
     "ConfigType": "FILTER",
     "FilterCondition": "sale_date >= :start_date AND sale_amount > :min_amount",
     "Description": "Filter for recent high-value sales",
     "LastUpdated": "2024-07-23T10:15:00Z"
   }
   ```

### 2. Query Builder Logic

#### a. **Components of the Query Builder:**

1. **QueryConfigLoader:**
   - **Purpose:** Retrieve configuration data from DynamoDB.
   - **Inputs:** ConfigId.
   - **Outputs:** Configuration items.

2. **QueryBuilder:**
   - **Purpose:** Construct the SQL query using the retrieved configuration.
   - **Inputs:** Configuration items (e.g., Table, Columns, JoinCondition, FilterCondition).
   - **Outputs:** SQL query string.

3. **QueryExecutor:**
   - **Purpose:** Execute the constructed SQL query on the specified database (Athena or Redshift).
   - **Inputs:** SQL query string, database type.
   - **Outputs:** Execution results (or query execution ID).

#### b. **Interaction Flow:**

1. **Load Configuration:**
   - **Action:** `QueryConfigLoader` fetches configuration items from DynamoDB based on the provided ConfigId.
   - **Outcome:** Configuration items are retrieved and passed to the `QueryBuilder`.

2. **Build Query:**
   - **Action:** `QueryBuilder` constructs the SQL query string using the configuration items.
   - **Outcome:** A complete SQL query string is generated.

3. **Execute Query:**
   - **Action:** `QueryExecutor` takes the SQL query string and executes it on the specified database (Athena or Redshift).
   - **Outcome:** The query is executed, and the results (or execution ID) are returned.

### 3. AWS Service Integration

#### a. **DynamoDB Integration:**
   - **Service:** AWS DynamoDB
   - **Role:** Store and retrieve configuration data.

#### b. **Athena Integration:**
   - **Service:** AWS Athena
   - **Role:** Execute queries and retrieve data from S3.

#### c. **Redshift Integration:**
   - **Service:** Amazon Redshift
   - **Role:** Execute queries and retrieve data from the Redshift cluster.

### Architecture Diagram

```
+-------------------+        +------------------+        +------------------+
|   Client Request  | -----> | QueryConfigLoader| -----> |  DynamoDB Table  |
+-------------------+        +------------------+        +------------------+
                                          |
                                          v
                                  +------------------+
                                  |  QueryBuilder    |
                                  +------------------+
                                          |
                                          v
                                  +------------------+
                                  | QueryExecutor    |
            +-------------------->+------------------+<----------------------+
            |                     |                  |                       |
            v                     v                  v                       v
     +-------------+       +-------------+    +-------------+         +--------------+
     |   Athena    |       |   Redshift  |    | Execution   |         |   Results    |
     |   Client    |       |   Client    |    |   Results   |         +--------------+
     +-------------+       +-------------+    +-------------+
```

### Summary

1. **DynamoDB Table:** Store configurations using a composite key schema.
2. **QueryConfigLoader:** Load configurations from DynamoDB.
3. **QueryBuilder:** Build SQL queries based on the loaded configurations.
4. **QueryExecutor:** Execute the SQL queries on Athena or Redshift and handle the results.

This design ensures flexibility, scalability, and separation of concerns, making it easier to maintain and extend the query builder framework as needed.
