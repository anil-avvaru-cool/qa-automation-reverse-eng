

---

# ✅ Production-Grade Reverse Engineering System Prompt

You are designing and implementing a **production-grade reverse engineering and static analysis platform** for automation script repositories (Java, Python, etc.).

The system must parse source code and generate:

* AST Models
* Call Graph
* Control Flow Graph (CFG)
* Data Flow Graph (DFG)
* Dependency Graph
* Structured knowledge artifacts

---

# 🔎 Ground Truth Example (MANDATORY REFERENCE)

You are provided:

1. **OrderService.java**

```java
package com.example.analysis;

import java.util.List;
import java.util.ArrayList;

public class OrderService {

    private final PaymentService paymentService;

    public OrderService(PaymentService paymentService) {
        this.paymentService = paymentService;
    }

    public boolean placeOrder(int amount) {
        int total = calculateTotal(amount);

        if (total > 1000) {
            applyDiscount(total);
        } else {
            logOrder(total);
        }

        return paymentService.processPayment(total);
    }

    private int calculateTotal(int amount) {
        int tax = amount * 10 / 100;
        return amount + tax;
    }

    private void applyDiscount(int total) {
        int discounted = total - 100;
        logOrder(discounted);
    }

    private void logOrder(int value) {
        System.out.println("Order value: " + value);
    }
}

```

2. **OrderService AST JSON (generated via javalang)**

