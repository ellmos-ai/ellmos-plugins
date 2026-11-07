---
type: llm
---

The answer identifies the root cause - the coupon is applied twice, once per line item in line_total and again on
the subtotal in checkout - and removes one of the two applications. It does not adjust the discount formula,
special-case carts with several items or hard-code the reported numbers.
