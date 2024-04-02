# CWDateControl System README

This document outlines the configuration and interrelation of three DynamoDB tables within the CWDateControl system: `CWDateControl`, `CWHolidayCalendar`, and `CWJobGroupReference`. These tables collectively manage the scheduling and processing of jobs and files, taking into account business dates, holidays, and execution windows.

## Table Descriptions

### CWDateControl Table

This table is responsible for controlling the date logic for job execution.

| Attribute Name       | Data Type | Description |
|----------------------|-----------|-------------|
| JobGroupName         | String    | The name of the job group to which the control belongs. |
| Region               | String    | A sort key that represents the region for which the job group is configured. |
| CatchUpMode          | Boolean   | Indicates if the system is in catch-up mode. |
| CurrentBusinessDate  | Date      | The current business date being processed. |
| IsDay0               | Boolean   | A flag indicating if it's the initial day of processing. |
| IsOnHold             | Boolean   | Specifies whether the job group is on hold and should not be processed. |
| CurrentSnapshotId    | String    | For intraday files, this holds details of the snapshot to be processed. |
| LastUpdatedTime      | Timestamp | The last time this entry was updated. |
| NextBusinessDate     | Date      | The next business date for processing. |
| PreviousBusinessDate | Date      | The business date that was last processed. |

### CWHolidayCalendar Table

This table contains information about weekends and holidays for each job group and region.

| Attribute Name | Data Type | Description |
| -------------- | --------- | ----------- |
| JobGroupName   | String    | The name of the job group this calendar applies to. |
| Year           | String    | Sort key representing the year for the holiday calendar. |
| Weekends       | Set       | A set of days that are considered weekends. |
| Region         | Map       | A map detailing the specific holidays for a region by date. |

### CWJobGroupReference Table

The `CWJobGroupReference` table stores metadata for files/jobs.

| Attribute Name    | Data Type | Description |
| ----------------- | --------- | ----------- |
| JobGroupName      | String    | The name of the job group. |
| Source            | String    | Sort key that represents the source of the job. |
| ExecutionWindow   | List      | An array specifying the time window for processing intraday files. |
| Region            | Map       | Maps the region to the corresponding job group name. |

## Process Flow

1. Before the start of a job, the system checks if the date control is enabled by looking up the `CWDateControl` table.
2. If enabled, the job's batch date is verified against the `CurrentBusinessDate` and `NextBusinessDate` in the `CWDateControl` table.
3. Depending on the `CatchUpMode` and `IsOnHold` flags, the system decides whether to process or skip the job.
4. The `CWHolidayCalendar` table provides information on weekends and holidays, which are used to determine the correct `NextBusinessDate`.
5. For intraday jobs, the `CWJobGroupReference` table provides execution window metadata, which is critical for scheduling the job processing.
6. After a job is processed, the `CWDateControl` table is updated with a new `CurrentBusinessDate` that reflects the next valid business day, considering the data from the `CWHolidayCalendar`.

Please ensure all tables are maintained with up-to-date and accurate information to ensure seamless job scheduling and file processing.

---