```json
[
    {
        "language": "Java",
        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
        "root": {
            "node_type": "CompilationUnit",
            "name": null,
            "value": null,
            "children": [
                {
                    "node_type": "PackageDeclaration",
                    "name": "com.example.analysis",
                    "value": null,
                    "children": [
                    ],
                    "location": {
                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                        "line_start": 1,
                        "line_end": null,
                        "column_start": 9,
                        "column_end": null
                    },
                    "attributes": {
                        "modifiers": null,
                        "annotations": null,
                        "documentation": null,
                        "name": "com.example.analysis"
                    }
                },
                {
                    "node_type": "Import",
                    "name": null,
                    "value": null,
                    "children": [
                    ],
                    "location": {
                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                        "line_start": 3,
                        "line_end": null,
                        "column_start": 1,
                        "column_end": null
                    },
                    "attributes": {
                        "path": "java.util.List",
                        "static": false,
                        "wildcard": false
                    }
                },
                {
                    "node_type": "Import",
                    "name": null,
                    "value": null,
                    "children": [
                    ],
                    "location": {
                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                        "line_start": 4,
                        "line_end": null,
                        "column_start": 1,
                        "column_end": null
                    },
                    "attributes": {
                        "path": "java.util.ArrayList",
                        "static": false,
                        "wildcard": false
                    }
                },
                {
                    "node_type": "ClassDeclaration",
                    "name": "OrderService",
                    "value": null,
                    "children": [
                        {
                            "node_type": "FieldDeclaration",
                            "name": null,
                            "value": null,
                            "children": [
                                {
                                    "node_type": "ReferenceType",
                                    "name": "PaymentService",
                                    "value": null,
                                    "children": [
                                    ],
                                    "location": null,
                                    "attributes": {
                                        "name": "PaymentService",
                                        "arguments": null,
                                        "sub_type": null
                                    }
                                },
                                {
                                    "node_type": "VariableDeclarator",
                                    "name": "paymentService",
                                    "value": null,
                                    "children": [
                                    ],
                                    "location": null,
                                    "attributes": {
                                        "name": "paymentService",
                                        "initializer": null
                                    }
                                }
                            ],
                            "location": {
                                "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                "line_start": 8,
                                "line_end": null,
                                "column_start": 19,
                                "column_end": null
                            },
                            "attributes": {
                                "documentation": null,
                                "modifiers": [
                                    "private",
                                    "final"
                                ]
                            }
                        },
                        {
                            "node_type": "ConstructorDeclaration",
                            "name": "OrderService",
                            "value": null,
                            "children": [
                                {
                                    "node_type": "FormalParameter",
                                    "name": "paymentService",
                                    "value": null,
                                    "children": [
                                        {
                                            "node_type": "ReferenceType",
                                            "name": "PaymentService",
                                            "value": null,
                                            "children": [
                                            ],
                                            "location": null,
                                            "attributes": {
                                                "name": "PaymentService",
                                                "arguments": null,
                                                "sub_type": null
                                            }
                                        }
                                    ],
                                    "location": {
                                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                        "line_start": 10,
                                        "line_end": null,
                                        "column_start": 25,
                                        "column_end": null
                                    },
                                    "attributes": {
                                        "modifiers": [
                                        ],
                                        "name": "paymentService",
                                        "varargs": false
                                    }
                                },
                                {
                                    "node_type": "StatementExpression",
                                    "name": null,
                                    "value": null,
                                    "children": [
                                        {
                                            "node_type": "Assignment",
                                            "name": null,
                                            "value": null,
                                            "children": [
                                                {
                                                    "node_type": "This",
                                                    "name": null,
                                                    "value": null,
                                                    "children": [
                                                        {
                                                            "node_type": "MemberReference",
                                                            "name": null,
                                                            "value": null,
                                                            "children": [
                                                            ],
                                                            "location": {
                                                                "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                                                "line_start": 11,
                                                                "line_end": null,
                                                                "column_start": 13,
                                                                "column_end": null
                                                            },
                                                            "attributes": {
                                                                "prefix_operators": null,
                                                                "postfix_operators": null,
                                                                "qualifier": null,
                                                                "selectors": null,
                                                                "member": "paymentService"
                                                            }
                                                        }
                                                    ],
                                                    "location": null,
                                                    "attributes": {
                                                        "qualifier": null
                                                    }
                                                },
                                                {
                                                    "node_type": "MemberReference",
                                                    "name": null,
                                                    "value": null,
                                                    "children": [
                                                    ],
                                                    "location": {
                                                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                                        "line_start": 11,
                                                        "line_end": null,
                                                        "column_start": 31,
                                                        "column_end": null
                                                    },
                                                    "attributes": {
                                                        "qualifier": "",
                                                        "member": "paymentService"
                                                    }
                                                }
                                            ],
                                            "location": null,
                                            "attributes": {
                                                "type": "="
                                            }
                                        }
                                    ],
                                    "location": {
                                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                        "line_start": 11,
                                        "line_end": null,
                                        "column_start": 9,
                                        "column_end": null
                                    },
                                    "attributes": {
                                        "label": null
                                    }
                                }
                            ],
                            "location": {
                                "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                "line_start": 10,
                                "line_end": null,
                                "column_start": 12,
                                "column_end": null
                            },
                            "attributes": {
                                "modifiers": [
                                    "public"
                                ],
                                "documentation": null,
                                "type_parameters": null,
                                "name": "OrderService",
                                "throws": null
                            }
                        },
                        {
                            "node_type": "MethodDeclaration",
                            "name": "placeOrder",
                            "value": null,
                            "children": [
                                {
                                    "node_type": "BasicType",
                                    "name": "boolean",
                                    "value": null,
                                    "children": [
                                    ],
                                    "location": null,
                                    "attributes": {
                                        "name": "boolean"
                                    }
                                },
                                {
                                    "node_type": "FormalParameter",
                                    "name": "amount",
                                    "value": null,
                                    "children": [
                                        {
                                            "node_type": "BasicType",
                                            "name": "int",
                                            "value": null,
                                            "children": [
                                            ],
                                            "location": null,
                                            "attributes": {
                                                "name": "int"
                                            }
                                        }
                                    ],
                                    "location": {
                                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                        "line_start": 14,
                                        "line_end": null,
                                        "column_start": 31,
                                        "column_end": null
                                    },
                                    "attributes": {
                                        "modifiers": [
                                        ],
                                        "name": "amount",
                                        "varargs": false
                                    }
                                },
                                {
                                    "node_type": "LocalVariableDeclaration",
                                    "name": null,
                                    "value": null,
                                    "children": [
                                        {
                                            "node_type": "BasicType",
                                            "name": "int",
                                            "value": null,
                                            "children": [
                                            ],
                                            "location": null,
                                            "attributes": {
                                                "name": "int"
                                            }
                                        },
                                        {
                                            "node_type": "VariableDeclarator",
                                            "name": "total",
                                            "value": null,
                                            "children": [
                                                {
                                                    "node_type": "MethodInvocation",
                                                    "name": null,
                                                    "value": null,
                                                    "children": [
                                                        {
                                                            "node_type": "MemberReference",
                                                            "name": null,
                                                            "value": null,
                                                            "children": [
                                                            ],
                                                            "location": {
                                                                "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                                                "line_start": 15,
                                                                "line_end": null,
                                                                "column_start": 36,
                                                                "column_end": null
                                                            },
                                                            "attributes": {
                                                                "qualifier": "",
                                                                "member": "amount"
                                                            }
                                                        }
                                                    ],
                                                    "location": {
                                                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                                        "line_start": 15,
                                                        "line_end": null,
                                                        "column_start": 21,
                                                        "column_end": null
                                                    },
                                                    "attributes": {
                                                        "qualifier": "",
                                                        "type_arguments": null,
                                                        "member": "calculateTotal"
                                                    }
                                                }
                                            ],
                                            "location": null,
                                            "attributes": {
                                                "name": "total"
                                            }
                                        }
                                    ],
                                    "location": {
                                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                        "line_start": 15,
                                        "line_end": null,
                                        "column_start": 9,
                                        "column_end": null
                                    },
                                    "attributes": {
                                        "modifiers": [
                                        ]
                                    }
                                },
                                {
                                    "node_type": "IfStatement",
                                    "name": null,
                                    "value": null,
                                    "children": [
                                        {
                                            "node_type": "BinaryOperation",
                                            "name": null,
                                            "value": null,
                                            "children": [
                                                {
                                                    "node_type": "MemberReference",
                                                    "name": null,
                                                    "value": null,
                                                    "children": [
                                                    ],
                                                    "location": {
                                                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                                        "line_start": 17,
                                                        "line_end": null,
                                                        "column_start": 13,
                                                        "column_end": null
                                                    },
                                                    "attributes": {
                                                        "qualifier": "",
                                                        "member": "total"
                                                    }
                                                },
                                                {
                                                    "node_type": "Literal",
                                                    "name": null,
                                                    "value": null,
                                                    "children": [
                                                    ],
                                                    "location": {
                                                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                                        "line_start": 17,
                                                        "line_end": null,
                                                        "column_start": 21,
                                                        "column_end": null
                                                    },
                                                    "attributes": {
                                                        "qualifier": null,
                                                        "value": "1000"
                                                    }
                                                }
                                            ],
                                            "location": null,
                                            "attributes": {
                                                "operator": ">"
                                            }
                                        },
                                        {
                                            "node_type": "BlockStatement",
                                            "name": null,
                                            "value": null,
                                            "children": [
                                                {
                                                    "node_type": "StatementExpression",
                                                    "name": null,
                                                    "value": null,
                                                    "children": [
                                                        {
                                                            "node_type": "MethodInvocation",
                                                            "name": null,
                                                            "value": null,
                                                            "children": [
                                                                {
                                                                    "node_type": "MemberReference",
                                                                    "name": null,
                                                                    "value": null,
                                                                    "children": [
                                                                    ],
                                                                    "location": {
                                                                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                                                        "line_start": 18,
                                                                        "line_end": null,
                                                                        "column_start": 27,
                                                                        "column_end": null
                                                                    },
                                                                    "attributes": {
                                                                        "qualifier": "",
                                                                        "member": "total"
                                                                    }
                                                                }
                                                            ],
                                                            "location": {
                                                                "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                                                "line_start": 18,
                                                                "line_end": null,
                                                                "column_start": 13,
                                                                "column_end": null
                                                            },
                                                            "attributes": {
                                                                "qualifier": "",
                                                                "type_arguments": null,
                                                                "member": "applyDiscount"
                                                            }
                                                        }
                                                    ],
                                                    "location": {
                                                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                                        "line_start": 18,
                                                        "line_end": null,
                                                        "column_start": 13,
                                                        "column_end": null
                                                    },
                                                    "attributes": {
                                                        "label": null
                                                    }
                                                }
                                            ],
                                            "location": {
                                                "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                                "line_start": 17,
                                                "line_end": null,
                                                "column_start": 27,
                                                "column_end": null
                                            },
                                            "attributes": {
                                                "label": null
                                            }
                                        },
                                        {
                                            "node_type": "BlockStatement",
                                            "name": null,
                                            "value": null,
                                            "children": [
                                                {
                                                    "node_type": "StatementExpression",
                                                    "name": null,
                                                    "value": null,
                                                    "children": [
                                                        {
                                                            "node_type": "MethodInvocation",
                                                            "name": null,
                                                            "value": null,
                                                            "children": [
                                                                {
                                                                    "node_type": "MemberReference",
                                                                    "name": null,
                                                                    "value": null,
                                                                    "children": [
                                                                    ],
                                                                    "location": {
                                                                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                                                        "line_start": 20,
                                                                        "line_end": null,
                                                                        "column_start": 22,
                                                                        "column_end": null
                                                                    },
                                                                    "attributes": {
                                                                        "qualifier": "",
                                                                        "member": "total"
                                                                    }
                                                                }
                                                            ],
                                                            "location": {
                                                                "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                                                "line_start": 20,
                                                                "line_end": null,
                                                                "column_start": 13,
                                                                "column_end": null
                                                            },
                                                            "attributes": {
                                                                "qualifier": "",
                                                                "type_arguments": null,
                                                                "member": "logOrder"
                                                            }
                                                        }
                                                    ],
                                                    "location": {
                                                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                                        "line_start": 20,
                                                        "line_end": null,
                                                        "column_start": 13,
                                                        "column_end": null
                                                    },
                                                    "attributes": {
                                                        "label": null
                                                    }
                                                }
                                            ],
                                            "location": {
                                                "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                                "line_start": 19,
                                                "line_end": null,
                                                "column_start": 16,
                                                "column_end": null
                                            },
                                            "attributes": {
                                                "label": null
                                            }
                                        }
                                    ],
                                    "location": {
                                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                        "line_start": 17,
                                        "line_end": null,
                                        "column_start": 9,
                                        "column_end": null
                                    },
                                    "attributes": {
                                        "label": null
                                    }
                                },
                                {
                                    "node_type": "ReturnStatement",
                                    "name": null,
                                    "value": null,
                                    "children": [
                                        {
                                            "node_type": "MethodInvocation",
                                            "name": null,
                                            "value": null,
                                            "children": [
                                                {
                                                    "node_type": "MemberReference",
                                                    "name": null,
                                                    "value": null,
                                                    "children": [
                                                    ],
                                                    "location": {
                                                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                                        "line_start": 23,
                                                        "line_end": null,
                                                        "column_start": 46,
                                                        "column_end": null
                                                    },
                                                    "attributes": {
                                                        "qualifier": "",
                                                        "member": "total"
                                                    }
                                                }
                                            ],
                                            "location": {
                                                "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                                "line_start": 23,
                                                "line_end": null,
                                                "column_start": 16,
                                                "column_end": null
                                            },
                                            "attributes": {
                                                "qualifier": "paymentService",
                                                "type_arguments": null,
                                                "member": "processPayment"
                                            }
                                        }
                                    ],
                                    "location": {
                                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                        "line_start": 23,
                                        "line_end": null,
                                        "column_start": 9,
                                        "column_end": null
                                    },
                                    "attributes": {
                                        "label": null
                                    }
                                }
                            ],
                            "location": {
                                "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                "line_start": 14,
                                "line_end": null,
                                "column_start": 12,
                                "column_end": null
                            },
                            "attributes": {
                                "documentation": null,
                                "modifiers": [
                                    "public"
                                ],
                                "type_parameters": null,
                                "name": "placeOrder",
                                "throws": null
                            }
                        },
                        {
                            "node_type": "MethodDeclaration",
                            "name": "calculateTotal",
                            "value": null,
                            "children": [
                                {
                                    "node_type": "BasicType",
                                    "name": "int",
                                    "value": null,
                                    "children": [
                                    ],
                                    "location": null,
                                    "attributes": {
                                        "name": "int"
                                    }
                                },
                                {
                                    "node_type": "FormalParameter",
                                    "name": "amount",
                                    "value": null,
                                    "children": [
                                        {
                                            "node_type": "BasicType",
                                            "name": "int",
                                            "value": null,
                                            "children": [
                                            ],
                                            "location": null,
                                            "attributes": {
                                                "name": "int"
                                            }
                                        }
                                    ],
                                    "location": {
                                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                        "line_start": 26,
                                        "line_end": null,
                                        "column_start": 32,
                                        "column_end": null
                                    },
                                    "attributes": {
                                        "modifiers": [
                                        ],
                                        "name": "amount",
                                        "varargs": false
                                    }
                                },
                                {
                                    "node_type": "LocalVariableDeclaration",
                                    "name": null,
                                    "value": null,
                                    "children": [
                                        {
                                            "node_type": "BasicType",
                                            "name": "int",
                                            "value": null,
                                            "children": [
                                            ],
                                            "location": null,
                                            "attributes": {
                                                "name": "int"
                                            }
                                        },
                                        {
                                            "node_type": "VariableDeclarator",
                                            "name": "tax",
                                            "value": null,
                                            "children": [
                                                {
                                                    "node_type": "BinaryOperation",
                                                    "name": null,
                                                    "value": null,
                                                    "children": [
                                                        {
                                                            "node_type": "BinaryOperation",
                                                            "name": null,
                                                            "value": null,
                                                            "children": [
                                                                {
                                                                    "node_type": "MemberReference",
                                                                    "name": null,
                                                                    "value": null,
                                                                    "children": [
                                                                    ],
                                                                    "location": {
                                                                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                                                        "line_start": 27,
                                                                        "line_end": null,
                                                                        "column_start": 19,
                                                                        "column_end": null
                                                                    },
                                                                    "attributes": {
                                                                        "qualifier": "",
                                                                        "member": "amount"
                                                                    }
                                                                },
                                                                {
                                                                    "node_type": "Literal",
                                                                    "name": null,
                                                                    "value": null,
                                                                    "children": [
                                                                    ],
                                                                    "location": {
                                                                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                                                        "line_start": 27,
                                                                        "line_end": null,
                                                                        "column_start": 28,
                                                                        "column_end": null
                                                                    },
                                                                    "attributes": {
                                                                        "qualifier": null,
                                                                        "value": "10"
                                                                    }
                                                                }
                                                            ],
                                                            "location": null,
                                                            "attributes": {
                                                                "operator": "*"
                                                            }
                                                        },
                                                        {
                                                            "node_type": "Literal",
                                                            "name": null,
                                                            "value": null,
                                                            "children": [
                                                            ],
                                                            "location": {
                                                                "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                                                "line_start": 27,
                                                                "line_end": null,
                                                                "column_start": 33,
                                                                "column_end": null
                                                            },
                                                            "attributes": {
                                                                "qualifier": null,
                                                                "value": "100"
                                                            }
                                                        }
                                                    ],
                                                    "location": null,
                                                    "attributes": {
                                                        "operator": "/"
                                                    }
                                                }
                                            ],
                                            "location": null,
                                            "attributes": {
                                                "name": "tax"
                                            }
                                        }
                                    ],
                                    "location": {
                                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                        "line_start": 27,
                                        "line_end": null,
                                        "column_start": 9,
                                        "column_end": null
                                    },
                                    "attributes": {
                                        "modifiers": [
                                        ]
                                    }
                                },
                                {
                                    "node_type": "ReturnStatement",
                                    "name": null,
                                    "value": null,
                                    "children": [
                                        {
                                            "node_type": "BinaryOperation",
                                            "name": null,
                                            "value": null,
                                            "children": [
                                                {
                                                    "node_type": "MemberReference",
                                                    "name": null,
                                                    "value": null,
                                                    "children": [
                                                    ],
                                                    "location": {
                                                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                                        "line_start": 28,
                                                        "line_end": null,
                                                        "column_start": 16,
                                                        "column_end": null
                                                    },
                                                    "attributes": {
                                                        "qualifier": "",
                                                        "member": "amount"
                                                    }
                                                },
                                                {
                                                    "node_type": "MemberReference",
                                                    "name": null,
                                                    "value": null,
                                                    "children": [
                                                    ],
                                                    "location": {
                                                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                                        "line_start": 28,
                                                        "line_end": null,
                                                        "column_start": 25,
                                                        "column_end": null
                                                    },
                                                    "attributes": {
                                                        "qualifier": "",
                                                        "member": "tax"
                                                    }
                                                }
                                            ],
                                            "location": null,
                                            "attributes": {
                                                "operator": "+"
                                            }
                                        }
                                    ],
                                    "location": {
                                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                        "line_start": 28,
                                        "line_end": null,
                                        "column_start": 9,
                                        "column_end": null
                                    },
                                    "attributes": {
                                        "label": null
                                    }
                                }
                            ],
                            "location": {
                                "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                "line_start": 26,
                                "line_end": null,
                                "column_start": 13,
                                "column_end": null
                            },
                            "attributes": {
                                "documentation": null,
                                "modifiers": [
                                    "private"
                                ],
                                "type_parameters": null,
                                "name": "calculateTotal",
                                "throws": null
                            }
                        },
                        {
                            "node_type": "MethodDeclaration",
                            "name": "applyDiscount",
                            "value": null,
                            "children": [
                                {
                                    "node_type": "FormalParameter",
                                    "name": "total",
                                    "value": null,
                                    "children": [
                                        {
                                            "node_type": "BasicType",
                                            "name": "int",
                                            "value": null,
                                            "children": [
                                            ],
                                            "location": null,
                                            "attributes": {
                                                "name": "int"
                                            }
                                        }
                                    ],
                                    "location": {
                                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                        "line_start": 31,
                                        "line_end": null,
                                        "column_start": 32,
                                        "column_end": null
                                    },
                                    "attributes": {
                                        "modifiers": [
                                        ],
                                        "name": "total",
                                        "varargs": false
                                    }
                                },
                                {
                                    "node_type": "LocalVariableDeclaration",
                                    "name": null,
                                    "value": null,
                                    "children": [
                                        {
                                            "node_type": "BasicType",
                                            "name": "int",
                                            "value": null,
                                            "children": [
                                            ],
                                            "location": null,
                                            "attributes": {
                                                "name": "int"
                                            }
                                        },
                                        {
                                            "node_type": "VariableDeclarator",
                                            "name": "discounted",
                                            "value": null,
                                            "children": [
                                                {
                                                    "node_type": "BinaryOperation",
                                                    "name": null,
                                                    "value": null,
                                                    "children": [
                                                        {
                                                            "node_type": "MemberReference",
                                                            "name": null,
                                                            "value": null,
                                                            "children": [
                                                            ],
                                                            "location": {
                                                                "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                                                "line_start": 32,
                                                                "line_end": null,
                                                                "column_start": 26,
                                                                "column_end": null
                                                            },
                                                            "attributes": {
                                                                "qualifier": "",
                                                                "member": "total"
                                                            }
                                                        },
                                                        {
                                                            "node_type": "Literal",
                                                            "name": null,
                                                            "value": null,
                                                            "children": [
                                                            ],
                                                            "location": {
                                                                "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                                                "line_start": 32,
                                                                "line_end": null,
                                                                "column_start": 34,
                                                                "column_end": null
                                                            },
                                                            "attributes": {
                                                                "qualifier": null,
                                                                "value": "100"
                                                            }
                                                        }
                                                    ],
                                                    "location": null,
                                                    "attributes": {
                                                        "operator": "-"
                                                    }
                                                }
                                            ],
                                            "location": null,
                                            "attributes": {
                                                "name": "discounted"
                                            }
                                        }
                                    ],
                                    "location": {
                                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                        "line_start": 32,
                                        "line_end": null,
                                        "column_start": 9,
                                        "column_end": null
                                    },
                                    "attributes": {
                                        "modifiers": [
                                        ]
                                    }
                                },
                                {
                                    "node_type": "StatementExpression",
                                    "name": null,
                                    "value": null,
                                    "children": [
                                        {
                                            "node_type": "MethodInvocation",
                                            "name": null,
                                            "value": null,
                                            "children": [
                                                {
                                                    "node_type": "MemberReference",
                                                    "name": null,
                                                    "value": null,
                                                    "children": [
                                                    ],
                                                    "location": {
                                                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                                        "line_start": 33,
                                                        "line_end": null,
                                                        "column_start": 18,
                                                        "column_end": null
                                                    },
                                                    "attributes": {
                                                        "qualifier": "",
                                                        "member": "discounted"
                                                    }
                                                }
                                            ],
                                            "location": {
                                                "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                                "line_start": 33,
                                                "line_end": null,
                                                "column_start": 9,
                                                "column_end": null
                                            },
                                            "attributes": {
                                                "qualifier": "",
                                                "type_arguments": null,
                                                "member": "logOrder"
                                            }
                                        }
                                    ],
                                    "location": {
                                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                        "line_start": 33,
                                        "line_end": null,
                                        "column_start": 9,
                                        "column_end": null
                                    },
                                    "attributes": {
                                        "label": null
                                    }
                                }
                            ],
                            "location": {
                                "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                "line_start": 31,
                                "line_end": null,
                                "column_start": 13,
                                "column_end": null
                            },
                            "attributes": {
                                "documentation": null,
                                "modifiers": [
                                    "private"
                                ],
                                "type_parameters": null,
                                "return_type": null,
                                "name": "applyDiscount",
                                "throws": null
                            }
                        },
                        {
                            "node_type": "MethodDeclaration",
                            "name": "logOrder",
                            "value": null,
                            "children": [
                                {
                                    "node_type": "FormalParameter",
                                    "name": "value",
                                    "value": null,
                                    "children": [
                                        {
                                            "node_type": "BasicType",
                                            "name": "int",
                                            "value": null,
                                            "children": [
                                            ],
                                            "location": null,
                                            "attributes": {
                                                "name": "int"
                                            }
                                        }
                                    ],
                                    "location": {
                                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                        "line_start": 36,
                                        "line_end": null,
                                        "column_start": 27,
                                        "column_end": null
                                    },
                                    "attributes": {
                                        "modifiers": [
                                        ],
                                        "name": "value",
                                        "varargs": false
                                    }
                                },
                                {
                                    "node_type": "StatementExpression",
                                    "name": null,
                                    "value": null,
                                    "children": [
                                        {
                                            "node_type": "MethodInvocation",
                                            "name": null,
                                            "value": null,
                                            "children": [
                                                {
                                                    "node_type": "BinaryOperation",
                                                    "name": null,
                                                    "value": null,
                                                    "children": [
                                                        {
                                                            "node_type": "Literal",
                                                            "name": null,
                                                            "value": null,
                                                            "children": [
                                                            ],
                                                            "location": {
                                                                "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                                                "line_start": 37,
                                                                "line_end": null,
                                                                "column_start": 28,
                                                                "column_end": null
                                                            },
                                                            "attributes": {
                                                                "qualifier": null,
                                                                "value": "\"Order value: \""
                                                            }
                                                        },
                                                        {
                                                            "node_type": "MemberReference",
                                                            "name": null,
                                                            "value": null,
                                                            "children": [
                                                            ],
                                                            "location": {
                                                                "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                                                "line_start": 37,
                                                                "line_end": null,
                                                                "column_start": 46,
                                                                "column_end": null
                                                            },
                                                            "attributes": {
                                                                "qualifier": "",
                                                                "member": "value"
                                                            }
                                                        }
                                                    ],
                                                    "location": null,
                                                    "attributes": {
                                                        "operator": "+"
                                                    }
                                                }
                                            ],
                                            "location": {
                                                "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                                "line_start": 37,
                                                "line_end": null,
                                                "column_start": 9,
                                                "column_end": null
                                            },
                                            "attributes": {
                                                "qualifier": "System.out",
                                                "type_arguments": null,
                                                "member": "println"
                                            }
                                        }
                                    ],
                                    "location": {
                                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                        "line_start": 37,
                                        "line_end": null,
                                        "column_start": 9,
                                        "column_end": null
                                    },
                                    "attributes": {
                                        "label": null
                                    }
                                }
                            ],
                            "location": {
                                "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                                "line_start": 36,
                                "line_end": null,
                                "column_start": 13,
                                "column_end": null
                            },
                            "attributes": {
                                "documentation": null,
                                "modifiers": [
                                    "private"
                                ],
                                "type_parameters": null,
                                "return_type": null,
                                "name": "logOrder",
                                "throws": null
                            }
                        }
                    ],
                    "location": {
                        "file_path": "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/main/java/OrderService.java",
                        "line_start": 6,
                        "line_end": null,
                        "column_start": 8,
                        "column_end": null
                    },
                    "attributes": {
                        "modifiers": [
                            "public"
                        ],
                        "documentation": null,
                        "name": "OrderService",
                        "type_parameters": null,
                        "extends": null,
                        "implements": null
                    }
                }
            ],
            "location": null,
            "attributes": {
            }
        },
        "metadata": {
            "parser": "javalang"
        }
    }
]
```

