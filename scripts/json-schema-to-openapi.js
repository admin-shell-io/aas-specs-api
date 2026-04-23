#!/usr/bin/env node

/**
 * Converts JSON Schema definitions to OpenAPI 3.0 YAML format
 * Usage: node json-schema-to-openapi.js <input.json> <output.yaml>
 */

const fs = require('fs');
const path = require('path');
const yaml = require('yaml');

/**
 * Converts a JSON Schema definition to OpenAPI schema format
 */
function convertSchemaToOpenAPI(schema) {
  if (!schema || typeof schema !== 'object') {
    return schema;
  }

  const result = {};

  // Handle JSON Schema 'const' keyword (not supported in OpenAPI 3.0)
  // Convert to pattern that matches exactly that value
  if ('const' in schema) {
    const constValue = schema.const;
    // Escape special regex characters and create exact match pattern
    const escapedValue = String(constValue).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    result.pattern = `^${escapedValue}$`;
  }

  // Copy basic JSON Schema properties that are valid in OpenAPI
  const directCopyProps = [
    'type', 'enum', 'format', 'pattern', 'minLength', 'maxLength',
    'minimum', 'maximum', 'exclusiveMinimum', 'exclusiveMaximum',
    'multipleOf', 'minItems', 'maxItems', 'uniqueItems',
    'minProperties', 'maxProperties', 'required', 'description',
    'default', 'example', 'deprecated', 'readOnly', 'writeOnly',
    'title', 'additionalProperties'
  ];

  for (const prop of directCopyProps) {
    if (prop in schema) {
      // Don't overwrite pattern if it was set from 'const'
      if (prop === 'pattern' && result.pattern) {
        continue;
      }
      result[prop] = schema[prop];
    }
  }

  // Handle properties
  if (schema.properties) {
    result.properties = {};
    for (const [key, value] of Object.entries(schema.properties)) {
      result.properties[key] = convertSchemaToOpenAPI(value);
    }
  }

  // Handle items (for arrays)
  if (schema.items) {
    result.items = convertSchemaToOpenAPI(schema.items);
  }

  // Handle oneOf, anyOf, allOf
  for (const combinator of ['oneOf', 'anyOf', 'allOf']) {
    if (schema[combinator]) {
      result[combinator] = schema[combinator].map(s => convertSchemaToOpenAPI(s));
    }
  }

  // Handle $ref - convert from JSON Schema definitions to OpenAPI components
  if (schema.$ref) {
    // Convert #/definitions/Name to #/components/schemas/Name
    result.$ref = schema.$ref.replace('#/definitions/', '#/components/schemas/');
  }

  // Handle discriminator (if present)
  if (schema.discriminator) {
    result.discriminator = schema.discriminator;
  }

  // Handle nullable (OpenAPI 3.0 specific)
  if (schema.nullable !== undefined) {
    result.nullable = schema.nullable;
  }

  return result;
}

/**
 * Main conversion function
 */
function convertJsonSchemaToOpenAPI(jsonSchema) {
  // Extract metadata from the JSON schema
  const title = jsonSchema.title || 'API Schema';
  const schemaId = jsonSchema.$id || '';

  // Initialize OpenAPI document structure
  const openApiDoc = {
    openapi: '3.0.3',
    info: {
      title: title,
      description: `The schemas implementing the Asset Administration Shell specification.\n\nCopyright: Industrial Digital Twin Association (IDTA) 2025`,
      contact: {
        name: 'Industrial Digital Twin Association (IDTA)',
        email: 'info@idtwin.org'
      },
      license: {
        name: 'CC BY 4.0',
        url: 'https://creativecommons.org/licenses/by/4.0/'
      },
      version: 'V3.2.0'
    },
    components: {
      schemas: {}
    }
  };

  // Convert all definitions to OpenAPI schemas
  if (jsonSchema.definitions) {
    for (const [name, definition] of Object.entries(jsonSchema.definitions)) {
      openApiDoc.components.schemas[name] = convertSchemaToOpenAPI(definition);
    }
  }

  return openApiDoc;
}

/**
 * CLI entry point
 */
function main() {
  const args = process.argv.slice(2);

  if (args.length < 2) {
    console.error('Usage: node json-schema-to-openapi.js <input.json> <output.yaml>');
    process.exit(1);
  }

  const inputPath = path.resolve(args[0]);
  const outputPath = path.resolve(args[1]);

  console.log(`Reading JSON Schema from: ${inputPath}`);

  // Read input JSON schema
  let jsonSchema;
  try {
    const inputContent = fs.readFileSync(inputPath, 'utf8');
    jsonSchema = JSON.parse(inputContent);
  } catch (error) {
    console.error(`Error reading or parsing input file: ${error.message}`);
    process.exit(1);
  }

  console.log(`Converting ${Object.keys(jsonSchema.definitions || {}).length} definitions...`);

  // Convert to OpenAPI
  const openApiDoc = convertJsonSchemaToOpenAPI(jsonSchema);

  console.log(`Writing OpenAPI YAML to: ${outputPath}`);

  // Write output as YAML
  try {
    const yamlContent = yaml.stringify(openApiDoc, {
      lineWidth: 0, // Don't wrap lines
      indent: 2,
      defaultStringType: 'PLAIN',
      defaultKeyType: 'PLAIN'
    });
    fs.writeFileSync(outputPath, yamlContent, 'utf8');
  } catch (error) {
    console.error(`Error writing output file: ${error.message}`);
    process.exit(1);
  }

  console.log(`✓ Successfully converted to OpenAPI format`);
  console.log(`  - Schemas: ${Object.keys(openApiDoc.components.schemas).length}`);
}

// Run if called directly
if (require.main === module) {
  main();
}

module.exports = { convertJsonSchemaToOpenAPI, convertSchemaToOpenAPI };
