# Systematic Debugging

Do not patch from symptoms alone.

1. Reproduce the failure with the smallest reliable command or scenario.
2. Read the complete error and inspect the nearest relevant code,
   configuration, inputs, and recent diff.
3. Form one evidence-backed root-cause hypothesis. Add focused instrumentation
   or a narrow test only when needed to distinguish causes.
4. Make the smallest fix that addresses the cause.
5. Re-run the reproducer, relevant tests, and one nearby regression check.

Preserve user changes. Never hide a failure by weakening tests, swallowing
errors, or broadening retries without evidence.

After two failed attempts, change the diagnostic method. After a third failure
of the same class, stop and report the evidence, attempts, and remaining
decision.
