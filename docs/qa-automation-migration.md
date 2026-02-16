

Below is a **production-grade Migration Execution Pipeline Blueprint** for converting one QA automation framework to another (e.g., Selenium → Playwright / UiPath) using the **Modular IR architecture** we defined.

This is designed for:

* 1000+ tests
* Parallel processing
* Incremental regeneration
* Enterprise CI/CD integration
* Traceability & rollback

---

# 1️⃣ High-Level Pipeline Architecture

```
                ┌─────────────────────────┐
                │  Source Repo (Selenium) │
                └─────────────┬───────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Source Parser  │
                    │  (AST Builder)  │
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │  IR Generator   │
                    │  (Modular JSON) │
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │ IR Validator    │
                    │ (Schema + Ref)  │
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │ Optimization    │
                    │ Engine (AI/Rules)│
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │ Target Generator│
                    │ (Playwright /   │
                    │  UiPath)        │
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │ Build & Compile │
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │ Test Execution  │
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │ Report & Diff   │
                    └─────────────────┘
```

---

# 2️⃣ Pipeline Stages (Detailed)

---

# Stage 1 — Source Inventory & Analysis

### Goal:

Understand scope before migration.

### Actions:

* Count test classes
* Identify POM usage
* Identify custom wrappers
* Detect anti-patterns (Thread.sleep, hardcoded waits)
* Identify data providers
* Identify parallel config

### Output:

`migration_inventory.json`

---

# Stage 2 — AST Parsing

### Goal:

Convert Selenium code into structured AST.

### Tools:

