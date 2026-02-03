

---

## Top-Level Repository Structure

```
automation-reverse-engineering/
├── README.md
├── pyproject.toml                 # or package.json / pom.xml
├── requirements.txt
├── .gitignore
├── .env.example
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── docs/
│   ├── architecture/
│   │   ├── logical-architecture.md
│   │   ├── logical-architecture.mmd
│   │   └── c4-diagrams/
│   ├── onboarding.md
│   └── faq.md
├── scripts/
│   └── run_pipeline.sh
├── src/
│   ├── ingestion/
│   ├── static_analysis/
│   ├── semantic_analysis/
│   ├── test_generation/
│   ├── knowledge_base/
│   ├── traceability/
│   ├── output/
│   └── common/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── ci/
    ├── github-actions.yml
    └── jenkinsfile
```

---

## Detailed Mapping to Logical Architecture

### 1. Code Ingestion & Normalization

```
src/ingestion/
├── __init__.py
├── repository_scanner.py
├── language_detection.py
├── code_normalizer.py
├── dependency_resolution.py
└── ingestion_pipeline.py
```

**Maps to**

* Repository Scanner
* Language Detection
* Code Normalization
* Dependency Resolution

---

### 2. Static Analysis Engine

```
src/static_analysis/
├── __init__.py
├── ast/
│   ├── ast_parser.py
│   └── ast_model.py
├── cfg/
│   ├── cfg_builder.py
│   └── cfg_model.py
├── dfg/
│   ├── dfg_builder.py
│   └── dfg_model.py
├── call_graph/
│   ├── call_graph_builder.py
│   └── call_graph_model.py
├── dependency_graph/
│   ├── dependency_graph_builder.py
│   └── dependency_graph_model.py
└── static_analysis_pipeline.py
```

**Maps to**

* AST Parser
* Control Flow Graph
* Data Flow Graph
* Call Graph
* Dependency Graph

---

### 3. Semantic Understanding Layer

```
src/semantic_analysis/
├── __init__.py
├── code_summarization.py
├── intent_behavior_mining.py
├── automation_pattern_detection.py
├── business_logic_inference.py
├── semantic_model.py
└── semantic_pipeline.py
```

**Maps to**

* Code Summarization
* Intent & Behavior Mining
* Automation Pattern Identification
* Business Logic Inference

---

### 4. Test Case Generator

```
src/test_generation/
├── __init__.py
├── test_strategy.py
├── unit/
│   ├── unit_test_generator.py
│   └── unit_templates/
├── integration/
│   ├── integration_test_generator.py
│   └── integration_templates/
├── e2e/
│   ├── e2e_test_generator.py
│   └── e2e_templates/
├── edge_cases/
│   └── edge_case_generator.py
└── test_generation_pipeline.py
```

**Maps to**

* Unit Tests
* Integration Tests
* End-to-End Tests
* Edge and Negative Cases

---

### 5. Knowledge Base Builder

```
src/knowledge_base/
├── __init__.py
├── documentation_generator.py
├── flow_explanation_generator.py
├── faq_generator.py
├── kb_templates/
└── kb_pipeline.py
```

**Maps to**

* Code Documentation
* Flow and Architecture Explanation
* FAQ Generator

---

### 6. Traceability & Metadata Store

```
src/traceability/
├── __init__.py
├── metadata_models.py
├── code_to_test_mapper.py
├── code_to_kb_mapper.py
├── versioning.py
├── impact_analysis.py
└── traceability_service.py
```

**Maps to**

* Traceability
* Versioning
* Change Impact Analysis

---

### 7. Output & Consumption Layer

```
src/output/
├── __init__.py
├── ci_integration.py
├── test_framework_exporter.py
├── kb_publisher.py
├── export_formats/
│   ├── markdown_exporter.py
│   ├── html_exporter.py
│   └── pdf_exporter.py
└── output_pipeline.py
```

**Maps to**

* CI CD Integration
* Test Frameworks
* Knowledge Base Portal
* Export Artifacts

---

### 8. Shared Utilities

```
src/common/
├── __init__.py
├── config.py
├── logging.py
├── file_utils.py
├── graph_utils.py
└── llm_client.py
```

---

## Orchestration Entry Point

```
src/main.py
```

```text
main.py
 └── ingestion
      └── static_analysis
           └── semantic_analysis
                └── test_generation
                     └── knowledge_base
                          └── traceability
                               └── output
```

---

## Why This Structure Works

* **Direct traceability** from architecture → code
* Easy to:

  * Swap languages or frameworks
  * Add new analysis stages
* CI-friendly and testable
* Scales to enterprise-grade tooling

---

