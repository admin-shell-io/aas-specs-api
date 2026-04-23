# JSON Schema to OpenAPI Converter

This script converts JSON Schema definitions from `aas.json` into OpenAPI 3.0 YAML format in `openapi.yaml`.

## Usage

### Quick Start

Run the conversion using npm script:

```bash
npm run convert-schema
```

### Manual Usage

You can also run the script directly:

```bash
node scripts/json-schema-to-openapi.js <input.json> <output.yaml>
```

Example:
```bash
node scripts/json-schema-to-openapi.js Part1-MetaModel-Schemas/aas.json Part1-MetaModel-Schemas/openapi.yaml
```

## What It Does

The script:

1. **Reads** the JSON Schema file (`aas.json`)
2. **Converts** all definitions to OpenAPI 3.0 schema format:
   - Translates `#/definitions/` references to `#/components/schemas/`
   - Preserves all schema properties (type, enum, pattern, required, etc.)
   - Handles complex schemas (allOf, oneOf, anyOf)
   - Maintains nested properties and array items
3. **Generates** a complete OpenAPI document with:
   - OpenAPI 3.0.3 metadata
   - IDTA info and licensing
   - All schemas under `components.schemas`
4. **Writes** the output as formatted YAML

## Features

- ✅ Preserves all JSON Schema constraints
- ✅ Converts schema references properly
- ✅ Handles complex compositions (allOf, oneOf, anyOf)
- ✅ Maintains patterns, enums, and validation rules
- ✅ Formats output as readable YAML
- ✅ Supports all 70 AAS metamodel definitions

## Requirements

- Node.js 14+
- Dependencies: `yaml` (installed via npm install)

## Output

The script generates `openapi.yaml` with:
- OpenAPI version: 3.0.3
- 70 schema definitions under `components.schemas`
- All references converted to OpenAPI format

## Development

The script is modular and exports functions for use in other tools:
- `convertJsonSchemaToOpenAPI(jsonSchema)` - Main conversion function
- `convertSchemaToOpenAPI(schema)` - Schema-level converter