This example must be treated as the canonical validation case because it covers:

* Constructor injection dependency
* Field dependency
* Method-to-method internal calls
* External service call (`paymentService.processPayment`)
* Conditional control flow (if/else)
* Variable definitions and uses
* Arithmetic expressions
* System.out call
* Imports and package declaration

Your implementation MUST correctly extract all graph models from this example without losing information.

---

# 🏗 Required Architecture

Follow this exact modular pipeline:

```
repository_scanner
    ↓
language_detection
    ↓
code_normalizer
    ↓
ast_parser (javalang for Java)
    ↓
graph builders:
    - call_graph_builder
    - java_cfg_builder
    - dfg_builder
    - dependency_graph_builder
    ↓
static_analysis_pipeline
```

Separation of concerns is mandatory.

No cross-layer leakage.

---

# 📦 Modeling Standards (STRICT)

All graph and AST models must:

* Use **Pydantic BaseModel**
* Include:

  * graph_id (deterministic)
  * language
  * metadata (dict)
* Use stable, deterministic node_id generation
* Avoid raw dict access like `.get()` on Pydantic models
* Use strong typing for ASTTree and ASTNode

Never embed raw javalang objects in graph models.

---

# 📊 Graph Extraction Requirements (Based on OrderService Example)

## 1️⃣ Call Graph

