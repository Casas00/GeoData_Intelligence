# GeoData Intelligence

**AI-Assisted Geospatial Data Harmonization Platform**

Plataforma para la interpretación, normalización e integración de datos geoespaciales heterogéneos mediante procesos ETL asistidos por inteligencia artificial.

---

## 1. Overview

GeoData Intelligence is a modular platform designed to simplify the integration and management of heterogeneous geospatial datasets.

The platform receives datasets from different sources and formats, automatically inspects their structure, and uses AI-assisted interpretation to propose mappings, target schemas and data transformations.

After human review and deterministic validation, approved transformations are executed and the resulting datasets are stored in PostgreSQL/PostGIS, becoming available through a REST API.

The project combines conventional geospatial data processing with local AI inference to reduce the manual effort required to harmonize datasets from different sources.

## 2. Problem Statement

Geospatial information is commonly produced by different organizations, providers, sensors and platforms.

Even when datasets represent similar phenomena, they may differ in:

- Attribute structures and column names.
- Data types and naming conventions.
- Coordinate reference systems (CRS).
- Geometric representations.
- Units of measurement.
- Record identification systems.

These inconsistencies make data integration and joint exploitation difficult.

GeoData Intelligence aims to reduce this complexity through automated inspection, AI-assisted interpretation and configurable data normalization.

## 3. Main Objectives

- Develop a modular REST API for dataset management and consultation.
- Implement automatic inspection of tabular and geospatial files.
- Integrate local language models to interpret unknown data structures.
- Propose field mappings and configurable target schemas.
- Implement human review and approval of transformation proposals.
- Develop deterministic ETL processes for data validation and normalization.
- Store datasets in PostgreSQL/PostGIS using independent thematic tables.
- Maintain traceability of ingestion, transformation and update operations.
- Provide endpoints for dataset exploration, filtering and retrieval.

## 4. Core Workflow

The platform follows a controlled ingestion and harmonization workflow:

1. **Data ingestion:** The user uploads a supported file.
2. **Automatic inspection:** The system identifies its format, attributes, data types, geometries and available metadata.
3. **AI-assisted interpretation:** A local language model proposes a target schema, field mappings and potential transformations.
4. **Human review:** The user examines, modifies, approves or rejects the proposal.
5. **Validation and transformation:** Deterministic rules validate the approved plan and execute the corresponding ETL operations.
6. **Storage:** The resulting dataset is created or updated in PostgreSQL/PostGIS, together with its metadata.
7. **Publication and exploration:** The dataset becomes available through the REST API for querying, filtering and spatial analysis.

AI is used as an interpretation and recommendation component. Data validation and execution remain under the control of conventional application logic.

## 5. Data Management Architecture

### Flexible thematic schemas

Datasets will be organized using configurable thematic schemas rather than a single universal data model.

For example, meteorological stations and road networks will retain their own specific attributes while following common conventions where applicable.

Common conventions may include:

- Internal identifiers.
- Original source identifiers, when available.
- Normalized attribute names.
- Consistent data types.
- Geometry and CRS definitions, when applicable.
- Source and processing metadata.

Each dataset can therefore retain its own relational structure while benefiting from a consistent management framework.

### PostgreSQL/PostGIS organization

The planned database organization separates internal platform metadata from thematic datasets.

```text
geodata_intelligence/
│
├── metadata/
│   ├── datasets
│   ├── ingestion_jobs
│   ├── dataset_schemas
│   └── transformation_history
│
├── meteorology/
│   ├── weather_stations
│   └── weather_observations
│
├── transport/
│   ├── roads
│   └── railways
│
└── administration/
    ├── municipalities
    └── provinces
```

The metadata schema will act as the platform's internal control layer, maintaining information about registered datasets, their physical storage locations, schemas and ingestion history.

### Dataset updates

The platform will identify whether an incoming file corresponds to an existing dataset.

Depending on the dataset structure and available identifiers, the user will be able to incorporate new records, update existing ones or replace the stored content.

This allows datasets to evolve through successive ingestion operations without creating a new database table for every uploaded file.

## 6. AI Integration

The initial AI integration will use Ollama to run a language model locally.

The application will communicate with the local model through its HTTP API, sending dataset inspection information and receiving structured interpretation proposals.

The model will be used to:

- Identify potential dataset categories.
- Suggest correspondences between source and target attributes.
- Recommend thematic schemas.
- Identify potential transformations.
- Report uncertainties and possible inconsistencies.

The initial implementation will explore relatively small models from the Qwen or Gemma families, depending on available hardware.

AI proposals will always be validated by deterministic application rules and reviewed by the user before execution.

## 7. Technology Stack

| Area | Technology | Purpose |
|---|---|---|
| Backend | Python, FastAPI | REST API |
| Data validation | Pydantic | Request and response validation |
| Database | PostgreSQL, PostGIS | Relational and spatial storage |
| Database access | SQLAlchemy | Database interaction |
| Local AI | Ollama, LLM | Dataset interpretation |
| Vector processing | GeoPandas, Shapely | Reading and transforming vector data |
| CRS management | PyProj | Coordinate transformations |
| Raster processing | Rasterio, GDAL | Future raster support |
| Testing | Pytest | Automated testing |
| Environment | Docker | Reproducible deployment |
| API documentation | OpenAPI / Swagger | API documentation |

Technology choices may evolve as the implementation progresses.

## 8. Development Roadmap

| Phase | Description |
|---|---|
| 1. Architecture | Define the system architecture, data model and ingestion workflow. |
| 2. Core Backend | Implement FastAPI, database connectivity and initial management endpoints. |
| 3. Data Inspection | Implement file reception, format detection and automatic inspection. |
| 4. AI Integration | Connect Ollama and develop structured interpretation proposals. |
| 5. Validation and Normalization | Implement schemas, review mechanisms and transformation rules. |
| 6. Storage and ETL | Create and update database tables and register processing history. |
| 7. Data Exploration | Implement dataset queries, attribute filters and spatial operations. |
| 8. Consolidation | Add automated tests, security, Docker, documentation and deployment support. |

## 9. Testing Strategy

The initial development will use synthetic datasets to control test conditions and avoid unnecessary dependencies on external data licences.

These datasets will include deliberately introduced inconsistencies, such as:

- Different column names representing equivalent attributes.
- Missing values.
- Incorrect or missing coordinates.
- Different coordinate reference systems.
- Inconsistent data types.
- Duplicate records.

This will allow the inspection, interpretation and normalization components to be evaluated against known expected results.

## 10. Project Structure

The backend will follow a modular monolithic architecture, separating API endpoints, business logic, data access, ingestion and processing components.

The application structure will evolve as new capabilities are implemented.

## 11. Project Status

**Initial development phase.**

The project architecture and main functional requirements have been defined. The initial FastAPI application and Python development environment are operational.

Further development will progressively introduce database integration, data inspection, AI-assisted interpretation and ETL capabilities.

---

*GeoData Intelligence — AI-Assisted Geospatial Data Harmonization Platform*