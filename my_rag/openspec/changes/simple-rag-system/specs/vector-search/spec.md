## ADDED Requirements

### Requirement: Embed user queries
The system SHALL convert user queries into vector embeddings using the same model as document ingestion.

#### Scenario: Embed search query
- **WHEN** user submits a search query
- **THEN** system generates embedding using sentence-transformers all-MiniLM-L6-v2 model

#### Scenario: Handle empty query
- **WHEN** user submits an empty or whitespace-only query
- **THEN** system returns an error message requesting valid input

### Requirement: Perform similarity search
The system SHALL retrieve the most relevant document chunks based on semantic similarity.

#### Scenario: Retrieve top-k results
- **WHEN** user performs a search with k=5
- **THEN** system returns the 5 most similar document chunks based on cosine similarity

#### Scenario: Filter by similarity threshold
- **WHEN** system retrieves results
- **THEN** system only returns chunks with similarity score above 0.3

#### Scenario: No relevant results
- **WHEN** no chunks meet the similarity threshold
- **THEN** system returns empty results with appropriate message

### Requirement: Return results with metadata
The system SHALL provide search results with source information and relevance scores.

#### Scenario: Include source metadata
- **WHEN** system returns search results
- **THEN** each result includes chunk text, source file path, chunk index, and similarity score

#### Scenario: Sort by relevance
- **WHEN** system returns multiple results
- **THEN** results are sorted by similarity score in descending order

### Requirement: Support configurable retrieval parameters
The system SHALL allow users to configure search behavior.

#### Scenario: Configure number of results
- **WHEN** user specifies top-k parameter
- **THEN** system returns exactly k results (or fewer if insufficient matches)

#### Scenario: Configure similarity threshold
- **WHEN** user specifies minimum similarity threshold
- **THEN** system filters results below that threshold

### Requirement: Handle vector database queries efficiently
The system SHALL perform searches with minimal latency.

#### Scenario: Fast retrieval
- **WHEN** user performs a search on a database with 1000+ chunks
- **THEN** system returns results in under 1 second

#### Scenario: Handle concurrent queries
- **WHEN** multiple queries are submitted simultaneously
- **THEN** system processes them without blocking or errors
