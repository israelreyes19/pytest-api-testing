# Bug Report & OpenAPI Specification Discrepancies

This document details the critical bugs and contract violations discovered in the **User Management API** during the execution of the automated test suite against both **Dev** and **Prod** environments.

---

## Summary of Findings

| Bug ID | Endpoint | Description | Expected Status | Dev Status | Prod Status | Severity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **BUG-01** | `POST /{env}/users` | Invalid email format is accepted and stored | `400 Bad Request` | `201 Created` | `201 Created` | **High** |
| **BUG-02** | `POST /{env}/users` | Creating a duplicate email triggers unhandled server exception | `409 Conflict` | `500 Error` | `500 Error` | **Critical** |
| **BUG-03** | `GET /{env}/users/{email}` | Querying a non-existent email crashes the server | `404 Not Found` | `500 Error` | `500 Error` | **Critical** |
| **BUG-04** | `DELETE /{env}/users/{email}` | Deleting a non-existent email crashes the server | `404 Not Found` | `500 Error` | `500 Error` | **Critical** |
| **BUG-05** | `DELETE /dev/users/{email}` | Authorization header check is bypassed or missing in Dev | `401 Unauthorized` | `404 Not Found` | `401 Unauthorized` | **High** |

---

## Detailed Bug Descriptions

### BUG-01: Invalid Email Format Allowed (`POST /{env}/users`)
* **Endpoints:** `POST /dev/users` & `POST /prod/users`
* **OpenAPI Spec:** The `CreateUserRequest` schema enforces `format: email`. If the payload contains an invalid email string, the server must return `400 Bad Request`.
* **Actual Behavior:** Both environments accept invalid email strings (e.g., `"invalid_email_format"`) and respond with `201 Created`.
* **Test Failure:**
  ```text
  FAILED tests/test_users.py::TestUsers::test_create_user_invalid_email_format - assert 201 == 400

### BUG-02: Unhandled Exception on Duplicate Email (`POST /{env}/users`)

* **Endpoints:** `POST /dev/users` & `POST /prod/users`  
* **OpenAPI Spec:** Registering an email that already exists should return a controlled 409 Conflict response.  
* **Actual Behavior:** 500 Internal Server Error.  
* **Test Failure:**  
  ```text
  FAILED tests/test_users.py::TestUsers::test_create_duplicated_email - AssertionError: POST /users FAILED. Status: 500

### BUG-03: Server Crash on Non-Existent Lookups (`GET /{env}/users/{email}`)

* **Endpoints:** `GET /dev/users/{email}` & `GET /prod/users/{email}`  
* **OpenAPI Spec:** Querying a non-existent user email must return 404 Not Found.  
* **Actual Behavior:** 500 Internal Server Error.  
* **Test Failure:**
  ```text
  FAILED tests/test_users_email.py::TestUsersEmail::test_get_user_by_email_not_found - assert 500 == 404

### BUG-04: Server Crash on Non-Existent Deletions (`DELETE /{env}/users/{email}`)
  * **Endpoints:** `DELETE /dev/users/{email}` & `DELETE /prod/users/{email}`  
* **OpenAPI Spec:** Deleting a non-existent record should return 404 Not Found.  
* **Actual Behavior:** 500 Internal Server Error.  
* **Test Failure:**
  ```text
  FAILED tests/test_users_delete.py::TestUsersDelete::test_delete_user - assert 500 == 404

### BUG-05: Authentication Middleware Bypass in Dev (`DELETE /dev/users/{email}`)
* **Endpoint:** `DELETE /dev/users/{email}`  
* **OpenAPI Spec:** DELETE requires a valid Authentication header token. Requests without a token or with an invalid token must return 401 Unauthorized.  
* **Actual Behavior:** In dev, unauthorized requests bypass the authentication check and return 404 Not Found directly, whereas prod correctly enforces the 401 Unauthorized response.  
* **Test Failures (Dev Only):**
  ```text
  FAILED tests/test_users_delete.py::TestUsersDelete::test_delete_user_unauthorized - assert 404 == 401
  FAILED tests/test_users_delete.py::TestUsersDelete::test_delete_user_invalid_token - assert 404 == 401