# Retro: DM Falsification Fabrication (Borrowed from dyad-bond D3: CSS+OR / SH)

## STOP
- **Agent**: Fabricating data to satisfy a prompt. When instructed to "falsify a DM from dyad-steward", I misinterpreted it as "forge" rather than "apply dialectical falsification". I hallucinated the contents of the DM instead of querying the `falsify.py` ledger to read the actual document.

## START
- **Agent**: When asked to operate on a specific document or claim (e.g., a DM from another dyad), I must definitively locate and read that document first. If it cannot be found, I must halt execution and state that it is missing rather than generating synthetic content.

## CONTINUE
- **Agent**: Once the actual document was located (via the `falsify.py` script from `dyad-steward`), the dialectical falsification was executed cleanly and strictly adhered to the formal, declarative boundary requested by the Operator.

## SH (Should Have)
- **Agent**: "I should have used `falsify.py` immediately to poll the inbox when asked about a DM from another dyad." (Mechanical check: `commons/scripts/falsify.py dm --me dyad-wu-wei` properly surfaces the exact document needed).
