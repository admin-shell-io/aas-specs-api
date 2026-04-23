#!/usr/bin/env node

/**
 * Simple test to validate the JSON Schema to OpenAPI conversion
 */

const { convertJsonSchemaToOpenAPI, convertSchemaToOpenAPI } = require('./json-schema-to-openapi.js');

console.log('Running conversion tests...\n');

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✓ ${name}`);
    passed++;
  } catch (error) {
    console.error(`✗ ${name}`);
    console.error(`  ${error.message}`);
    failed++;
  }
}

function assertEquals(actual, expected, message) {
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    throw new Error(`${message}\n  Expected: ${JSON.stringify(expected)}\n  Actual: ${JSON.stringify(actual)}`);
  }
}

// Test 1: Basic type conversion
test('converts simple type schema', () => {
  const input = { type: 'string', minLength: 1 };
  const output = convertSchemaToOpenAPI(input);
  assertEquals(output, { type: 'string', minLength: 1 }, 'Should preserve type and constraints');
});

// Test 2: Enum conversion
test('converts enum schema', () => {
  const input = { type: 'string', enum: ['A', 'B', 'C'] };
  const output = convertSchemaToOpenAPI(input);
  assertEquals(output, { type: 'string', enum: ['A', 'B', 'C'] }, 'Should preserve enum values');
});

// Test 3: $ref conversion
test('converts $ref from definitions to components/schemas', () => {
  const input = { $ref: '#/definitions/MyType' };
  const output = convertSchemaToOpenAPI(input);
  assertEquals(output, { $ref: '#/components/schemas/MyType' }, 'Should convert $ref path');
});

// Test 4: Object with properties
test('converts object with properties', () => {
  const input = {
    type: 'object',
    required: ['name'],
    properties: {
      name: { type: 'string' },
      age: { type: 'integer', minimum: 0 }
    }
  };
  const output = convertSchemaToOpenAPI(input);
  assertEquals(output.type, 'object', 'Should have type object');
  assertEquals(output.required, ['name'], 'Should preserve required');
  assertEquals(Object.keys(output.properties), ['name', 'age'], 'Should have all properties');
});

// Test 5: Array with items
test('converts array schema', () => {
  const input = {
    type: 'array',
    minItems: 1,
    items: { $ref: '#/definitions/Item' }
  };
  const output = convertSchemaToOpenAPI(input);
  assertEquals(output.type, 'array', 'Should have type array');
  assertEquals(output.minItems, 1, 'Should preserve minItems');
  assertEquals(output.items.$ref, '#/components/schemas/Item', 'Should convert items $ref');
});

// Test 6: allOf composition
test('converts allOf composition', () => {
  const input = {
    allOf: [
      { $ref: '#/definitions/Base' },
      { properties: { extra: { type: 'string' } } }
    ]
  };
  const output = convertSchemaToOpenAPI(input);
  assertEquals(output.allOf[0].$ref, '#/components/schemas/Base', 'Should convert allOf $ref');
  assertEquals(output.allOf.length, 2, 'Should preserve all allOf items');
});

// Test 7: Full JSON Schema to OpenAPI conversion
test('converts full JSON Schema document', () => {
  const input = {
    $schema: 'https://json-schema.org/draft/2019-09/schema',
    title: 'Test Schema',
    definitions: {
      Person: {
        type: 'object',
        properties: {
          name: { type: 'string' }
        }
      },
      Address: {
        type: 'object',
        properties: {
          street: { type: 'string' }
        }
      }
    }
  };
  const output = convertJsonSchemaToOpenAPI(input);
  assertEquals(output.openapi, '3.0.3', 'Should have OpenAPI version');
  assertEquals(Object.keys(output.components.schemas).length, 2, 'Should have 2 schemas');
  assertEquals(Object.keys(output.components.schemas), ['Person', 'Address'], 'Should have both definitions');
});

// Test 8: Pattern preservation
test('preserves regex patterns', () => {
  const input = {
    type: 'string',
    pattern: '^[a-zA-Z]+$'
  };
  const output = convertSchemaToOpenAPI(input);
  assertEquals(output.pattern, '^[a-zA-Z]+$', 'Should preserve pattern');
});

// Test 9: const to pattern conversion
test('converts const to pattern', () => {
  const input = {
    const: 'AnnotatedRelationshipElement'
  };
  const output = convertSchemaToOpenAPI(input);
  assertEquals(output.pattern, '^AnnotatedRelationshipElement$', 'Should convert const to exact match pattern');
});

// Test 10: const with special characters
test('converts const with special regex characters', () => {
  const input = {
    const: 'test.value$special'
  };
  const output = convertSchemaToOpenAPI(input);
  assertEquals(output.pattern, '^test\\.value\\$special$', 'Should escape special regex characters');
});

// Summary
console.log(`\n${'='.repeat(50)}`);
console.log(`Tests passed: ${passed}`);
console.log(`Tests failed: ${failed}`);
console.log(`${'='.repeat(50)}`);

if (failed > 0) {
  process.exit(1);
} else {
  console.log('\n✓ All tests passed!');
}
