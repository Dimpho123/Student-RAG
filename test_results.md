# RAG Assistant Test Results

## Overview

The RAG Assistant was tested using the FastAPI `/ask` endpoint.

The test suite covers:

- Student Handbook questions
- ZAIO website questions
- Questions that cannot be answered from the available knowledge base

A total of 9 tests were executed.

**Result: 9/9 tests passed.**

---

## Test Results

### Test 1 — Student Handbook: Live Class Times

**Question:**

What are the live class times?

**Retrieved Source:**

Student Handbook - Page 11

**Generated Answer:**

Live classes are scheduled as follows:

- First 12 weeks:
  - Tuesdays: 9 am – 11 am
  - Thursdays: 6 pm – 8 pm
- After the first 12 weeks:
  - Tuesdays only: 9 am – 11 am
- All live sessions are recorded for later viewing.

**Result:** PASS

---

### Test 2 — Student Handbook: Joining Classes

**Question:**

How do I join classes?

**Retrieved Source:**

Student Handbook - Page 12

**Generated Answer:**

Students join live classes through the provided Zoom link. Google Classroom access is provided after orientation, and Discord is available for tutoring support and coding questions.

**Result:** PASS

---

### Test 3 — Student Handbook: First 12 Weeks

**Question:**

What happens after the first 12 weeks?

**Retrieved Source:**

Student Handbook - Page 11

**Generated Answer:**

After the first 12 weeks, students have one live class every Tuesday from 9 am to 11 am.

**Result:** PASS

---

### Test 4 — ZAIO Website: Courses

**Question:**

What courses does ZAIO offer?

**Retrieved Source:**

ZAIO Website - https://www.zaio.io/compare-courses

**Generated Answer:**

ZAIO offers Occupational Certificates in Software Development, Cybersecurity and Data Science, as well as bootcamps in Full Stack AI Engineering, Cloud & DevOps Engineering, Full Stack Web Development, Data Science, Cybersecurity and Digital Marketing.

**Result:** PASS

---

### Test 5 — ZAIO Website: Bootcamps

**Question:**

What bootcamps does ZAIO offer?

**Retrieved Source:**

ZAIO Website - https://www.zaio.io/compare-courses

**Generated Answer:**

ZAIO offers the following bootcamps:

- Full Stack AI Engineer
- Cloud & DevOps Engineer
- Full Stack Web Development
- Data Science
- Cybersecurity
- Digital Marketing

**Result:** PASS

---

### Test 6 — ZAIO Website: Online Learning

**Question:**

Are ZAIO courses fully online?

**Retrieved Source:**

ZAIO Website - https://www.zaio.io/qualifications/occupational-certificate-data-science

**Generated Answer:**

Yes. ZAIO's Occupational Certificate programmes and bootcamps are delivered entirely online.

**Result:** PASS

---

### Test 7 — Unanswerable Question: Population

**Question:**

What is the population of South Africa?

**Retrieved Source:**

None

**Generated Answer:**

I could not find that information in the available knowledge base.

**Result:** PASS

---

### Test 8 — Unanswerable Question: Weather

**Question:**

What will the weather be tomorrow?

**Retrieved Source:**

None

**Generated Answer:**

I could not find that information in the available knowledge base.

**Result:** PASS

---

### Test 9 — Unanswerable Question: Football

**Question:**

Who won the latest football match?

**Retrieved Source:**

None

**Generated Answer:**

I could not find that information in the available knowledge base.

**Result:** PASS

---

## Test Summary

| Test Category | Tests | Passed | Failed |
|---|---:|---:|---:|
| Student Handbook | 3 | 3 | 0 |
| ZAIO Website | 3 | 3 | 0 |
| Unanswerable Questions | 3 | 3 | 0 |
| **Total** | **9** | **9** | **0** |

## Final Result

**9/9 tests passed successfully.**

The tests demonstrate that the RAG assistant can:

1. Retrieve information from the Student Handbook.
2. Retrieve information from the ZAIO website.
3. Generate answers using retrieved knowledge.
4. Return the source used for the answer.
5. Refuse questions when the required information cannot be found in the available knowledge base.

## Test Command

The tests were executed using:

```bash
pytest test_api.py -v -s