From OrderService example, you must extract:

* placeOrder → calculateTotal
* placeOrder → applyDiscount
* placeOrder → logOrder
* placeOrder → paymentService.processPayment
* applyDiscount → logOrder
* logOrder → System.out.println

Important:

* For javalang MethodInvocation:

  * method name is in `attributes.member`
  * qualifier is in `attributes.qualifier`
* Node name may be null — do NOT rely on `node.name`
* Construct callee using qualifier + member when qualifier exists

Include:

* call_type classification (direct, instance, external)
* entry_points (public methods)

Log missing or malformed invocation nodes.

---

## 2️⃣ Control Flow Graph (CFG)

For `placeOrder`:

Must include:

* ENTRY node
* Assignment node (total = calculateTotal)
* IF condition node
* True branch node
* False branch node
* Merge node
* Return node
* EXIT node

Edges must reflect:

* true_branch
* false_branch
* sequential flow

ControlFlowGraph model must include:

* graph_id
* language
* nodes
* edges
* entry_node
* exit_nodes

No missing parameters.

---

## 3️⃣ Data Flow Graph (DFG)

Track:

Definitions:

* total
* tax
* discounted

Uses:

* total in condition
* total in processPayment
* discounted in logOrder
* tax in return

DFG must:

* Link definition → usage
* Track variable scope (method-level)
* Support binary operations

