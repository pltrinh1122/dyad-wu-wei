import sys

def require_operator_approval(prompt_text: str) -> bool:
    """
    Enforces the TTY Isolation Principle.
    Reads input directly from /dev/tty if available, completely bypassing standard input.
    This guarantees the confirmation comes from a physical keyboard attached to the
    controlling terminal, preventing spoofing via pipes or automated subprocesses.
    """
    try:
        # Open the physical terminal device directly
        with open('/dev/tty', 'r+') as tty:
            tty.write(prompt_text)
            tty.flush()
            response = tty.readline().strip().lower()
            return response == 'y'
    except OSError:
        # Fallback for environments where /dev/tty is unavailable,
        # but strictly enforce that stdin must be an interactive TTY.
        if not sys.stdin.isatty():
            print("\n[SECURITY EXCEPTION] Operator gate bypass attempted via piped stdin or non-interactive shell.")
            print("Action aborted to prevent automated spoofing.")
            sys.exit(1)
            
        # Standard input is attached to a TTY.
        print(prompt_text, end='', flush=True)
        response = sys.stdin.readline().strip().lower()
        return response == 'y'
