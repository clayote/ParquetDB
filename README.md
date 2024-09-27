# ParquetDB

ParquetDB is a lightweight database-like system built on top of Apache Parquet files using PyArrow. It offers a simple and efficient way to store, manage, and retrieve complex data types without the overhead of serialization, which is often a bottleneck in machine learning pipelines. By leveraging Parquet's columnar storage format and PyArrow's computational capabilities, ParquetDB provides high performance for data-intensive applications. 


## Table of Contents

- [Features](#features)
- [Why ParquetDB?](#why-parquetdb)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Creating a Database](#creating-a-database)
  - [Adding Data](#adding-data)
  - [Reading Data](#reading-data)
  - [Updating Data](#updating-data)
  - [Deleting Data](#deleting-data)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Simple Interface**: Easy-to-use methods for creating, reading, updating, and deleting data.
- **High Performance**: Utilizes Apache Parquet and PyArrow for efficient data storage and retrieval.
- **Supports Complex Data Types**: Handles nested and complex data types without serialization overhead.
- **Scalable**: Designed to handle large datasets efficiently.
- **Schema Evolution**: Supports adding new fields and updating schemas seamlessly.

## Roadmap

- Support foriegn keys use
- Multiprocessing for reading and writing

## Why ParquetDB?

### The Challenge of Serialization and Deserialization

In many data processing and machine learning workflows, a significant performance bottleneck occurs during the serialization and deserialization of data. Serialization is the process of converting complex data structures or objects into a format that can be easily stored or transmitted, while deserialization is the reverse process of reconstructing these objects from the serialized format.

The need for serialization arises when:
1. Storing data on disk
2. Transmitting data over a network
3. Caching data in memory

However, serialization and deserialization can be computationally expensive, especially when dealing with large datasets or complex object structures. This process can lead to:

- Increased I/O operations
- Higher CPU usage
- Increased memory consumption
- Longer processing times

These issues become particularly problematic in machine learning pipelines, where data needs to be frequently loaded, processed, and saved. The overhead of constantly serializing and deserializing data can significantly slow down the entire workflow, affecting both development iteration speed and production performance.

### How Parquet Files Address the Serialization Challenge

Apache Parquet files offer a solution to the serialization/deserialization problem by providing:

1. **Columnar Storage Format**: Parquet stores data in a columnar format, which allows for efficient compression and encoding schemes. This format is particularly beneficial for analytical queries that typically involve a subset of columns.
2. **Schema Preservation**: Parquet files store the schema of the data along with the data itself. This eliminates the need for separate schema definitions and reduces the risk of schema mismatch errors.
3. **Efficient Encoding**: Parquet uses advanced encoding techniques like dictionary encoding, bit packing, and run length encoding, which can significantly reduce file sizes and improve read performance.
4. **Predicate Pushdown**: Parquet supports predicate pushdown, allowing queries to skip irrelevant data blocks entirely, further improving query performance.
5. **Compatibility**: Parquet files are compatible with various big data processing frameworks, making it easier to integrate into existing data pipelines.

By leveraging these features, ParquetDB eliminates the need for explicit serialization and deserialization of complex data types. Data can be read directly from and written directly to Parquet files, maintaining its structure and allowing for efficient querying and processing.

### The ParquetDB Advantage

ParquetDB builds upon the benefits of Parquet files by providing:

1. A simple, database-like interface for working with Parquet files
2. Efficient storage and retrieval of complex data types
3. High-performance data operations leveraging PyArrow's computational capabilities
4. Seamless integration with machine learning pipelines and data processing workflows

By using ParquetDB, developers and data scientists can focus on their core tasks without worrying about the intricacies of data serialization or the performance implications of frequent I/O operations. This results in faster development cycles, improved system performance, and more efficient use of computational resources.


## Installation

Install ParquetDB using pip:

```bash
pip install parquetdb
```

## Quick Start

```python
from parquetdb import ParquetDB

# Initialize the database
db = ParquetDB('path/to/db')

# Create data
data = [
    {'name': 'Alice', 'age': 30, 'occupation': 'Engineer'},
    {'name': 'Bob', 'age': 25, 'occupation': 'Data Scientist'}
]

# Add data to the database
db.create(data, table_name='employees')

# Read data from the database
employees = db.read(table_name='employees')
print(employees.to_pandas())
```

## Usage

### Creating a Database

Initialize a ParquetDB instance by specifying the path to the database directory:

```python
from parquetdb import ParquetDB

db = ParquetDB('path/to/db')
```

### Adding Data

Add data to the database using the `create` method. Data can be a dictionary, a list of dictionaries, or a Pandas DataFrame.

```python
data = [
    {'name': 'Charlie', 'age': 28, 'occupation': 'Designer'},
    {'name': 'Diana', 'age': 32, 'occupation': 'Product Manager'}
]

db.create(data, table_name='employees')
```

### Reading Data

Read data from the database using the `read` method. You can filter data by IDs, specify columns, and apply filters.

```python
# Read all data
all_employees = db.read(table_name='employees')

# Read specific columns
names = db.read(table_name='employees', columns=['name'])

# Read data with filters
from pyarrow import compute as pc

age_filter = pc.field('age') > 30
older_employees = db.read(table_name='employees', filters=[age_filter])
```

### Updating Data

Update existing records in the database using the `update` method. Each record must include the `id` field.

```python
update_data = [
    {'id': 1, 'occupation': 'Senior Engineer'},
    {'id': 3, 'age': 29}
]

db.update(update_data, table_name='employees')
```

### Deleting Data

Delete records from the database by specifying their IDs.

```python
db.delete(ids=[2, 4], table_name='employees')
```


## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

*Note: This project is in its initial stages. Features and APIs are subject to change. Please refer to the latest documentation and release notes for updates.*