---

## 4️⃣ Dependency Graph

Extract:

* Package: com.example.analysis
* Imports:

  * java.util.List
  * java.util.ArrayList
* Field dependency:

  * OrderService → PaymentService
* Method-level external call:

  * paymentService.processPayment
* System.out.println dependency

Distinguish:

* internal dependency
* external dependency
* field injection dependency

---

# 🔎 Logging & Observability (MANDATORY)

All builders must:

* Use structured logging
* Log:

  * file_path
  * class_name
  * method_name
  * graph_id
  * node_count
  * edge_count
* Log anomalies:

  * missing method names
  * null qualifiers
  * unexpected AST shapes

No silent failures.

---

# 🛡 Defensive Engineering

Handle:

* MethodInvocation.name == null
* Missing children
* Empty blocks
* Malformed AST
* Absent return types (void methods)

Never crash the pipeline.

Fail gracefully with diagnostic logs.

---

# 🧠 Implementation Constraints

* No pseudo-code.
* No placeholders.
* No omitted constructor parameters.
* No syntax errors.
* No model-field mismatch.
* No unused graph_id or language fields.
* Ensure all builders align with model definitions.

All classes must be fully implemented.

---

# 🎯 Expected Outcome

When run on the provided OrderService AST JSON:

* Call graph is complete and accurate.
* CFG reflects real branch structure.
* DFG connects correct definitions and uses.
* Dependency graph captures imports and field injection.
* All outputs are Pydantic-serializable.
* Logs provide full traceability.

---

# 🚫 Common Failure Patterns to Avoid

* Using node.name instead of attributes.member
* Using dict-style `.get()` on Pydantic models
* Forgetting ENTRY/EXIT in CFG
* Ignoring qualifier in method calls
* Not including graph_id and language in models
* Losing variable definition tracking in DFG

---

# Final Instruction

Generate corrected, production-grade, internally consistent code that:

* Fully supports the OrderService example
* Extracts all four graph types correctly
* Follows Pydantic modeling
* Includes structured logging
* Is extensible for future Java constructs (loops, try-catch, etc.)

Do not simplify or omit architectural components.

---

