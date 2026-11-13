# Pydantic schemas

## 1. Purpose

The `app/schemas/` package defines the data contracts used by the GeoData Intelligence API and validates the information that enters and leaves the application.

These classes are **Pydantic models**, not database tables. They are separate from the SQLAlchemy models in `app/models/`:

- **Pydantic (`app/schemas/`)**: validates incoming data and structures API responses.
- **SQLAlchemy (`app/models/`)**: represents database tables, columns and relationships.
- **Services (`app/services/`)**: implement application operations, using validated Pydantic data and SQLAlchemy models.

The logical dataset definition is particularly important: it describes the attributes and optional spatial component that a dataset is expected to contain. It is later stored in `metadata.dataset_schemas.definition` as JSONB.

## 2. Logical dataset definition

The definition is composed of three nested models, currently located in `app/schemas/dataset_definition.py`.

### 2.1. `FieldDefinition`

Describes one non-spatial attribute in a logical dataset schema.

| Property | Type | Meaning |
|---|---|---|
| `name` | `str` | Attribute name. Between 1 and 100 characters. |
| `type` | `Literal[...]` | Data type: `integer`, `float`, `string`, `boolean`, `date` or `datetime`. |
| `description` | `str \| None` | Optional explanation of the attribute. |
| `required` | `bool` | Indicates whether the attribute is required. Defaults to `False`. |

**Name validation**

The `name` validator:

1. Removes leading and trailing whitespace.
2. Converts the name to lowercase.
3. Allows letters, numbers and underscores.
4. Rejects names that begin with a number.
5. Rejects an empty name.

The model uses `ConfigDict(extra="forbid")`, so additional properties not declared in the model are rejected.

Example:

```python
FieldDefinition(
    name="station_id",
    type="integer",
    description="Identifier of the monitoring station",
    required=True
)
```

### 2.2. `GeometryDefinition`

Describes the spatial component of a dataset.

| Property | Type | Meaning |
|---|---|---|
| `type` | `Literal[...]` | Geometry type. |
| `crs` | `str` | Coordinate Reference System identifier. Between 1 and 50 characters. |
| `nullable` | `bool` | Indicates whether geometry can be absent. Defaults to `False`. |

Supported geometry types:

- `Point`
- `MultiPoint`
- `LineString`
- `MultiLineString`
- `Polygon`
- `MultiPolygon`

Example:

```python
GeometryDefinition(
    type="Point",
    crs="EPSG:25831",
    nullable=False
)
```

The CRS is currently represented as a string. Its semantic validity (for example, whether the identifier corresponds to a CRS supported by the platform) must be checked by the relevant application or processing logic; this Pydantic model only validates that a non-empty string is supplied.

### 2.3. `DatasetDefinition`

Represents the complete logical structure of a dataset.

| Property | Type | Meaning |
|---|---|---|
| `fields` | `list[FieldDefinition]` | List of non-spatial attributes. Defaults to an empty list. |
| `geometry` | `GeometryDefinition \| None` | Optional spatial definition. Defaults to `None`. |

The model validates that field names are unique after normalization. For example, `Station_ID` and `station_id` are treated as duplicates because field names are normalized to lowercase.

A dataset is therefore not required to contain geometry. This supports both spatial and non-spatial datasets.

Example:

```python
DatasetDefinition(
    fields=[
        FieldDefinition(
            name="station_id",
            type="integer",
            required=True
        ),
        FieldDefinition(
            name="water_level",
            type="float",
            description="Measured water level",
            required=True
        )
    ],
    geometry=None
)
```

As with the nested models, undeclared additional properties are forbidden.

## 3. Dataset schema API models

The models in `app/schemas/dataset_schema.py` define the payloads used to create, update and return logical schema records.

### 3.1. `DatasetSchemaCreate`

Input model for creating the first version of a logical schema.

| Property | Type | Meaning |
|---|---|---|
| `name` | `str` | Logical schema name. |
| `description` | `str \| None` | Optional description. |
| `definition` | `DatasetDefinition` | Validated logical structure. |

The service assigns the initial version (`1`) and generates the `schema_code`; clients should not provide either value.

### 3.2. `DatasetSchemaVersionCreate`

Input model intended for creating a subsequent version of an existing logical schema.

It contains:

| Property | Type | Meaning |
|---|---|---|
| `description` | `str \| None` | Optional description for the new version. |
| `definition` | `DatasetDefinition` | Logical structure of the new version. |

The version number and code must be assigned by the service, not supplied by the client. The operation must preserve the identity of the schema family (`name`) while creating a new version record.

> Implementation note: the model defines the input contract. The creation and validation workflow for subsequent versions must be considered implemented only once the corresponding service operation is available and tested.

### 3.3. `DatasetSchemaUpdate`

Input model for updating the descriptive metadata of an existing schema.

```python
class DatasetSchemaUpdate(BaseModel):
    description: str | None = None
```

This model deliberately exposes only `description`. It does **not** allow changing:

- `schema_id`
- `schema_code`
- `name`
- `version`
- `definition`

The distinction between an omitted field and an explicit `null` is relevant. The service checks `model_fields_set` to determine whether `description` was actually included in the request. Therefore:

- `{}` means that no update field was supplied.
- `{"description": null}` means that the description was explicitly set to `NULL`.
- `{"description": "New description"}` changes the description.

This keeps logical structure and identity separate from descriptive metadata.

### 3.4. `DatasetSchemaResponse`

Response model for returning a logical schema to API clients.

It exposes the schema identifier, code, name, description, version, definition and creation timestamp:

| Property | Meaning |
|---|---|
| `schema_id` | Internal database identifier. |
| `schema_code` | Unique human-readable schema code. |
| `name` | Logical schema family/name. |
| `description` | Optional descriptive text. |
| `version` | Version number of the logical definition. |
| `definition` | Validated logical structure (`DatasetDefinition`). |
| `created_at` | Creation timestamp. |

The model uses `ConfigDict(from_attributes=True)` so it can be populated from SQLAlchemy ORM objects.

## 4. Validation boundaries

Validation is performed at more than one level:

1. **Pydantic validation** checks the structure and types of the request, allowed values, field naming rules and duplicate field names.
2. **Service validation** checks business rules that depend on the database or the operation, such as whether a schema name already exists or whether an update target can be identified.
3. **Database constraints** enforce persistence-level rules such as primary keys and uniqueness.

These layers have different responsibilities. Passing Pydantic validation does not automatically mean that a request is valid for the current database state or safe to execute as a physical data transformation.

## 5. Relationship with PostgreSQL

A `DatasetDefinition` is serialized to a JSON-compatible dictionary and stored in:

```text
metadata.dataset_schemas.definition
```

The column uses PostgreSQL `JSONB`. It stores the **logical description** of the dataset structure; it is not the physical storage of the dataset's records.

The actual records are stored separately in the physical dataset table. A dataset references the exact logical schema version it follows through its `schema_id` foreign key.

For the database entities and relationships, see [`data_model.md`](data_model.md). For version creation, immutability and dataset migration policy, see [`dataset_versioning.md`](dataset_versioning.md).

## 6. Design principles

- Keep API contracts separate from SQLAlchemy persistence models.
- Validate and normalize field names consistently.
- Allow non-spatial datasets by making geometry optional.
- Keep the logical definition explicit and structured rather than accepting arbitrary unvalidated properties.
- Do not let update payloads mutate schema identity or its versioned definition.
- Keep database-dependent rules in services and persistence constraints in PostgreSQL.