* JavaParser (Java)
* Python AST
* Roslyn (C#)

### Extract:

* Test methods
* Page objects
* Locators
* Wait strategies
* Assertions
* Data providers

Output:

```
semantic_model/
```

---

# Stage 3 — IR Generation (Modular)

For each test:

```
tests/TC_*.json
```

For each page:

```
targets.json
```

For each dataset:

```
data/*.json
```

### Critical:

* Compute checksum for each source test
* Store in IR:

```json
"sourceChecksum": "sha256-abc123"
```

---

# Stage 4 — IR Validation Layer

Validate:

✔ JSON Schema compliance
✔ targetId existence
✔ dataSetId existence
✔ orphan references
✔ duplicate targets
✔ circular dependencies

Fail fast if invalid.

---

# Stage 5 — Optimization Engine (Optional but Recommended)

### Rule-based + AI-driven improvements:

* Remove redundant waits
* Convert XPath → CSS
* Suggest Playwright role locators
* Detect flaky patterns
* Improve selector stability score
* Deduplicate targets

Produces:

```
optimized_ir/
```

---

# Stage 6 — Incremental Regeneration Logic

Before generating target code:

For each test:

```
if sourceChecksum unchanged
    skip generation
else
    regenerate
```

Benefits:

* Fast CI
* Efficient partial rollouts
* Safe rollback

---

# Stage 7 — Target Framework Generator

### Generator types:

| Target     | Generator Output |
| ---------- | ---------------- |
| Playwright | .spec.ts files   |
| UiPath     | .xaml workflows  |
| Cypress    | .cy.ts files     |

### Strategy Selection Algorithm:

For each step:

```
1. Read targetId
2. Resolve preferredStrategy
3. Check framework compatibility
4. If unsupported → fallback
5. Apply template
```

Example:

```typescript
await page.locator('#login-btn').click();
```

---

# Stage 8 — Build & Compile

### Playwright:

* npm install
* TypeScript compile
* Lint
* Static analysis

### UiPath:

* Validate XAML
* Package project

Fail build if:

* Syntax error
* Missing imports
* Broken references

---

# Stage 9 — Parallel Test Execution

Shard execution:

```
CI Node 1 → AUTH_SUITE
CI Node 2 → ORDER_SUITE
CI Node 3 → PAYMENT_SUITE
```

Or:

```
Split by test files
```

---

# Stage 10 — Validation & Behavior Comparison

Compare:

| Metric         | Selenium | Target |
| -------------- | -------- | ------ |
| Pass Rate      | 95%      | ?      |
| Execution Time | 20m      | ?      |
| Flaky Count    | 5        | ?      |

Optional:

* Screenshot diff
* DOM snapshot comparison
* API response diff

---

# Stage 11 — Reporting & Traceability

Generate:

* Migration coverage report
* Confidence score per test
* Risk classification
* Skipped tests
* Failed conversions

---

# 3️⃣ Enterprise-Grade CI/CD Blueprint

## Git-Based Flow

```
feature/migration-batch-1
      ↓
Auto-generate PR
      ↓
Code review
      ↓
Merge
      ↓
Nightly validation run
```

---

# 4️⃣ Parallelization Strategy (Large Scale)

If 1000 tests:

```
Split IR into 10 batches
Each batch processed independently
```

Use:

* Worker pool
* Message queue
* Distributed runners

Architecture:

```
IR Queue → Worker Nodes → Generator → Result Store
```

---

# 5️⃣ Rollback Strategy

Never overwrite source.

Maintain:

```
/selenium-original/
/playwright-migrated/
```

If regression detected:

* Revert branch
* Disable suite
* Roll back by batch

---

# 6️⃣ Observability Layer

Log at each stage:

* Parsing time
* Generation time
* Test duration
* Failure cause classification

Persist:

```
migration_metrics.db
```

Track:

* Flakiness delta
* Stability improvement
* Speed improvement

---

# 7️⃣ Security & Governance Controls

* Approval gate before merge
* Risk-level tagging
* Manual review required for:

  * Dynamic locators
  * Custom wrappers
  * Complex API tests

---

# 8️⃣ Recommended Tech Stack

| Layer     | Technology               |
| --------- | ------------------------ |
| Parser    | JavaParser               |
| IR        | JSON + Schema            |
| Validator | AJV                      |
| Optimizer | Rule Engine + LLM        |
| Generator | Template Engine          |
| CI        | GitHub Actions / Jenkins |
| Storage   | File + Optional DB       |

---

# 9️⃣ End-to-End Execution Flow

```
1. Scan source
2. Parse AST
3. Generate IR (modular)
4. Validate IR
5. Optimize IR
6. Incremental check
7. Generate target tests
8. Compile
9. Execute
10. Compare metrics
11. Generate migration report
```

---

# 🔟 Migration Maturity Levels

| Level | Capability                          |
| ----- | ----------------------------------- |
| L1    | Syntax conversion                   |
| L2    | Behavioral mapping                  |
| L3    | Data-aware                          |
| L4    | Execution-aware                     |
| L5    | AI-optimized intelligent migration  |
| L6    | Continuous auto-migration on commit |

This pipeline supports L5–L6.

---

# Final Architecture Principle

This is not a “code converter.”

It is a:

> **Compiler-style transformation pipeline with validation, optimization, and controlled code generation.**

---


Below is a **production-grade Folder-Based IR(Intermediate Representation) Segmentation model** with:

* Modular separation
* Shared targets
* Shared test data
* Separate test files
* Suite mapping
* Login + Order examples
* Referential consistency using `targetId`

This is structured for **1000+ tests scalability**, incremental migration, and parallel processing.

---

# 📁 Recommended IR Folder Structure

```
ir/
 ├── project.json
 ├── environment.json
 ├── targets.json
 ├── data/
 │     ├── login_data.json
 │     └── order_data.json
 ├── suites/
 │     ├── auth_suite.json
 │     └── order_suite.json
 └── tests/
       ├── TC_LOGIN_VALID_001.json
       └── TC_ORDER_CREATE_001.json
```

---

# 1️⃣ project.json

```json
{
  "irVersion": "2.0.0",
  "projectName": "EcommerceAutomation",
  "sourceFramework": "Selenium-Java-TestNG",
  "targetFramework": "Playwright-TS",
  "architecturePattern": "POM",
  "supportsParallel": true,
  "createdOn": "2026-02-12"
}
```

---

# 2️⃣ environment.json

```json
{
  "baseUrls": {
    "qa": "https://qa.example.com"
  },
  "executionMode": "parallel",
  "browsers": ["chrome"],
  "timeouts": {
    "implicit": 5000,
    "explicit": 10000,
    "pageLoad": 30000
  },
  "retryPolicy": {
    "enabled": true,
    "maxRetries": 2
  }
}
```

---

# 3️⃣ targets.json (Central Target Repository)

```json
{
  "targets": [

    {
      "targetId": "LOGIN_USERNAME",
      "type": "ui-element",
      "context": { "page": "LoginPage" },
      "semantic": { "role": "textbox", "businessName": "Username Input" },
      "selectorStrategies": [
        { "strategy": "css", "value": "#username", "stabilityScore": 0.96 },
        { "strategy": "uipath-selector", "value": "<webctrl id='username' />", "stabilityScore": 0.88 }
      ],
      "preferredStrategy": "css"
    },

    {
      "targetId": "LOGIN_PASSWORD",
      "type": "ui-element",
      "context": { "page": "LoginPage" },
      "semantic": { "role": "textbox", "businessName": "Password Input" },
      "selectorStrategies": [
        { "strategy": "css", "value": "#password", "stabilityScore": 0.97 }
      ],
      "preferredStrategy": "css"
    },

    {
      "targetId": "LOGIN_BUTTON",
      "type": "ui-element",
      "context": { "page": "LoginPage" },
      "semantic": { "role": "button", "businessName": "Login Button" },
      "selectorStrategies": [
        { "strategy": "css", "value": "#login-btn", "stabilityScore": 0.94 }
      ],
      "preferredStrategy": "css"
    },

    {
      "targetId": "WELCOME_MESSAGE",
      "type": "ui-element",
      "context": { "page": "HomePage" },
      "semantic": { "role": "label", "businessName": "Welcome Message" },
      "selectorStrategies": [
        { "strategy": "css", "value": "#welcome-msg", "stabilityScore": 0.98 }
      ],
      "preferredStrategy": "css"
    },

    {
      "targetId": "ORDER_PRODUCT_SEARCH",
      "type": "ui-element",
      "context": { "page": "OrderPage" },
      "semantic": { "role": "textbox", "businessName": "Product Search Input" },
      "selectorStrategies": [
        { "strategy": "css", "value": "#search-product", "stabilityScore": 0.93 }
      ],
      "preferredStrategy": "css"
    },

    {
      "targetId": "ORDER_ADD_TO_CART",
      "type": "ui-element",
      "context": { "page": "OrderPage" },
      "semantic": { "role": "button", "businessName": "Add To Cart Button" },
      "selectorStrategies": [
        { "strategy": "css", "value": ".add-to-cart", "stabilityScore": 0.91 }
      ],
      "preferredStrategy": "css"
    },

    {
      "targetId": "ORDER_CONFIRMATION_MSG",
      "type": "ui-element",
      "context": { "page": "OrderConfirmationPage" },
      "semantic": { "role": "label", "businessName": "Order Confirmation Message" },
      "selectorStrategies": [
        { "strategy": "css", "value": "#order-confirm-msg", "stabilityScore": 0.97 }
      ],
      "preferredStrategy": "css"
    }
  ]
}
```

---

# 4️⃣ data/login_data.json

```json
{
  "dataSetId": "LOGIN_DATA",
  "type": "inline",
  "records": [
    {
      "username": "testuser1",
      "password": "Password123",
      "expectedMessage": "Welcome testuser1"
    }
  ]
}
```

---

# 5️⃣ data/order_data.json

```json
{
  "dataSetId": "ORDER_DATA",
  "type": "inline",
  "records": [
    {
      "productName": "Laptop",
      "expectedConfirmation": "Order placed successfully"
    }
  ]
}
```

---

# 6️⃣ suites/auth_suite.json

```json
{
  "suiteId": "AUTH_SUITE",
  "description": "Authentication Tests",
  "tests": [
    "TC_LOGIN_VALID_001"
  ]
}
```

---

# 7️⃣ suites/order_suite.json

```json
{
  "suiteId": "ORDER_SUITE",
  "description": "Order Tests",
  "tests": [
    "TC_ORDER_CREATE_001"
  ]
}
```

---

# 8️⃣ tests/TC_LOGIN_VALID_001.json

```json
{
  "testId": "TC_LOGIN_VALID_001",
  "suiteId": "AUTH_SUITE",
  "priority": "P1",
  "severity": "Critical",

  "dataBinding": {
    "dataSetId": "LOGIN_DATA",
    "iterationStrategy": "row-wise"
  },

  "steps": [
    {
      "stepId": "STEP_01",
      "action": "navigate",
      "target": { "type": "url", "value": "qa:/login" }
    },
    {
      "stepId": "STEP_02",
      "action": "type",
      "targetId": "LOGIN_USERNAME",
      "input": { "source": "data", "field": "username" }
    },
    {
      "stepId": "STEP_03",
      "action": "type",
      "targetId": "LOGIN_PASSWORD",
      "input": { "source": "data", "field": "password", "masked": true }
    },
    {
      "stepId": "STEP_04",
      "action": "click",
      "targetId": "LOGIN_BUTTON"
    },
    {
      "stepId": "STEP_05",
      "action": "waitForVisible",
      "targetId": "WELCOME_MESSAGE"
    }
  ],

  "assertions": [
    {
      "assertId": "ASSERT_01",
      "type": "equals",
      "actual": { "source": "ui", "targetId": "WELCOME_MESSAGE" },
      "expected": { "source": "data", "field": "expectedMessage" }
    }
  ]
}
```

---

# 9️⃣ tests/TC_ORDER_CREATE_001.json

```json
{
  "testId": "TC_ORDER_CREATE_001",
  "suiteId": "ORDER_SUITE",
  "priority": "P1",
  "severity": "High",

  "dataBinding": {
    "dataSetId": "ORDER_DATA",
    "iterationStrategy": "row-wise"
  },

  "steps": [
    {
      "stepId": "STEP_01",
      "action": "navigate",
      "target": { "type": "url", "value": "qa:/orders" }
    },
    {
      "stepId": "STEP_02",
      "action": "type",
      "targetId": "ORDER_PRODUCT_SEARCH",
      "input": { "source": "data", "field": "productName" }
    },
    {
      "stepId": "STEP_03",
      "action": "click",
      "targetId": "ORDER_ADD_TO_CART"
    },
    {
      "stepId": "STEP_04",
      "action": "waitForVisible",
      "targetId": "ORDER_CONFIRMATION_MSG"
    }
  ],

  "assertions": [
    {
      "assertId": "ASSERT_01",
      "type": "equals",
      "actual": { "source": "ui", "targetId": "ORDER_CONFIRMATION_MSG" },
      "expected": { "source": "data", "field": "expectedConfirmation" }
    }
  ]
}
```

---

# 🔎 Why This Model Scales

✔ One test per file
✔ Centralized target repository
✔ Centralized data
✔ Suite orchestration separated
✔ Supports incremental regeneration
✔ Supports parallel transformation
✔ Clean foreign-key style linking
✔ Git-friendly
✔ CI-friendly

---

# 🏗 Architecture Pattern Used

This follows:

> **Normalized Distributed IR with Referential Linking**

Similar to:

* Database normalization
* Compiler intermediate representation segmentation
* Monorepo modularization strategy

---

# AST domain models for static analysis

```python

"""
AST domain models for static analysis.

Purpose:
- Provide language-agnostic AST representations
- Preserve traceability to source files
- Act as a stable contract between parsing and analysis layers
"""

from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from typing import Any, Dict, List, Optional, Generator
from pydantic import BaseModel, Field, TypeAdapter, PrivateAttr


class SourceLocation(BaseModel):
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    start_column: Optional[int] = None
    end_column: Optional[int] = None


class ASTNode(BaseModel):
    """
    Canonical normalized AST node used across entire analysis pipeline.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    node_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    node_type: str
    name: Optional[str] = None

    # ---------------------------------------------------------
    # Structure
    # ---------------------------------------------------------

    children: List["ASTNode"] = Field(default_factory=list)

    # ---------------------------------------------------------
    # Source Mapping
    # ---------------------------------------------------------

    location: Optional[SourceLocation] = None

    # ---------------------------------------------------------
    # Raw Parser Attributes
    # ---------------------------------------------------------

    attributes: Dict[str, Any] = Field(default_factory=dict)

    # ---------------------------------------------------------
    # Semantic Extensions (Future-Proof)
    # ---------------------------------------------------------

    modifiers: List[str] = Field(default_factory=list)
    annotations: List[str] = Field(default_factory=list)

    scope_id: Optional[str] = None        # Symbol table scope reference
    symbol_ref: Optional[str] = None     # Link to resolved symbol
    type_hint: Optional[str] = None      # Optional type info

    # ---------------------------------------------------------
    # Private Parent (Not Serialized)
    # ---------------------------------------------------------

    _parent: Optional["ASTNode"] = PrivateAttr(default=None)

    # ---------------------------------------------------------
    # Parent Handling
    # ---------------------------------------------------------

    @property
    def parent(self) -> Optional["ASTNode"]:
        return self._parent

    def set_parent(self, parent: Optional["ASTNode"]) -> None:
        self._parent = parent

    def add_child(self, child: "ASTNode") -> None:
        child.set_parent(self)
        self.children.append(child)

    # ---------------------------------------------------------
    # Traversal Utilities
    # ---------------------------------------------------------

    def walk(self) -> Generator["ASTNode", None, None]:
        yield self
        for child in self.children:
            yield from child.walk()

    def find_by_type(self, node_type: str) -> List["ASTNode"]:
        return [n for n in self.walk() if n.node_type == node_type]

    def ancestors(self) -> Generator["ASTNode", None, None]:
        current = self.parent
        while current:
            yield current
            current = current.parent

    # ---------------------------------------------------------
    # Safe Serialization
    # ---------------------------------------------------------

    def model_dump(self, *args, **kwargs):
        kwargs.setdefault("exclude", {"_parent"})
        return super().model_dump(*args, **kwargs)


ASTNode.model_rebuild()


class ASTTree(BaseModel): 
    """
    Root container for a parsed source file.
    """
    language: str
    file_path: str
    root: ASTNode
    metadata: Dict[str, Any] = Field(default_factory=dict)


```

Below are **Selenium + Java + TestNG (POM style)** implementations matching your IR:

* `TC_LOGIN_VALID_001`
* `TC_ORDER_CREATE_001`

Assumptions:

* Framework: Selenium WebDriver
* Test Runner: TestNG
* Pattern: Page Object Model
* Parallel-ready
* Explicit waits (no `Thread.sleep`)

---

# 1️⃣ Base Test Setup

## `BaseTest.java`

```java
package base;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;

import java.time.Duration;

public class BaseTest {

    protected WebDriver driver;
    protected WebDriverWait wait;
    protected String baseUrl = "https://qa.example.com";

    @BeforeMethod
    public void setUp() {
        driver = new ChromeDriver();
        driver.manage().window().maximize();
        wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    @AfterMethod
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
```

---

# 2️⃣ Page Objects

## `LoginPage.java`

```java
package pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class LoginPage {

    private WebDriver driver;

    private By username = By.cssSelector("#username");
    private By password = By.cssSelector("#password");
    private By loginButton = By.cssSelector("#login-btn");

    public LoginPage(WebDriver driver) {
        this.driver = driver;
    }

    public void enterUsername(String user) {
        driver.findElement(username).sendKeys(user);
    }

    public void enterPassword(String pass) {
        driver.findElement(password).sendKeys(pass);
    }

    public void clickLogin() {
        driver.findElement(loginButton).click();
    }
}
```

---

## `HomePage.java`

```java
package pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class HomePage {

    private WebDriver driver;

    private By welcomeMessage = By.cssSelector("#welcome-msg");

    public HomePage(WebDriver driver) {
        this.driver = driver;
    }

    public String getWelcomeMessage() {
        return driver.findElement(welcomeMessage).getText();
    }

    public By getWelcomeLocator() {
        return welcomeMessage;
    }
}
```

---

## `OrderPage.java`

```java
package pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class OrderPage {

    private WebDriver driver;

    private By productSearch = By.cssSelector("#search-product");
    private By addToCartButton = By.cssSelector(".add-to-cart");

    public OrderPage(WebDriver driver) {
        this.driver = driver;
    }

    public void searchProduct(String product) {
        driver.findElement(productSearch).sendKeys(product);
    }

    public void clickAddToCart() {
        driver.findElement(addToCartButton).click();
    }
}
```

---

## `OrderConfirmationPage.java`

```java
package pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class OrderConfirmationPage {

    private WebDriver driver;

    private By confirmationMessage = By.cssSelector("#order-confirm-msg");

    public OrderConfirmationPage(WebDriver driver) {
        this.driver = driver;
    }

    public String getConfirmationMessage() {
        return driver.findElement(confirmationMessage).getText();
    }

    public By getConfirmationLocator() {
        return confirmationMessage;
    }
}
```

---

# 3️⃣ Test Classes

---

# ✅ TC_LOGIN_VALID_001

## `TC_LOGIN_VALID_001.java`

```java
package tests;

import base.BaseTest;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.testng.Assert;
import org.testng.annotations.Test;
import pages.HomePage;
import pages.LoginPage;

public class TC_LOGIN_VALID_001 extends BaseTest {

    @Test
    public void validLoginTest() {

        String username = "testuser1";
        String password = "Password123";
        String expectedMessage = "Welcome testuser1";

        driver.get(baseUrl + "/login");

        LoginPage loginPage = new LoginPage(driver);
        loginPage.enterUsername(username);
        loginPage.enterPassword(password);
        loginPage.clickLogin();

        HomePage homePage = new HomePage(driver);

        wait.until(ExpectedConditions.visibilityOfElementLocated(
                homePage.getWelcomeLocator()
        ));

        String actualMessage = homePage.getWelcomeMessage();

        Assert.assertEquals(actualMessage, expectedMessage);
    }
}
```

---

# ✅ TC_ORDER_CREATE_001

## `TC_ORDER_CREATE_001.java`

```java
package tests;

import base.BaseTest;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.testng.Assert;
import org.testng.annotations.Test;
import pages.OrderConfirmationPage;
import pages.OrderPage;

public class TC_ORDER_CREATE_001 extends BaseTest {

    @Test
    public void createOrderTest() {

        String productName = "Laptop";
        String expectedConfirmation = "Order placed successfully";

        driver.get(baseUrl + "/orders");

        OrderPage orderPage = new OrderPage(driver);
        orderPage.searchProduct(productName);
        orderPage.clickAddToCart();

        OrderConfirmationPage confirmationPage =
                new OrderConfirmationPage(driver);

        wait.until(ExpectedConditions.visibilityOfElementLocated(
                confirmationPage.getConfirmationLocator()
        ));

        String actualMessage = confirmationPage.getConfirmationMessage();

        Assert.assertEquals(actualMessage, expectedConfirmation);
    }
}
```

---

# 🔎 Traceability to IR

| IR Step          | Selenium Mapping                             |
| ---------------- | -------------------------------------------- |
| navigate         | `driver.get()`                               |
| type             | `sendKeys()`                                 |
| click            | `click()`                                    |
| waitForVisible   | `WebDriverWait + visibilityOfElementLocated` |
| equals assertion | `Assert.assertEquals()`                      |

---

Below is a **concise, end-to-end demonstration** of how your Selenium Java tests would be transformed into the **Modular IR structure** you designed.

I will show:

1️⃣ What the parser extracts (AST → semantic model)
2️⃣ How targets are resolved
3️⃣ How data binding is inferred
4️⃣ Final IR JSON produced
5️⃣ Dependency graph output

---

# 1️⃣ Static Analysis Phase

Assume this Selenium test:

```java
driver.get(baseUrl + "/login");
loginPage.enterUsername(username);
loginPage.enterPassword(password);
loginPage.clickLogin();
wait.until(ExpectedConditions.visibilityOfElementLocated(
        homePage.getWelcomeLocator()
));
Assert.assertEquals(actualMessage, expectedMessage);
```

---

## Step A — AST Extraction

From your `ASTNode` model, the parser produces simplified semantic nodes:

```
MethodDeclaration(validLoginTest)
 ├── MethodCall(driver.get)
 ├── MethodCall(enterUsername)
 ├── MethodCall(enterPassword)
 ├── MethodCall(clickLogin)
 ├── MethodCall(wait.until)
 └── MethodCall(Assert.assertEquals)
```

Each call contains:

* node_type = "MethodCall"
* name = method name
* attributes:

  * caller
  * arguments
  * resolved_symbol

---

# 2️⃣ Call Graph Resolution

Call graph builder resolves:

```
validLoginTest
  ├── LoginPage.enterUsername
  ├── LoginPage.enterPassword
  ├── LoginPage.clickLogin
  ├── HomePage.getWelcomeLocator
```

This links test method → page object → locator definitions.

---

# 3️⃣ Locator Extraction (Target Builder)

From `LoginPage.java`:

```java
private By username = By.cssSelector("#username");
```

Extractor produces:

```json
{
  "targetId": "LOGIN_USERNAME",
  "type": "ui-element",
  "context": { "page": "LoginPage" },
  "selectorStrategies": [
    { "strategy": "css", "value": "#username" }
  ]
}
```

Repeat for all locators.

---

# 4️⃣ Action Mapping Rules

Mapping rules (semantic layer):

| Selenium Pattern            | IR Action        |
| --------------------------- | ---------------- |
| driver.get()                | navigate         |
| sendKeys()                  | type             |
| click()                     | click            |
| wait.until(visibilityOf...) | waitForVisible   |
| Assert.assertEquals         | equals assertion |

---

# 5️⃣ Data Flow Analysis

From:

```java
String username = "testuser1";
```

Data flow builder classifies:

```
constant → test data
```

Converted into:

```
dataSetId = LOGIN_DATA
iterationStrategy = row-wise
```

---

# 6️⃣ Generated IR (TC_LOGIN_VALID_001)

## `tests/TC_LOGIN_VALID_001.json`

```json
{
  "schemaVersion": "2.0.0",
  "testId": "TC_LOGIN_VALID_001",
  "suiteId": "AUTH_SUITE",
  "sourceChecksum": "sha256-a18fd32e",

  "dataBinding": {
    "dataSetId": "LOGIN_DATA",
    "iterationStrategy": "row-wise"
  },

  "steps": [
    {
      "stepId": "STEP_01",
      "action": "navigate",
      "target": { "type": "url", "value": "qa:/login" }
    },
    {
      "stepId": "STEP_02",
      "action": "type",
      "targetId": "LOGIN_USERNAME",
      "input": { "source": "data", "field": "username" }
    },
    {
      "stepId": "STEP_03",
      "action": "type",
      "targetId": "LOGIN_PASSWORD",
      "input": { "source": "data", "field": "password", "masked": true }
    },
    {
      "stepId": "STEP_04",
      "action": "click",
      "targetId": "LOGIN_BUTTON"
    },
    {
      "stepId": "STEP_05",
      "action": "waitForVisible",
      "targetId": "WELCOME_MESSAGE"
    }
  ],

  "assertions": [
    {
      "assertId": "ASSERT_01",
      "type": "equals",
      "actual": { "source": "ui", "targetId": "WELCOME_MESSAGE" },
      "expected": { "source": "data", "field": "expectedMessage" }
    }
  ]
}
```

---

# 7️⃣ Generated IR (TC_ORDER_CREATE_001)

```json
{
  "schemaVersion": "2.0.0",
  "testId": "TC_ORDER_CREATE_001",
  "suiteId": "ORDER_SUITE",
  "sourceChecksum": "sha256-b91a7dd3",

  "dataBinding": {
    "dataSetId": "ORDER_DATA",
    "iterationStrategy": "row-wise"
  },

  "steps": [
    {
      "stepId": "STEP_01",
      "action": "navigate",
      "target": { "type": "url", "value": "qa:/orders" }
    },
    {
      "stepId": "STEP_02",
      "action": "type",
      "targetId": "ORDER_PRODUCT_SEARCH",
      "input": { "source": "data", "field": "productName" }
    },
    {
      "stepId": "STEP_03",
      "action": "click",
      "targetId": "ORDER_ADD_TO_CART"
    },
    {
      "stepId": "STEP_04",
      "action": "waitForVisible",
      "targetId": "ORDER_CONFIRMATION_MSG"
    }
  ],

  "assertions": [
    {
      "assertId": "ASSERT_01",
      "type": "equals",
      "actual": { "source": "ui", "targetId": "ORDER_CONFIRMATION_MSG" },
      "expected": { "source": "data", "field": "expectedConfirmation" }
    }
  ]
}
```

---

# 8️⃣ Generated Dependency Graph

`dependency_graph.json`

```json
{
  "TC_LOGIN_VALID_001": {
    "targets": [
      "LOGIN_USERNAME",
      "LOGIN_PASSWORD",
      "LOGIN_BUTTON",
      "WELCOME_MESSAGE"
    ],
    "dataSetId": "LOGIN_DATA"
  },
  "TC_ORDER_CREATE_001": {
    "targets": [
      "ORDER_PRODUCT_SEARCH",
      "ORDER_ADD_TO_CART",
      "ORDER_CONFIRMATION_MSG"
    ],
    "dataSetId": "ORDER_DATA"
  }
}
```

This enables incremental invalidation.

---

# 9️⃣ Structural Hashing (Optional Enhancement)

From AST:

```
hash(validLoginTest subtree) → sha256-a18fd32e
```

If only assertion changes:
→ regenerate only that test.

---

# 🔟 End-to-End Flow Summary

```
Selenium Java
   ↓
AST Builder
   ↓
Call Graph Resolution
   ↓
Locator Extraction
   ↓
Data Flow Analysis
   ↓
Action Mapping Engine
   ↓
IR JSON Files
   ↓
Dependency Graph Generation
```

---

# Final Takeaway

The IR is generated by:

* AST normalization
* Lightweight call graph
* Minimal control flow analysis
* Target extraction from page objects
* Data flow tracing
* Deterministic mapping rules

No heavy compiler backend required — just semantic extraction tailored to QA patterns.

---

Below is a **production-grade Git folder structure** for your **IR Generation Engine** (compiler-style QA migration system).

This structure supports:

* Modular static analysis
* AST normalization
* Call/Control/Data flow layers
* IR generation
* Dependency tracking
* Optimization
* Incremental regeneration
* Parallel execution
* CI integration
* Schema evolution

---

# 📁 Repository: `qa-migration-compiler/`

```
qa-migration-compiler/
│
├── README.md
├── pyproject.toml / requirements.txt
├── .gitignore
├── docker/
│     ├── Dockerfile
│     └── docker-compose.yml
│
├── config/
│     ├── default.yaml
│     ├── environments/
│     │      ├── dev.yaml
│     │      └── prod.yaml
│     └── logging.yaml
│
├── schemas/                      # JSON schema contracts
│     ├── ir/
│     │     ├── project.schema.json
│     │     ├── environment.schema.json
│     │     ├── test.schema.json
│     │     ├── targets.schema.json
│     │     └── suite.schema.json
│     └── ast/
│           └── ast_node.schema.json
│
├── src/
│     ├── main.py                 # CLI entry point
│     │
│     ├── core/                   # Compiler core
│     │     ├── pipeline.py
│     │     ├── context.py
│     │     ├── registry.py
│     │     └── exceptions.py
│     │
│     ├── parser/                 # Language parsers
│     │     ├── base_parser.py
│     │     ├── java/
│     │     │     ├── java_parser.py
│     │     │     ├── java_ast_adapter.py
│     │     │     └── symbol_resolver.py
│     │     └── python/
│     │           └── python_parser.py
│     │
│     ├── ast/                    # Canonical AST layer
│     │     ├── models.py         # (your ASTNode, ASTTree)
│     │     ├── builder.py
│     │     ├── hasher.py
│     │     └── metrics.py
│     │
│     ├── analysis/               # Static analysis modules
│     │     ├── call_graph/
│     │     │     ├── builder.py
│     │     │     └── resolver.py
│     │     │
│     │     ├── control_flow/
│     │     │     └── cfg_builder.py
│     │     │
│     │     ├── data_flow/
│     │     │     ├── dfg_builder.py
│     │     │     └── variable_tracker.py
│     │     │
│     │     ├── dependency/
│     │     │     ├── dependency_graph.py
│     │     │     └── invalidation_engine.py
│     │     │
│     │     └── complexity/
│     │           └── analyzer.py
│     │
│     ├── extraction/             # Domain extraction layer
│     │     ├── test_extractor.py
│     │     ├── page_object_extractor.py
│     │     ├── locator_extractor.py
│     │     ├── assertion_mapper.py
│     │     └── action_mapper.py
│     │
│     ├── ir/
│     │     ├── models/
│     │     │     ├── project.py
│     │     │     ├── environment.py
│     │     │     ├── test.py
│     │     │     ├── targets.py
│     │     │     ├── suite.py
│     │     │     └── data.py
│     │     │
│     │     ├── builder/
│     │     │     ├── test_ir_builder.py
│     │     │     ├── targets_ir_builder.py
│     │     │     ├── suite_ir_builder.py
│     │     │     └── project_ir_builder.py
│     │     │
│     │     ├── validator/
│     │     │     ├── schema_validator.py
│     │     │     └── reference_validator.py
│     │     │
│     │     └── writer/
│     │           ├── file_writer.py
│     │           └── deterministic_serializer.py
│     │
│     ├── optimization/
│     │     ├── rules/
│     │     │     ├── xpath_to_css.py
│     │     │     ├── redundant_wait_removal.py
│     │     │     └── flaky_pattern_detector.py
│     │     │
│     │     ├── ai/
│     │     │     └── llm_optimizer.py
│     │     │
│     │     └── confidence_scoring.py
│     │
│     ├── incremental/
│     │     ├── checksum_engine.py
│     │     ├── structural_hash.py
│     │     ├── change_detector.py
│     │     └── regeneration_planner.py
│     │
│     ├── execution/
│     │     ├── worker.py
│     │     ├── queue_adapter.py
│     │     └── batch_processor.py
│     │
│     ├── observability/
│     │     ├── metrics_collector.py
│     │     ├── timing_profiler.py
│     │     └── migration_logger.py
│     │
│     └── utils/
│           ├── file_utils.py
│           ├── hashing.py
│           └── graph_utils.py
│
├── tests/                         # Unit tests for compiler engine
│     ├── test_parser.py
│     ├── test_call_graph.py
│     ├── test_ir_builder.py
│     ├── test_dependency_graph.py
│     └── test_incremental.py
│
├── samples/
│     ├── selenium_input/
│     │     └── login_example.java
│     └── expected_ir_output/
│           └── TC_LOGIN_VALID_001.json
│
├── scripts/
│     ├── run_full_pipeline.sh
│     ├── run_incremental.sh
│     └── validate_ir.sh
│
└── output/                        # Generated IR (gitignored)
      ├── ir/
      ├── optimized_ir/
      └── dependency_graph.json
```

---

# 🔎 Architecture Layer Explanation

## `parser/`

Language-specific AST generation.

## `ast/`

Canonical normalized AST contract.

## `analysis/`

Static analysis engines:

* Call graph
* Control flow
* Data flow
* Dependency graph
* Complexity

## `extraction/`

QA-domain semantic mapping:

* Page object detection
* Locator extraction
* Assertion mapping

## `ir/`

Pure IR layer:

* Models
* Builders
* Validators
* Deterministic writers

Strict separation from parser layer.

## `optimization/`

Rule-based + AI enhancements.

## `incremental/`

Checksum, structural hashing, invalidation logic.

## `execution/`

Parallel worker framework.

## `observability/`

Metrics, p95/p99 timing, failure classification.

---

# 🎯 Design Principles Embedded

* Clean compiler layering
* Deterministic IR serialization
* Schema-driven validation
* Incremental regeneration
* Parallel-safe
* Extensible to multiple languages
* Enterprise CI compatible

---

# Minimal Version (If Starting Lean)

If you want v1 MVP:

Keep only:

```
parser/
ast/
analysis/call_graph/
analysis/dependency/
extraction/
ir/
incremental/
```

Add rest later.

---

