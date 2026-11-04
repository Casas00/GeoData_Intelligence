# GeoData Intelligence — Data Model

**Version:** 0.1.0  
**Status:** Initial implementation  
**Database:** PostgreSQL + PostGIS

## 1. Overview

The application uses a relational metadata model to manage datasets, logical schema definitions, data sources, ingestion processes and transformation history.

The metadata tables are stored in the PostgreSQL `metadata` schema.

Dataset records are stored separately in their corresponding physical PostgreSQL schemas and tables.

## 2. Database tables

### 2.1. `metadata.dataset_schemas`

Stores reusable logical schema definitions and their versions.

| Field | Type | Constraints | Description |
|---|---|---|---|
| schema_id | Integer | PK | Unique identifier |
| name | VARCHAR(150) | NOT NULL | Logical schema name |
| description | TEXT | NULL | Description |
| version | Integer | NOT NULL | Schema version |
| definition | JSONB | NOT NULL | Logical schema definition |
| created_at | TIMESTAMPTZ | NOT NULL | Creation timestamp |

**Unique constraint:** `(name, version)`

### 2.2. `metadata.datasets`

Stores registered datasets and their physical database location.

| Field | Type | Constraints | Description |
|---|---|---|---|
| dataset_id | Integer | PK | Unique identifier |
| name | VARCHAR(150) | NOT NULL | Dataset name |
| description | TEXT | NULL | Description |
| schema_name | VARCHAR(100) | NOT NULL | Physical PostgreSQL schema |
| table_name | VARCHAR(100) | NOT NULL | Physical PostgreSQL table |
| data_type | VARCHAR(30) | NOT NULL | Dataset data type |
| geometry_type | VARCHAR(30) | NULL | Geometry type, if applicable |
| crs | VARCHAR(50) | NULL | Coordinate reference system |
| schema_id | Integer | FK, NULL | Associated logical schema version |
| status | VARCHAR(30) | NOT NULL | Dataset status |
| created_at | TIMESTAMPTZ | NOT NULL | Creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL | Last update timestamp |

### 2.3. `metadata.dataset_sources`

Stores information about the original sources of datasets.

| Field | Type | Constraints | Description |
|---|---|---|---|
| source_id | Integer | PK | Unique identifier |
| dataset_id | Integer | FK, NOT NULL | Associated dataset |
| source_name | VARCHAR(255) | NOT NULL | Source name |
| source_type | VARCHAR(50) | NOT NULL | Source type |
| source_format | VARCHAR(30) | NULL | Original data format |
| source_url | TEXT | NULL | Source URL |
| file_path | TEXT | NULL | Original file path |
| file_size | BIGINT | NULL | File size |
| file_hash | VARCHAR(64) | NULL | File hash |
| created_at | TIMESTAMPTZ | NOT NULL | Registration timestamp |

### 2.4. `metadata.ingestion_jobs`

Tracks ingestion and data management operations.

| Field | Type | Constraints | Description |
|---|---|---|---|
| job_id | Integer | PK | Unique process identifier |
| dataset_id | Integer | FK, NULL | Associated dataset |
| source_id | Integer | FK, NULL | Associated source |
| operation_type | VARCHAR(30) | NOT NULL | Operation type |
| status | VARCHAR(30) | NOT NULL | Process status |
| started_at | TIMESTAMPTZ | NOT NULL | Start timestamp |
| finished_at | TIMESTAMPTZ | NULL | Completion timestamp |
| records_detected | Integer | NULL | Detected records |
| records_inserted | Integer | NULL | Inserted records |
| records_updated | Integer | NULL | Updated records |
| records_deleted | Integer | NULL | Deleted records |
| records_rejected | Integer | NULL | Rejected records |
| error_message | TEXT | NULL | Error information |

### 2.5. `metadata.transformation_history`

Stores the transformations performed during ingestion processes.

| Field | Type | Constraints | Description |
|---|---|---|---|
| transformation_id | Integer | PK | Unique transformation identifier |
| job_id | Integer | FK, NOT NULL | Associated ingestion job |
| transformation_type | VARCHAR(100) | NOT NULL | Transformation type |
| description | TEXT | NULL | Transformation description |
| parameters | JSONB | NULL | Transformation parameters |
| status | VARCHAR(30) | NOT NULL | Transformation status |
| created_at | TIMESTAMPTZ | NOT NULL | Creation timestamp |

## 3. Relationships

- `dataset_schemas` 1:N `datasets`
- `datasets` 1:N `dataset_sources`
- `datasets` 1:N `ingestion_jobs`
- `dataset_sources` 1:N `ingestion_jobs`
- `ingestion_jobs` 1:N `transformation_history`

## 4. Design considerations

- Logical schema definitions are stored independently from physical PostgreSQL schemas.
- Each dataset references a specific logical schema version.
- Dataset records are stored in relational tables, rather than using a universal JSONB structure.
- JSONB is used for flexible schema definitions and additional metadata.
- The metadata model can evolve as new ingestion and data management requirements emerge.
- Physical dataset schemas and tables are managed dynamically by the application.

---

**Note:** This document describes the current implementation model. It is expected to evolve as the project develops.